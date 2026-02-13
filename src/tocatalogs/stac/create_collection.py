import json
import pystac
import fsspec
from copy import deepcopy as copy
import pandas as pd
from .utils.defaults import *
from .utils.misc import *

try:
    dslist=json.load(fsspec.open(defaults["EERIE_CLOUD_URL"]).open())
except:
    print("EERIE Cloud not available")
    dslist=None

def get_template_item_from_eeriecloud(project_id: str) -> pystac.item.Item:
    global dslist
    exp_items=[a for a in dslist if a.startswith(project_id.lower())]
    if project_id == "EERIE":
        exp_items=[a for a in dslist if not any(a.startswith(b) for b in ["nextgems","cosmo","era"])]
    if not exp_items:
        raise ValueError(f"Could not find any item for project {project_id.lower()}")
    for ei in exp_items:
        url=f"{defaults['EERIE_CLOUD_URL']}/{ei}/stac"
        try:
            pyitem=pystac.item.Item.from_file(url)
            return pyitem
        except:
            print(f"Could not open URL '{url}'")
    raise ValueError(f"Could not find a template from eeriecloud for project_id {project_id}")

def _set_stac_collection_id(local_conf: dict, template_item: pystac.item.Item = None):
    stac_collection_id=copy(defaults["STAC_COLLECTION_ID_TEMPLATE"])
    for template_element_raw in defaults["STAC_COLLECTION_ID_TEMPLATE"].split('-'):
        template_element=template_element_raw.replace('<','').replace('>','')
        template_item_value=None
        if template_item:
            template_item_value=template_item.properties.get(template_element)
        local_conf_value=local_conf.get(template_element)
        #
        if local_conf.get("prefer_template"):
            template_element_value=template_item_value if template_item_value else local_conf_value
        else:
            template_element_value=local_conf_value if local_conf_value else template_item_value
        if template_element == "institution_id":
            if not template_element_value and template_item:
                template_element_value=template_item.properties.get(
                    "centre"
                )
            if template_element_value:
                template_element_value=template_element_value.upper()
        if template_element_value:
            #template_element_value=template_element_value.replace('-','_')
            stac_collection_id=stac_collection_id.replace(template_element,template_element_value)
        else:
            raise ValueError(f"Could not find any value for STAC Collection ID template element {template_element}.")
    return stac_collection_id

def get_collection_id_from_item(stac_collection_conf: dict, template_item: pystac.item.Item = None) -> str :
    
    if not stac_collection_conf.get("version_id",None):
        stac_collection_conf["version_id"]=set_version_from_date()
    
    if not template_item:
        try:
            template_item=get_template_item_from_eeriecloud(stac_collection_conf["project_id"])
        except:
            pass
        
    return _set_stac_collection_id(stac_collection_conf, template_item=template_item)

def get_collection_description_from_item(stac_collection_conf: dict, template_item: pystac.item.Item = None, default: str = "Not set") -> str :
    description_key=stac_collection_conf.get(
        "description_key",
        "title"
    )
    if not template_item:
        template_item=get_template_item_from_eeriecloud(stac_collection_conf["project_id"])

    return template_item.properties.get(
        description_key,
        default
    )

def get_and_set_collection_providers_from_item(stac_collection_conf: dict, collection_dict: dict,template_item: dict = None) -> dict:
    if not template_item:
        template_item=get_template_item_from_eeriecloud(stac_collection_conf["project_id"])

    correct_provider_json=copy(collection_dict)
    template_providers=get_providers(template_item.to_dict())
    
    if template_providers:
        correct_provider_json["providers"]=template_providers
    else:
        correct_provider_json["providers"][0] = correct_provider_json["providers"][0]["name"]
    return correct_provider_json

def create_collection_defaults(
    stac_collection_id: str,
    start: str,
    end: str,
    time_format: str = '%Y',
    lon_min: int = -180,
    lon_max: int = 180,
    lat_min: int = -90,
    lat_max: int = 90,
    title: str = None, 
    description: str = None,
    keywords:list = None
):
        
    if not title:
        title=' '.join(stac_collection_id.split('-'))
    if not description:
        description=title
    if not keywords:
        keywords=title.split(' ')

    temporal_extent=pystac.TemporalExtent(
            [
                pd.to_datetime(str(start),format=time_format),
                pd.to_datetime(str(end),format=time_format)
            ]
        )
        
    spatial_extent=pystac.SpatialExtent([lon_min, lat_min, lon_max, lat_max])
    
    collection = pystac.Collection(
        id=stac_collection_id,
        title=title,
        description=description,
        extent=pystac.Extent(
            spatial=spatial_extent,
            temporal=temporal_extent,
        ),
        keywords=keywords,
        providers=[pystac.Provider(defaults["PROVIDER_DKRZ"])],
        #assets=assets,
    )
    collection_dict=collection.to_dict()
    return collection_dict