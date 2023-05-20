from django.urls import path
from . import views


urlpatterns = [
    path('api/AddDatabase', views.addDb),
    path('api/duplicateEnv/<int:id>/', views.duplicate_row, name='duplicate_row'),
    path('api/testconnection/<int:id>/',views.test_connection,name='test_connection'),
    path('api/displayAll',views.read_all_data), 
    path('api/deleteEnv/<int:item_id>/', views.delete_env, name='delete_env'),
    path('api/delete',views.delete_multiple),
    path('api/ShowEnv',views.show_Env),
    path('api/GetEnv/<int:item_id>/', views.show_one_env),
    path('api/EditDatabase/<int:item_id>/',views.edit_env),
]