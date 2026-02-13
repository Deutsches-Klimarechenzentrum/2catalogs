import xarray as xr
from pystac import Item, Asset, MediaType
from datetime import datetime
from copy import deepcopy as copy
import fsspec
import math
import json
from .utils.defaults import *

HOSTURL="https://stac2.cloud.dkrz.de/fastapi"
L_API=True
#HOSTURL="https://s3.eu-dkrz-1.dkrz.cloud"
JUPYTERLITE="https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/jupyterlite/index.html"
HOSTURLS={
    'AWI':None,
    'MPI-M':None
}
ID_TEMPLATE="project_id-source_id-experiment_id-version_id-realm-grid_label-level_type-frequency-cell_methods"
GRIDLOOK = "https://gridlook.pages.dev/"
ALTERNATE_KERCHUNK = dict(
    processed={
        "name": "Processed",
        "description": "Server-side on-the-fly rechunked and unifromly encoded data",
    }
)
XARRAY_DEF=dict(engine="zarr",chunks="auto")
XARRAY_ZARR=dict(consolidated=True)
XARRAY_KERCHUNK=dict(consolidated=False)
XSO={
    "xarray:storage_options":dict(lazy=True)
}
ALTERNATE_ASSETS="https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json"
STAC_EXTENSIONS = [
    "https://stac-extensions.github.io/xarray-assets/v1.0.0/schema.json",
    "https://stac-extensions.github.io/datacube/v2.2.0/schema.json"
]

XARRAY_ITEM = {"xarray:open_kwargs": dict(consolidated="true")}
DKRZ_IMPRINT_POLICY = """
[Imprint](https://www.dkrz.de/en/about-en/contact/impressum) and
[Privacy Policy](https://www.dkrz.de/en/about-en/contact/en-datenschutzhinweise).
"""

NEEDED_ATTRS=[
    'title',
    'description',
    '_xpublish_id',
    'time_min',
    'time_max',
    'bbox',
    'creation_date',
    'institution_id',
    'centre',
    'institution',
    'centreDescription',
    'license'
]

INSTITUTE_KEYS=[
        "institution_id",
        "institute_id",
        "institution",
        "institute",
        "centre"
        ]
SOURCE_KEYS=[
        "source_id",
        "model_id",
        "source",
        "model"
        ]
EXPERIMENT_KEYS=[
        "experiment_id",
        "experiment"
        ]
PROJECT_KEYS=[
        "project_id",
        "project",
        "activity_id",
        "activity"
        ]

frequency_mapping = {
    "10m": "10m",
    "15m": "15m",
    "3h": "3hr",
    "6h": "6hr",
    "1h": "1hr",
    "4h": "4hr",
    "24h": "daily",
    "1d": "daily",
    "day": "daily",
    "daily" : "daily",
    "mon": "monthly",
    "1m": "monthly",
    "1y": "yearly",
    "year": "yearly",
    "grid": "fx"
}

# Function to determine frequency
def set_frequency(inp:str, ds):
    global frequency_mapping
    if not ds.attrs.get("frequency"):
        for keyword, frequency in frequency_mapping.items():
            if keyword in inp.lower():
                ds.attrs["frequency"] = frequency
                break
    if not ds.attrs.get("frequency"):
        ds.attrs["frequency"] = "unknown"  # Default value if no match is found
    return ds

def get_spdx_license(exp_license: str) -> str:
    if exp_license:
        URL_LIST_OF_LICENSES="https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json"
        lol=json.load(fsspec.open(URL_LIST_OF_LICENSES).open())["licenses"]
        for license_dict in lol:
            if exp_license == license_dict["licenseId"] or exp_license in license_dict["name"] or license_dict["name"] in exp_license:
                return license_dict["licenseId"]
    return "other"


def get_bbox(
    ds:xr.Dataset,
    lonmin:float=-180.,
    latmin:float=-90.,
    lonmax:float=180.,
    latmax:float=90.
) -> list:
    if all(a in ds.variables for a in ["lon","lat"]):
        ds=ds.reset_coords()[["lon","lat"]]
        try:
            lonmin=ds["lon"].min().values[()]
            latmin=ds["lat"].min().values[()]
            lonmax=ds["lon"].max().values[()]
            latmax=ds["lat"].max().values[()]
        except:
            pass
    
    return [lonmin, latmin, lonmax, latmax]

def get_cube_extension(ds:xr.Dataset,time_min: str, time_max: str)->dict:
    cube=dict()
    cube['cube:dimensions']=dict()
    cube['cube:variables']=dict()
    for dv in ds.data_vars:
        cube['cube:variables'][dv]=dict(
                type="data",
                dimensions=[*ds[dv].dims],
                unit=ds[dv].attrs.get("units","Not set"),
                description=ds[dv].attrs.get("long_name",dv),
                #attrs=ds[dv].attrs
        )
    if time_min and time_max:
        cube['cube:dimensions']["time"]=dict(
                type="temporal",
                extent=[time_min, time_max]
        )
    return cube

def get_from_attrs(needed_attrs:list, ds:xr.Dataset) -> dict:
    datetimeattr=datetime.now()#.isoformat()
    from_attrs=dict()
    for key in needed_attrs:
        ds_attr=ds.attrs.get(key)
        if ds_attr:
            from_attrs[key]=ds_attr
            if (key=="time_min" or key == "time_max"):
                from_attrs[key]=from_attrs[key].split('.')[0]+'Z'
        if key == "creation_date" and not from_attrs.get(key):
            from_attrs[key]=datetimeattr
            
    return from_attrs
        
def get_geometry(
    bbox:list
) -> dict:
    return {
        "type": "Polygon",
        "coordinates": [[
                [bbox[0], bbox[1]],
                [bbox[0], bbox[3]],
                [bbox[2], bbox[3]],
                [bbox[2], bbox[1]],
                [bbox[0], bbox[1]]
        ]]
    }

def get_time_min_max(ds:xr.Dataset) -> tuple[str, str]:
    time_min = time_max = None
    if "time" in ds.variables:
        time_min=str(ds["time"].min().values[()]).split('.')[0]+'Z'
        time_max=str(ds["time"].max().values[()]).split('.')[0]+'Z'
    return time_min,time_max
        
def get_providers(ds_attrs: dict) -> list:
    providers=[copy(defaults["PROVIDER_DKRZ"])]
    creator_inst_id=ds_attrs.get(
        'institution_id',ds_attrs.get(
            'centre'
        )
    )
    if creator_inst_id:
        creator_inst=ds_attrs.get(
            'institution',ds_attrs.get(
                'centreDescription',"N/A"
            )
        )
        creator=copy(defaults["PROVIDER_DKRZ"])
        creator["name"]=creator_inst_id
        creator["description"]=creator_inst
        creator["url"]=HOSTURLS.get(creator_inst_id,"N/A")
        creator["roles"]=["producer"]
        providers.append(creator)
    return providers

def get_keywords(keywordstr: str) -> list:
    split1=keywordstr.split('-')
    split2=[a.split('_') for a in split1]
    return [element for sublist in split2 for element in sublist]

def get_description(ds:xr.Dataset, href:str=None)-> str:  
    source = next((ds.attrs.get(default) for default in SOURCE_KEYS if ds.attrs.get(default) is not None), "not Set")
    exp = next((ds.attrs.get(default) for default in EXPERIMENT_KEYS if ds.attrs.get(default) is not None), "not Set")
    project = next((ds.attrs.get(default) for default in PROJECT_KEYS if ds.attrs.get(default) is not None), "not Set")
    institute = next((ds.attrs.get(default) for default in INSTITUTE_KEYS if ds.attrs.get(default) is not None), "not Set")
    description = "Simulation data from project '"+project+ "' produced by Earth System Model '"+ source+"' and run by institution '"+institute+"' for the experiment '"+exp+"'"
    if href:
        description+=defaults["ITEM_SNIPPET"].replace(
            "REPLACE_ITEMURI",
            #'"'+defaults["STAC_API_URL_EXT"]+"/collections/"+stac_collection_id_lower+"/items/"+item_id+'"'
            href
        )    
    return description

def refine_for_eerie(item_id:str,griddict:dict)->dict:
    if "icon-esm-er" in item_id and "native" in item_id:
        griddict["store"]="https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/grids/"
        if "atmos" in item_id or "land" in item_id:
            griddict["dataset"]="icon_grid_0033_R02B08_G.zarr"
        elif "ocean" in item_id:
            griddict["dataset"]="icon_grid_0016_R02B09_O.zarr"
    if "gr025" in item_id:
        griddict["store"]="https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/grids/"
        if "ifs-amip" in item_id or "ifs-fesom2" in item_id:
            griddict["dataset"]="gr025_descending.zarr"
        else:
            griddict["dataset"]="gr025.zarr"
    return griddict

def get_gridlook(itemdict:dict,uri:str,ds:xr.Dataset,l_eeriecloud:bool)->dict:
    global L_API
    if not L_API:
        item_id=itemdict["id"]
        store_dataset_dict=dict(
            store='/'.join(uri.split('/')[0:-1]),
            dataset=uri.split('/')[-1]
        )
        if l_eeriecloud:
            store_dataset_dict=dict(
                store=defaults["EERIE_CLOUD_URL"]+"/",
                dataset=defaults["EERIE_CLOUD_URL"]+"/"+item_id+"/zarr"
            )    
        var_store_dataset_dict=dict()
        # Add data variables as assets
    #    for var_name, var_data in ds.data_vars.items():
        for var_name, var_data in ds.variables.items():
            var_store_dataset_dict[var_name]=copy(store_dataset_dict)

        itemdict["default_var"]=list(var_store_dataset_dict.keys())[0]
        itemdict["name"]=itemdict["properties"]["title"]

        griddict=copy(store_dataset_dict)
        if l_eeriecloud:
            griddict=refine_for_eerie(item_id,griddict)

        if "era5" in item_id:
            griddict["store"]="https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/grids/"
            griddict["dataset"]="era5.zarr"

        itemdict["levels"]=[
                dict(
                    name=item_id,
                    time=copy(store_dataset_dict),
                    grid=griddict,
                    datasources=var_store_dataset_dict
                    )
                ]
    return itemdict

def add_eerie_cloud_asset(
    item:Item,
    href:str, 
    extra_fields:dict
) -> Item:
    href_kerchunk='/'.join(href.split('/')[:-1])+"/kerchunk"
    href_zarr='/'.join(href.split('/')[:-1])+"/zarr"    
    extra_fields["alternate"]=copy(ALTERNATE_KERCHUNK)
    extra_fields["alternate"]["processed"]["href"]=href_zarr
    extra_fields["alternate"]["processed"]["name"]="Rechunked and uniformly compressed data"
    item.add_asset(
        "eerie-cloud",
        Asset(
            href=href_kerchunk,
            media_type=MediaType.ZARR,
            roles=["data"],
            title="Zarr-access through eerie cloud",
            description="Chunk-based access on raw-encoded data",
            extra_fields=extra_fields
        )
    )
    return item

def add_links(itemdict:dict,l_eeriecloud:bool)->dict:
    if l_eeriecloud:
        itemdict["links"]=[
            dict(
                rel="DOC",
                href="https://easy.gems.dkrz.de/simulations/EERIE/eerie_data-access_online.html",
                title="Usage of the eerie.cloud"
            )
        ]    
        itemdict["links"].append(dict(
            rel="collection",
            href='/'.join(defaults["EERIE_CLOUD_URL"].split('/')[:-1]+["stac-collection-all.json"]),
            type="application/json"
            ))
    return itemdict

def make_json_serializable(obj):
    """Recursively convert non-JSON serializable values to serializable formats."""
    if isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, bytes):
        return obj.decode(errors="ignore")  # Convert bytes to string
    else:
        try:
            json.dumps(obj)  # Test if serializable
            return obj  # If it works, return as is
        except (TypeError, OverflowError):
            return str(obj)  # Convert unsupported types to strings
    
def get_item_id(ds:xr.Dataset,ds_attrs:dict,l_eeriecloud:bool)->str:
    global ID_TEMPLATE
    if l_eeriecloud:
        if not ds_attrs["_xpublish_id"]:
            raise ValueError(
                "You set l_eeriecloud=True but there is no '_xpublish_id' attribute found which would be used as ID"
            )
        return ds_attrs["_xpublish_id"]
    source=ds.encoding.get("source")
    if source:
        return source.replace('/','-').replace(':','_').replace('.','-')
    if ID_TEMPLATE:
        item_id=copy(ID_TEMPLATE)
        for elem in ID_TEMPALTE.split('-'):
            item_id=item_id.replace(elem,ds.attrs.get(elem))
        return item_id
    return "template"

def xarray_dataset_to_stac_item(
    ds:xr.Dataset,
    ds_format:str="zarr",
    item_id:str=None,
    collection_id:str=None,
    exp_license:str=None,
    title:str=None,
    asset_access="dkrz-disk",
    l_eeriecloud:bool=False,
    l_cubeextension:bool=True,
    l_gridlook:bool=True
) -> Item:

    if ds_format != "zarr":
        raise ValueError("No other formats than zarr yet implemented.")
    #default
    stac_extensions=copy(STAC_EXTENSIONS)
    ds_attrs=get_from_attrs(copy(NEEDED_ATTRS),ds)
    if not item_id:
        item_id=get_item_id(ds,ds_attrs,l_eeriecloud)
    if not title:
        title=ds_attrs.get("title", item_id)
    if not ds_attrs.get("time_min"):
        ds_attrs["time_min"], ds_attrs["time_max"] = get_time_min_max(ds)
    if not ds_attrs.get("bbox"):
        ds_attrs["bbox"]=get_bbox(ds)
        
    stac_href=HOSTURL+"/"+item_id
    if collection_id:
        stac_href=f'{HOSTURL}/collections/{collection_id}/items/{item_id}'
        
    providers=get_providers(ds_attrs)
    license=get_spdx_license(exp_license)
    
    properties={
            "title": title,
            "description": ds_attrs.get("description",get_description(ds,stac_href)),
            "created":ds_attrs["creation_date"],
            "keywords":get_keywords(title),
            "providers":providers,
            "license":license
        }

    datetimeattr=datetime.now()
    if ds_attrs.get("time_min"):
        datetimeattr=None
        properties["start_datetime"]=ds_attrs["time_min"]
        properties["end_datetime"]=ds_attrs["time_max"]

    geometry=get_geometry(ds_attrs["bbox"])
    #geometry=get_geometry(get_bbox(ds))
    
    
    cube=get_cube_extension(ds, ds_attrs["time_min"],ds_attrs["time_max"])
        
    # Create a STAC item
    item = Item(
        id=item_id,
        geometry=geometry,
        bbox=ds_attrs["bbox"],
        #bbox=get_bbox(ds),
        datetime=datetimeattr,
        properties=properties,
        stac_extensions=stac_extensions
    )
    href=ds.encoding.get("source",ds.attrs.get("href"))    
    if l_gridlook:
        gridlook_href=GRIDLOOK+"#"+stac_href
        if L_API and href:
            gridlook_href=GRIDLOOK+"#"+href        
        item.add_asset(
            "gridlook",
            Asset(
                href=gridlook_href,
                media_type=MediaType.HTML,
                title="Visualization with gridlook",
                roles=["Visualization"],
                description="Visualization with gridlook"
            )
        )

    extra_fields={
        'Volume':str(int(ds.nbytes/1024**3)) + " GB uncompressed",
        'No of data variables':str(len(ds.data_vars))
    }
    if href:
        open_kwargs=ds.attrs.get("open_kwargs")
        open_config={
            "xarray:open_kwargs":open_kwargs if open_kwargs else (copy(XARRAY_DEF)|copy(XARRAY_ZARR)),
            "xarray:storage_options":ds.attrs.get("open_storage_options")
        }
        if href.startswith("reference"):
            if not open_config["xarray:storage_options"]:
                open_config["xarray:storage_options"]=copy(XSO)
            if not open_kwargs:
                open_config["xarray:open_kwargs"]=(copy(XARRAY_DEF)|copy(XARRAY_KERCHUNK))
        extra_fields.update(open_config)
        access_title="Zarr-access on dkrz"
        if href.startswith("http"):
            access_title="Zarr-access through cloud storage"
        item.add_asset(
                asset_access,
                Asset(
                    href=href,
                    media_type=MediaType.ZARR,
                    roles=["data"],
                    title=access_title,
                    description="Chunk-based access on raw data",
                    extra_fields=copy(extra_fields)
                )
        )
        if l_eeriecloud:
            item=add_eerie_cloud_asset(item, extra_fields, alternate=True)
    if l_eeriecloud:
        item=add_eerie_cloud_asset(item, extra_fields)
        item.add_asset(
            "xarray_view",
            Asset(
                href=defaults["EERIE_CLOUD_URL"]+"/"+item_id+"/",
                media_type=MediaType.HTML,
                title="Xarray dataset",
                roles=["overview"],
                description="HTML representation of the xarray dataset"
            )
        )
        item.add_asset(
            "jupyterlite",
            Asset(
                href=JUPYTERLITE,
                media_type=MediaType.HTML,
                title="Jupyterlite access",
                roles=["analysis"],
                description="Web-assembly based analysis platform with access to this item"
            )
        )
    itemdict=item.to_dict()
#    for asset in itemdict["assets"].keys():
    itemdict=add_links(itemdict,l_eeriecloud)
    #
    #gridlook
    #
    if l_gridlook:
        itemdict=get_gridlook(
            itemdict,href,ds,l_eeriecloud
        )

    if l_cubeextension:
        itemdict["properties"].update(cube)
        
    itemdict["properties"]["variables"]=list(itemdict["properties"]["cube:variables"].keys())
    if "crs" in ds.variables:
        zoomint=math.log2(int(ds["crs"].attrs["healpix_nside"]))
        itemdict["properties"]["zoom"]=int(math.log2(int(ds["crs"].attrs["healpix_nside"])))
        
    for dsatt,dsattval in ds.attrs.items():
        if not dsatt in itemdict["properties"] and not dsatt in itemdict and not "time" in dsatt.lower():
            itemdict["properties"][dsatt]=dsattval

    itemdict=make_json_serializable(itemdict)
    return itemdict

def add_asset_for_ds(
    item:Item,
    k:str,
    ds:xr.Dataset,
    item_id:str
) -> Item:
    href=ds.encoding.get("source",ds.attrs.get("href")) 
    if not href:
        raise ValueError("Neither found 'source' in encoding nor 'ref' in attributes")
    extra_fields={
        'Volume':str(int(ds.nbytes/1024**3)) + " GB uncompressed",
        'No of data variables':str(len(ds.data_vars))
    }     
    open_kwargs=ds.attrs.get("open_kwargs")
    open_config={
        "xarray:open_kwargs":open_kwargs if open_kwargs else (copy(XARRAY_DEF)|copy(XARRAY_ZARR)),
        "xarray:storage_options":ds.attrs.get("open_storage_options")
    }
    if href.startswith("reference"):
        if not open_config["xarray:storage_options"]:
            open_config["xarray:storage_options"]=copy(XSO)
        if not open_kwargs:
            open_config["xarray:open_kwargs"]=(copy(XARRAY_DEF)|copy(XARRAY_KERCHUNK))
            
    extra_fields.update(open_config)
    access_title="Zarr-access from Lustre"    
    if k == "dkrz-disk":
        newhref=href
        if href.startswith("/"):
            newhref="file://"+href
        item.add_asset(
                "dkrz-disk",
                Asset(
                    href=newhref,
                    media_type=MediaType.ZARR,
                    roles=["data"],
                    title=access_title,
                    description="Chunk-based access on raw data",
                    extra_fields=copy(extra_fields)
                )
        )        
    elif k == "dkrz-cloud":
        access_title="Zarr-access from cloud storage"     
        item.add_asset(
                "dkrz-cloud",
                Asset(
                    href=href,
                    media_type=MediaType.ZARR,
                    roles=["data"],
                    title=access_title,
                    description="Chunk-based access on raw data",
                    extra_fields=copy(extra_fields)
                )
        )                
    elif k == "eerie-cloud":
        item=add_eerie_cloud_asset(item,href, extra_fields)
        item.add_asset(
            "xarray_view",
            Asset(
                href='/'.join(href.split('/')[:-1])+"/",
                media_type=MediaType.HTML,
                title="Xarray dataset",
                roles=["overview"],
                description="HTML representation of the xarray dataset"
            )
        )
    elif k == "archive":
        access_title="Zarr-access from tape archive"     
        item.add_asset(
                "dkrz-tape",
                Asset(
                    href=href,
                    media_type=MediaType.ZARR,
                    roles=["data"],
                    title=access_title,
                    description="Chunk-based access on raw data",
                    extra_fields=copy(extra_fields)
                )
        )
    else:
        raise ValueError(k+" not implemented")
    return item


def get_item_from_source(
    ds:xr.Dataset,
    item_id:str=None,
    title:str=None,
    collection_id:str=None,
    exp_license:str=None,
    l_eeriecloud:bool=False
) -> Item:
    global HOSTURL
    stac_extensions=copy(STAC_EXTENSIONS)
    ds_attrs=get_from_attrs(copy(NEEDED_ATTRS),ds)
    if not item_id:
        item_id=get_item_id(ds,ds_attrs,l_eeriecloud)
    if not title:
        title=ds_attrs.get("title", item_id)
    if not ds_attrs.get("time_min"):
        ds_attrs["time_min"], ds_attrs["time_max"] = get_time_min_max(ds)
    if not ds_attrs.get("bbox"):
        ds_attrs["bbox"]=get_bbox(ds)
        
    stac_href=HOSTURL+"/"+item_id
    if collection_id:
        stac_href=f'{HOSTURL}/collections/{collection_id}/items/{item_id}'
        
    providers=get_providers(ds_attrs)
    license=get_spdx_license(exp_license)
    cube=get_cube_extension(ds, ds_attrs["time_min"],ds_attrs["time_max"])    
    
    properties={
        "title": title,
        "description": ds_attrs.get("description",get_description(ds,stac_href)),
        "created":ds_attrs["creation_date"],
        "keywords":get_keywords(title),
        "providers":providers,
        "license":license,
        "variables":list(cube["cube:variables"].keys()),
        **cube
    }
    if "crs" in ds.variables:
        zoomint=math.log2(int(ds["crs"].attrs["healpix_nside"]))
        properties["zoom"]=int(math.log2(int(ds["crs"].attrs["healpix_nside"])))

    for dsatt,dsattval in ds.attrs.items():
        if not properties.get(dsatt) and not "time" in dsatt.lower():
            properties[dsatt]=dsattval
        
    datetimeattr=datetime.now()
    if ds_attrs.get("time_min"):
        datetimeattr=None
        properties["start_datetime"]=ds_attrs["time_min"]
        properties["end_datetime"]=ds_attrs["time_max"]

    geometry=get_geometry(ds_attrs["bbox"])
        
    # Create a STAC item
    item = Item(
        id=item_id,
        geometry=geometry,
        bbox=ds_attrs["bbox"],
        #bbox=get_bbox(ds),
        datetime=datetimeattr,
        properties=properties,
        stac_extensions=stac_extensions
    )

    return item

def xarray_zarr_datasets_to_stac_item(
    dset_dict:dict,
    item_id:str=None,
    collection_id:str=None,
    exp_license:str=None,
    title:str=None
) ->dict:
    if not any(v for k,v in dset_dict.items()):
        raise ValueError("Need a dataset to start with")
    item_ds=dset_dict[list(dset_dict.keys())[0]]
    item=get_item_from_source(item_ds,item_id,title,collection_id,exp_license)
    for k,ds in dset_dict.items():
        item=add_asset_for_ds(item,k,ds,item_id)
        
    dscloud=None
    for b,ds in dset_dict.items():
        if b in ["dkrz-cloud","eerie-cloud"]:
            dscloud=dset_dict[b]
    if dscloud:
        item.add_asset(
            "jupyterlite",
            Asset(
                href=JUPYTERLITE,
                media_type=MediaType.HTML,
                title="Jupyterlite access",
                roles=["analysis"],
                description="Web-assembly based analysis platform with access to this item"
            )
        ) 
        gridlook_href=GRIDLOOK+"#"
        if "eerie-cloud" in dscloud.encoding["source"]:
            gridlook_href+="/".join(dscloud.encoding["source"].split('/')[:-1]+["stac"])
        else:
            gridlook_href+=dscloud.encoding["source"]
        item.add_asset(
            "gridlook",
            Asset(
                href=gridlook_href,
                media_type=MediaType.HTML,
                title="Visualization with gridlook",
                roles=["Visualization"],
                description="Visualization with gridlook"
            )
        )
        
    itemdict=item.to_dict()
    itemdict=make_json_serializable(itemdict)
    
    return itemdict
        