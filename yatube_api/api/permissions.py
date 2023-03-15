from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Ограничение доступа на внесение изменений."""
    message = (
        'Вы не можете вносить изенения, так как не являетесь автором '
        'контента.'
    )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
