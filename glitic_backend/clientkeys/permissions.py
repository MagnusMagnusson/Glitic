from rest_framework.permissions import BasePermission, SAFE_METHODS
import hashlib
from clientkeys.models import ClientToken

class ClientKeyChecksumMatch(BasePermission):
    message = "Checksum header does not match body for given key"
    def has_permission(request, view):
        hash = request.headers["X-checksum"]
        imp = request.headers["X-imp"]
        token = request.headers["X-token"]
        try:
            digest = ""
            token_key = ClientToken.objects.get(servertoken = token)
            hasher = token_key.getHashObject()
            print(hash)
            print(imp)
            print(token)
            if request.method in SAFE_METHODS:
                print(request.get_full_path())
            else:  
                b = request.body
                hasher.update(b)
                hasher.update(imp.encode("utf-8"))     
                hasher.update(token_key.clienttoken.encode("utf-8"))
                digest = hasher.hexdigest()      
                print(digest)
            return digest == hash
        except ClientToken.DoesNotExist:
            return False
