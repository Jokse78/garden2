from django.urls import path

from . import views
from .views import veisles_sarasas, mano_darzai
urlpatterns = [
    path('', views.index, name='index'),
    path('veisles/', views.veisles_sarasas, name='veisles_sarasas'),
    path('mano_darzai/', views.mano_darzai, name='mano_darzai'),
    path('redaguoti_profilį/', views.redaguoti_profilį, name='redaguoti_profilį'),
    path('apskaiciuoti_seklu_kieki/', views.apskaiciuoti_seklu_kieki, name='apskaiciuoti_seklu_kieki'),
    path('sekti_bukle/<int:darzas_id>/', views.sekti_bukle, name='sekti_bukle'),
    path('filtruoti_irankius/', views.filtruoti_irankius, name='filtruoti_irankius'),
    path('augalu_katalogas/', views.augalu_katalogas, name='augalu_katalogas'),
    path('prideti_nauja_augala/', views.prideti_nauja_augala, name='prideti_nauja_augala'),
    path('sukurti_darzo_plana/', views.sukurti_darzo_plana, name='sukurti_darzo_plana'),
    path('prideti_augalu_vieta/<int:darzo_planas_id>/', views.prideti_augalu_vieta, name='prideti_augalu_vieta'),
]

