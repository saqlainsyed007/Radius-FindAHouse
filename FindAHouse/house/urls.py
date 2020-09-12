from django.urls import path

from house.views import HouseSearchView


urlpatterns = [
    path(r'search/', HouseSearchView.as_view(), name='house_search'),
]
