from django.urls import path
from .views import HomePageView, arastirmaciDetail, getAllYayin,yayinCreateView,getYayinlarAdmin,arastirmaciDetailVis,getArastirmacilarAdmin,getTurlerAdmin

urlpatterns = [
    path('', HomePageView, name='home'),
    path('arastirmaci/<id>/', arastirmaciDetail, name='arastirmaci_detail'),
    path('arastirmaciVis/<id>/',arastirmaciDetailVis, name='arastirmaci_detailVis'),
    path('yayin/', getAllYayin, name='yayin'),
    path('admin/yayinlar/',getYayinlarAdmin,name='yayin_admin'),
    path('admin/arastirmacilar/',getArastirmacilarAdmin,name='arastirmaci_admin'),
    path('admin/turler/',getTurlerAdmin,name='turler_admin'),
    path('admin/yayinlar/create',yayinCreateView,name='yayin_create')
]
