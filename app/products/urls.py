from django.urls import path

from .views import ProductViewSet

app_name = 'products'

urlpatterns = [
    path('', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]

