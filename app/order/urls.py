from django.urls import path

from .views import OrderViewSet

app_name = 'orders'

urlpatterns = [
    path('', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:pk>', OrderViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }))
]
