from django.urls import path

from .views import ProductViewSet, ReviewViewSet

app_name = 'products'

urlpatterns = [
    path('', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        # 'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('<str:pk>/reviews/', ReviewViewSet.as_view({
        'post': 'create',
        'get': 'list',
        # 'delete': 'destroy',
    })),
    path('reviews/<str:pk>', ReviewViewSet.as_view({
        # 'post': 'create',
        # 'get': 'list',
        # 'patch': 'partial_update',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
]

