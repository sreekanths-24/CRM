from django.urls import path
from . import views

urlpatterns = [
    path('', views.sendfeedback, name='sendfeedback'),
    path('ViewFeedbacks', views.viewfeedback, name='viewfeedback'),
    path('searchdata', views.searchdata, name='searchdata'),
    path('searchorder', views.searchorder, name='searchorder'),
    path('searchid', views.searchid, name='searchid'),
    path('ecommdata', views.ecommdata, name='ecommdata'),
    path('ecommorderdata', views.ecommorderdata, name='ecommorderdata'),
    path('supplierrecords', views.supplierrecords, name='supplierrecords'),
    path('supplier/<int:pk>', views.supplier, name='supplier'),
    path('delete_supplier/<int:pk>', views.delete_supplier, name='delete_supplier'),
    path('update_supplier/<int:pk>', views.update_supplier, name='update_supplier'),
    path('add_supplier_record', views.add_supplier_record, name='add_supplier_record'),
    path('dashboard', views.dashboard, name='dashboard'),
]