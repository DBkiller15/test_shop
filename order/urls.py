from django.urls import re_path
from .views import OrderListView, TopProductsView, HomeView


urlpatterns = [
    re_path(r'^$', HomeView.as_view(),  name='home'),
    re_path(r'^orders/$', OrderListView.as_view(),  name='orders'),
    re_path(r'^top-products/$', TopProductsView.as_view(),  name='top_products'),
]
