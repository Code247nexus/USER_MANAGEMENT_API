import json
import os 
class Operations():
    @classmethod
    def read_db(cls):
        if not os.path.exists("db.json"):
            return {}
        with open("db.json",'r') as f:
            data = json.load(f)
            return data
        
    @classmethod
    def write_db(cls,data):
        with open("db.json",'w') as f:
            json.dump(data,f,indent=4)
    @classmethod
    def create_id(cls):
        data = cls.read_db()
        new_id = str(int(max(data.keys(),default = "0"))+1)
        return new_id