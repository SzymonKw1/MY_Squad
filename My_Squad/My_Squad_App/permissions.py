from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperuser(BasePermission): #Tylko superuser ma dostep, czyli admin i Marcel
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Sprawdź, czy użytkownik jest zalogowany
        if not request.user or not request.user.is_authenticated:
            return False
        if 'trening' in request.path.lower():
            return False
        return True
