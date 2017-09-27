from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsAuthenticatedOrRetrieve(IsAuthenticated):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                super().has_permission(request, view))
