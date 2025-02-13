from bson import ObjectId
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def serialize_mongo_doc(doc):
    """Serialize MongoDB document to JSON-compatible format"""
    return json.loads(json.dumps(doc, cls=JSONEncoder)) 