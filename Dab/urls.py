from django.urls import path
from . import views

urlpatterns = [
    path('Dab/', views.copy_data, name='Dab'),
    path('Dab/getTraitements', views.get_traitements, name='Dab'),
    path('Dab/getTraitementsTable/<int:id>/', views.get_traitementsTable, name='Dab'),
    path('Dab/deleteTrait/<int:item_id>/', views.delete_Trait, name='delete_traitement'),   
    path('Dab/executeTraitment' , views.execute_traitement),
    path('Dab/addTraitmentTable' , views.add_to_traitementTable),
    path('Dab/addTraitment' , views.add_traitement),
    path('Dab/deleteTraitId/<int:id>/',views.delete_Trait_id,name="treatment_deleted"),
    path('Dab/ShowTraitements' , views.show_all_traitement),
    path('Dab/ShowAllTraitementsName' , views.show_all_traitement_names),
    
    

    

    
]