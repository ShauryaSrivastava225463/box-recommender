from django.urls import path
from .views import ProductListCreateView, BoxListCreateView, RecommendBoxView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('boxes/',    BoxListCreateView.as_view(),    name='box-list-create'),
    path('recommend/', RecommendBoxView.as_view(),   name='recommend-box'),
]
