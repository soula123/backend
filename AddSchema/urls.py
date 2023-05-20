from django.urls import path
from . import views


urlpatterns = [
    path('api/AddScheme', views.add_scheme),
    path('api/ShowScheme', views.show_all_schema),
    path('api/ShowSchemeNames', views.show_all_schema_names),
    path('api/UpdateSchema', views.update_schema),
    path('api/DeleteSchema', views.delete_items),
    
    path('api/deleteSchema/<int:item_id>/', views.delete_schema, name='delete_item'),
    path('api/showSchema/<int:item_id>/', views.show_schema),
    path('api/EditSchema/<int:item_id>/', views.edit_schema),
    

]