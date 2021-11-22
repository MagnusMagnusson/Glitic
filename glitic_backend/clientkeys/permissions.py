from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
import hashlib
from clientkeys.models import ClientToken

from rest_framework.permissions import IsAuthenticated


class ClientKeyChecksumMatch(BasePermission):
    message = "Checksum header does not match body for given key"
    def has_permission(request, view):
        if not (
            'x-checksum' in request.headers and 
            'x-imp' in request.headers and 
            'x-token' in request.headers  
        ):
            return False
        hash = request.headers["X-checksum"]
        imp = request.headers["X-imp"]
        token = request.headers["X-token"]
        try:
            digest = ""
            token_key = ClientToken.objects.get(servertoken = token)
            hasher = token_key.getHashObject()
            if request.method in SAFE_METHODS:
                print(request.get_full_path())
                return True
            else:  
                b = request.body
                hasher.update(b)
                hasher.update(imp.encode("utf-8"))     
                hasher.update(token_key.clienttoken.encode("utf-8"))
                digest = hasher.hexdigest() 
            return digest == hash
        except ClientToken.DoesNotExist:
            return False

class IsAuthenticatedOrClientAuthenticted(BasePermission):
    def has_permission(request, view):
        return request.user.is_authenticated | ClientKeyChecksumMatch.has_permission(request,view)
