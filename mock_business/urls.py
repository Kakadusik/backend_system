from django.urls import path
from .views import MockProductListView, MockProductDetailView

urlpatterns = [
    path('products/', MockProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', MockProductDetailView.as_view(), name='product-detail'),
]