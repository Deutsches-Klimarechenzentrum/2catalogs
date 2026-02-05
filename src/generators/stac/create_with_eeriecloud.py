from .utils.defaults import *
from .utils.api_interaction import *
from .create_collection import *

import pystac
import fsspec
import json
from copy import deepcopy as copy

UPDATE_DICT={
    "project":["project_id","project"],
    "Earth System Model":["source_id","source"],
    "institution":["institution_id","institution"],
    "experiment":["experiment_id","experiment"]
}

def update_eerieitem_description(item_json:dict, stac_collection_id:str)->dict:
    local_update_dict=copy(UPDATE_DICT)
    #sim_id=item_json["properties"].get("simulation_id")
    #print(sim_id)
    #if sim_id and len(sim_id)==7 and type(sim_id[len(sim_id)-1])==int:
    #    local_update_dict["experiment"].insert(0,"simulation_id")
        
    item_json["properties"]["description"]=item_json["properties"]["description"].replace(
        "https://eerie.cloud.dkrz.de/datasets/",
        defaults["STAC_API_URL_EXT"]+"/collections/"+stac_collection_id.lower()+"/items/"+item_json["id"] + '" #'
    )
    for name,elems in local_update_dict.items():        
        for elem in elems:
            item_json["properties"]["description"]=item_json["properties"]["description"].replace(
                f"{name} 'not Set'",
                f"{name} '"+item_json["properties"].get(elem,'not Set')+"'"
            )
    return item_json

def clean_eeriecloud_item(item_json: dict)->dict:
    if item_json.get("default_var",None):
        del item_json["default_var"]
    for v in list(item_json["properties"]["cube:variables"].keys()):
        del item_json["properties"]["cube:variables"][v]["attrs"]
    return item_json

def get_eeriecloud_item_title(project_id: str, exp_item: dict) -> str:
    pl = project_id.lower()
    ititle=exp_item["id"]
    if any(pl == b for b in ["era5","orcestra", "nextgems", "cosmo-rea"]):
        #item_json["properties"]["description"]="Data from "+item_json["properties"]["title"]+accguide
        ititle=' '.join(exp_item["id"].split('.')[-1].split('_'))
        if ititle.startswith("25"):
            ititle=' '.join('.'.join(exp_item["id"].split('.')[-2:]).split('_'))
    if exp_item["assets"]["dkrz-disk"]["href"].startswith("reference"):
        ititle+=defaults["STAC_ITEM_XPUBLISH_TITLE_SUFFIX"]
    return ititle

def create_items_from_eeriecloud(project_id: str, filterstring: str = None) -> list:
    dslist=json.load(fsspec.open(defaults["EERIE_CLOUD_URL"]).open())
    exp_items=[a for a in dslist if a.startswith(project_id.lower())]
    if project_id == "EERIE":
        exp_items=[a for a in dslist if not any(a.startswith(b) for b in ["nextgems","cosmo","era"])]
    if filterstring:
        exp_items=[a for a in exp_items if filterstring in a]
    items=[]
    for exp_item_name in exp_items:
        stacurl=f"{defaults['EERIE_CLOUD_URL']}/{exp_item_name}/stac"
        try:
            exp_item = pystac.item.Item.from_file(
                stacurl
            )
        except:
            print(f"Could not open {stacurl}")
            continue
        id_item=defaults["STAC_ITEM_ID_XPUBLISH_PREFIX"]+exp_item.id
        item_json=exp_item.to_dict()
        item_json["id"]=id_item
        item_json["properties"]["title"]=get_eeriecloud_item_title(
            project_id, 
            item_json
        )
        item_providers=get_providers(item_json)
        item_json["properties"]["license_id"]=get_spdx_license(item_json["properties"].get("license",None))
        if item_providers:
            item_json["properties"]["providers"]=item_providers
        item_json["properties"]["variables"]=list(item_json["properties"]["cube:variables"].keys())
        item_json=clean_eeriecloud_item(item_json)
        item_json["links"]=[]
        items.append(item_json)
    return items

def create_collection_from_eerieclouditem(
    stac_collection_conf:dict,
    stac_collection_id_raw:str,
    description:str = None,
    template_item:pystac.item.Item = None,
    lon_min: int = -180,
    lon_max: int = 180,
    lat_min: int = -90,
    lat_max: int = 90,
) -> dict:
    
    if not description:
        description=get_collection_description_from_item(
            stac_collection_conf,
            template_item=template_item # This is then taken from eeriecloud
        )
    
    title=None
    stac_collection_id=stac_collection_id_raw
    if '<' in stac_collection_id_raw or '>' in stac_collection_id_raw:
        stac_collection_id=stac_collection_id_raw.replace('<','').replace('>','')
        title=stac_collection_id_raw.replace('<','').replace('>-',' ').replace('>','')        
        title_elements=title.split(' ')
        keywords=copy(title_elements)
        #combine project and activity        
        if title_elements[0] != title_elements[1]:
            title_elements[0]=title_elements[0]+"-"+title_elements[1]
        del title_elements[1]
        
        #append version to experiment
        title=' '.join(title_elements[0:-1])+"-"+title_elements[-1]


    collection=create_collection_defaults( #uses id as title and description
        stac_collection_id,
        start=stac_collection_conf["start"],
        end=stac_collection_conf["end"],
        time_format=stac_collection_conf.get("time_format",None),
        description=description,
        keywords=keywords,
        title=title,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max
    )
    
    collection=get_and_set_collection_providers_from_item(
        stac_collection_conf, 
        collection,
        template_item=template_item #taken from eeriecloud
    )
    
    return collection