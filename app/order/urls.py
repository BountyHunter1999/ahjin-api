from django.urls import path

from .views import OrderViewSet

app_name = 'orders'

urlpatterns = [
    path('', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:pk>', OrderViewSet.as_view({
        'get': 'retrieve_order',
        'delete': 'destroy',
        'patch': 'update'
    })),
    path('user/<str:pk>', OrderViewSet.as_view({
        'get': 'retrieve_user_order',

    })),
]
