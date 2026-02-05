import requests

def api_delete_collection(base_url: str, cid: str):
    resp=requests.delete(f"{base_url}/collections/{cid}")
    if resp.status_code not in range(200,209):
        print(f"Status code: {resp.status_code} Cid {cid}")
        raise ValueError(
            f"Error deleting {cid} collection. Message: {resp.text}"
        )
def api_delete_item(base_url: str, cid: str, iid):
    resp=requests.delete(f"{base_url}/collections/{cid}/items/{iid}")
    if resp.status_code not in range(200,209):
        print(f"Status code: {resp.status_code} Cid {cid}")
        raise ValueError(
            f"Error deleting {iid} item from collection {cid}. Message: {resp.text}"
        )
        
def api_update_collection(base_url: str, cid: str, json: dict):
    resp=requests.put(f"{base_url}/collections/{cid}", json=json)
    if resp.status_code not in range(200,209):
        print(f"Status code: {resp.status_code} Cid {cid}")
        raise ValueError(
            f"Error updating {cid} collection. Message: {resp.text}"
        )
def api_update_item(base_url: str, cid: str, iid: str, json: dict):
    resp=requests.put(f"{base_url}/collections/{cid}/items/{iid}", json=json)
    if resp.status_code not in range(200,209):
        print(f"Status code: {resp.status_code} Cid {cid}")
        raise ValueError(
            f"Error updating item {iid} from {cid} collection. Message: {resp.text}"
        )
        
def api_create_collection(base_url: str, json: dict):
    resp=requests.post(f"{base_url}/collections", json=json)
    if resp.status_code not in range(200,209):
        #print(f"Status code: {resp.status_code} Cid {cid}")
        raise ValueError(
            f"Error ingesting collection. Message: {resp.text}"
        )
        
def api_create_item(base_url: str, cid: str, json: dict):
    resp=requests.post(f"{base_url}/collections/{cid}/items", json=json)
    if resp.status_code not in range(200,209):
        #print(f"Status code: {resp.status_code} Cid {cid}")
        raise ValueError(
            f"Error ingesting item for collection {cid}. Message: {resp.text}"
        )
        
def api_create_or_update_collection(base_url: str, cid: str, json: dict):
    try:
        api_create_collection(base_url, json)
    except:
        api_update_collection(base_url, cid, json)

def api_create_or_update_item(base_url: str, cid: str, json: dict, iid: str = None):
    try:
        api_create_item(base_url, cid, json)
    except:
        api_update_item(base_url, cid, iid, json)