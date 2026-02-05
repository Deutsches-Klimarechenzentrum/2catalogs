from copy import deepcopy as copy
import fsspec
import json
from .api_interaction import *
from .defaults import *
import pystac
import math
import itertools

from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
    
def get_combination_list(ups:dict) -> list:
    uplists=[up["allowed"] for up in ups]
    combinations = list(
            itertools.product(
                *uplists
                )
            )
    return [
            {
                ups[i]["name"]:comb[i]
                for i in range(len(ups))
                }
            for comb in combinations
            ]

def get_dataset_dict_from_intake(cat, dsnames:list) -> dict :
    dsdict={}
    for dsname in dsnames:
        desc=cat[dsname].describe()
        ups=desc.get("user_parameters")
        md=desc.get("metadata")
        if ups:
            combination_list=get_combination_list(ups)
            for comb in combination_list:
                iakey=dsname+"."+'_'.join([str(a) for a in list(comb.values())])
                try:
                    ds=cat[dsname](**comb).to_dask() #chunks="auto",storage_options=storage_options).to_dask()
                    ds.attrs["href"]=desc["args"]["urlpath"]
                    ds.attrs["open_kwargs"]=copy(desc["args"])
                    del ds.attrs["open_kwargs"]["urlpath"]
                    ds.attrs["open_kwargs"].update(dict(engine="zarr"))  
                    dsdict[iakey]=ds

                except:
                    print("Could not open "+iakey)
                    continue
        else:
            try:
                dsdict[dsname]=cat[dsname].to_dask() #chunks="auto",storage_options=storage_options).to_dask()
            except:
                print("Could not open "+dsname)
                continue
    return dsdict


def create_main(
    main_id:str,
    pattern_strings:list,
    title:str,
    description:str,
    keywords:list,
    template:dict=None,
):
    from pystac_client import Client as psc
    cat=psc.open(defaults["STAC_API_URL"])
    cols=[
        a
        for a in list(cat.get_collections())
        if any(b in a.id and a.id != main_id for b in pattern_strings )
    ]
    print("Found "+str(len(cols))+" collections")
    main_collection=template if template else cols[0].to_dict()    
    main_collection.update(dict(
        id=main_id,
        title=title,
        description=description,
        keywords=keywords,
    ))
    
    main_collection["links"]=[]
    for col in cols:
        coldict=col.to_dict()
        for childidx,child in enumerate(coldict["links"]):
            if child["rel"]=="self":
                main_collection["links"].append(
                    {
                        "rel":"child",
                        "href":f'{coldict["links"][childidx]["href"].replace(defaults["STAC_API_URL"],defaults["STAC_API_URL_EXT"])}',
                        "type":"application/json"
                    }
        )    
    api_create_or_update_collection(
        defaults["STAC_API_URL"],
        main_id,
        main_collection
    )

def link_and_dump_static_stacs(
    items:list,
    collection:dict,
    project_id:str,
    bucket:str="",
    l_orcestra:bool=False,
):
    for item_json in items:
        item_json["properties"]["description"]=item_json["properties"]["description"].replace(
            "https://eerie.cloud.dkrz.de/datasets/",
            defaults["STAC_BASE_URL"]+"/collections/"+collection["id"]+"/items/"+item_json["id"] + '" #'
        )
        item_json["collection"]="https://s3.eu-dkrz-1.dkrz.cloud/"+'/'.join([bucket,collection["id"]])
        item_json["links"].append(
            {
                "rel": "parent", 
                "href": "collection.json",
                "type": "application/geo+json", 
                "title": collection["title"]
            }
        )
        fn='/'.join(item_json["id"].split('/')[1:])
        if l_orcestra:
            fn="Orcestra-stac_items/"+item_json["id"]
        collection["links"].append(
            {
                "rel": "item", 
                "href": "https://s3.eu-dkrz-1.dkrz.cloud/"+'/'.join([bucket,fn]),
                "type": "application/geo+json", 
                "title": item_json["properties"]["title"]
            }
        )

        json.dump(
            item_json,
            fsspec.open(
                fn,
                "w"
            ).open(),
            indent=4
        )

    json.dump(
        collection,
        fsspec.open(
            f"{project_id}-stac_items/collection.json",
            "w"
        ).open(),
        indent=4
    )

def get_and_set_zoom(item_json:dict)->dict:
    zoomstr=None
    if item_json["properties"].get("zoom"):
        return item_json
    source_id=item_json["properties"].get("source_id")
    iid=item_json.get("id")
    if any(source_id==b for b in ["ICON","ICON-LAM"]):
        zoomstr=iid.split('_')[-1].strip('z').strip('.json')
        if zoomstr.isnumeric():
            item_json["properties"]["zoom"]=int(zoomstr)
    elif "healpix" in iid:
        try:
            zoomstr=iid.split('healpix')[-1].split(' ')[0].strip('.').strip('_snow').strip('_ocea')
            if zoomstr.isnumeric():
                item_json["properties"]["zoom"]=int(math.log2(int(zoomstr)))
        except:
            print(f"Could not find out healpix level for id {item_json['id']}")
    else:
        print(f"Could not find out healpix level for id {item_json['id']}")
    return item_json

def get_spdx_license(exp_license: str) -> str:
    if exp_license:
        URL_LIST_OF_LICENSES="https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json"
        lol=json.load(fsspec.open(URL_LIST_OF_LICENSES).open())["licenses"]
        for license_dict in lol:
            if exp_license == license_dict["licenseId"] or exp_license in license_dict["name"] or license_dict["name"] in exp_license:
                return license_dict["licenseId"]
    return "other"

def get_providers(template_item:dict) -> dict:
    providers=template_item["properties"].get("providers")
    if providers:
        todel=[]
        for i,p in enumerate(providers):
            if not isinstance(p["name"],str):
                print("not str ", p["name"])
                desc=providers[i].get("description")
                if desc:
                    providers[i]["name"]=desc
                else:
                    todel.append(i)
                    providers[i]["name"]="N/A"
                    providers[i]["description"]="N/A"
            if providers[i]["name"]=="252":
                print("name ",entry_id)
        for d in todel:
            del providers[i]
    return providers

def set_version_from_date():
    import datetime
    dnow=datetime.datetime.now()
    return "v"+dnow.strftime("%Y%m%d")


def delete_all_collections_by_prefix(stac_base_url: str, start_string: str):
    from pystac_client import Client as psc
    cat=psc.open(stac_base_url)
    xp_exps=[
        a
        for a in list(cat.get_all_collections())
        if a.id.startswith(start_string) or a.id.startswith(start_string.lower())
    ]
    print(f"Delete {len(xp_exps)} collections")
    for xp_exp in xp_exps:
        try:
            api_delete_collection(stac_base_url,xp_exp.id)
        except:
            print("Not found anymore: "+xp_exp.id)
            
def map_source_to_institution(local_conf: dict):
    if not local_conf.get("institution_id",None):
        lower_model=local_conf["source_id"].lower()
        if "icon" in lower_model:
            local_conf["institution_id"]="MPI-M"
        elif "ifs-fesom" in lower_model:
            local_conf["institution_id"]="AWI"
        elif "ifs-nemo" in lower_model:
            local_conf["institution_id"]="BSC"
        elif "merra" in lower_model:
            local_conf["institution_id"]="GMAO"
        elif "jra-3q" in lower_model:
            local_conf["institution_id"]="JMA"
        elif "cas-esm" in lower_model:
            local_conf["institution_id"]="CAS"
        elif "scream" in lower_model:
            local_conf["institution_id"]="E3SM-Project"            
        elif "ifs" in lower_model:
            local_conf["institution_id"]="ECMWF-DKRZ"
    return local_conf