from django.urls import path
from .views import HelloApiView, hello_api, ItemDetailView, ItemListView

urlpatterns = [
    path('hello/', hello_api, name='hello_api'),
    path('hello-class/', HelloApiView.as_view(), name = 'hello_api_class'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/<slug:slug>/', ItemDetailView.as_view(), name='item_detail'),
]
