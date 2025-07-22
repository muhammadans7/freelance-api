from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsFreelancer(BasePermission):  
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'freelancer'
    
    
class IsClient(BasePermission):  
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'