from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login_page.as_view(), name='login_page_url'),

    path('logout/', views.logout_page, name='logout_page_url'),
]
