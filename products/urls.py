from django.urls import path
from .views import ProductView

urlpatterns = [
    path('', ProductView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductView.as_view(), name='product-detail'),
]
