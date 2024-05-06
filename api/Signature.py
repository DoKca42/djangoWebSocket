import json
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from Log.Log import Log
from room.UniqId import Uniqid


class Signature:
    def __init__(self):
        pass

    @staticmethod
    def getPrivateKey():
        f = open("key/private_key.pem", "rb")
        #print(f.read())
        #Log.debug("[API] Key", str(f.read()))
        load_key = load_pem_private_key(f.read(), None)
        return load_key

    @staticmethod
    def create_signed_token(data, life_span_minutes=5):
        private_key = Signature.getPrivateKey()
        data['transaction_id'] = Uniqid.generate()
        data['expires'] = (datetime.utcnow() + timedelta(minutes=life_span_minutes)).isoformat()
        data = json.dumps(data).encode()

        signature = private_key.sign(
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return data, signature
