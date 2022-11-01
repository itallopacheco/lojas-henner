from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class IsOwnerAddress(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cliente.id == request.user.id
       

    def has_permission(self,request,view):
        return super().has_permission(request,view)

class IsOwnerCard(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cliente.id == request.user.id

    def has_permission(self,request,view):
        return super().has_permission(request,view)

