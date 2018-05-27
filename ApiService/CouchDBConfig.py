#! /bin/env/python3

import base64
import http.client
import json



class CouchDBConfig:
    def __init__(self, config_file):
        getBytes = lambda x: bytes(x, encoding="utf-8")
        with open(config_file) as json_data:
            conf = json.load(json_data)
            header = {
                "Authorization": "Basic " + str(base64.b64encode(getBytes(conf["account"] + ":" + conf["password"])),
                                                encoding='utf-8')
            }
            self.protocol = conf["protocol"]
            self.base_url = conf["db_location"]
            self.header = header

