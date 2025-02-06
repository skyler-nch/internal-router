import os
import requests
import json

class routes:
    def __init__(self):
        self.basedbpath = os.getenv("CONNECTIONPOOLPATH") + "/mongo"
        print(self.basedbpath)

    def _postrequest(self,payload:dict):
        response = requests.post(self.basedbpath,payload)
        return response.json()

    def retrieve_route(self,path:str):
        payload = {
            "db":"Penguin",
            "collection":"routes",
            "operation":"find_one",
            "data":json.dumps({"_id":path})
        }

        return self._postrequest(payload)

    def create_route(self,path:str,link:str,method:str):
        payload = {
            "db":"Penguin",
            "collection":"routes",
            "operation":"insert_one",
            "data":json.dumps({
                "_id":path,
                "link":link,
                "method":method
            })
        }

        return self._postrequest(payload)
    
    def redirect(self,path:str):
        link = self.retrieve_route(path)
        return link["link"]