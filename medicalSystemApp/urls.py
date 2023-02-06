from django.urls import path
from . import views

app_name='medicine'

urlpatterns = [
    path('', views.form_page),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('clear', views.clear, name='clear'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('basicInfo/<int:id>', views.basicInfo, name='basicInfo'),
    path('search', views.search, name='search'),
    path('MidNotes/<int:id>', views.MidNote, name='MidNotes'),
    path('billingHistory/<int:id>', views.billing_History, name='billingHistory'),
    path('midPhoto/<int:id>', views.midPhoto, name='midPhoto'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('destroy', views.destroy, name='destroy'),
]
