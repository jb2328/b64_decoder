#null decoder
import base64

loaded="GENERIC"

def b64toBytes(b64):
    return base64.b64decode(b64)
    
def decodePayload(data):
    obj = {}
    obj["device"]="unknown"
    obj["data"]=data.decode('utf-8')
    return obj
