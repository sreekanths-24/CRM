from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home_crm'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout_crm'),
    path('register/', views.register_user, name='register_crm'),
    path('record/<int:pk>', views.customer_record, name='record_crm'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record_crm'),
    path('update_record/<int:pk>', views.update_record, name='update_record_crm'),
]