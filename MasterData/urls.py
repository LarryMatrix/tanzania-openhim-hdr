from django.urls import path
from MasterData import views

urlpatterns = [
    path('departments', views.get_departments_page, name='get_departments_page'),
    path('exemptions', views.get_exemptions_page, name='get_exemptions_page'),
    path('payers', views.get_payers_page, name='get_payers_page'),
    path('wards', views.get_wards_page, name='get_wards_page'),
    path('gender', views.get_gender_page, name='get_gender_page'),
    path('places_of_death', views.get_places_of_death_page, name='get_places_of_death_page'),
    path('service_provider_rankings', views.get_service_provider_rankings_page, name='get_service_provider_rankings_page'),
    path('delete_mapping', views.delete_mapping, name='delete_mapping'),

]