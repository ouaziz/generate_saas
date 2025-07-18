from django.urls import path
from .landingpage import views as landingpage_views
from .backoffice import views as backoffice_views
# from django.conf.urls import handler404

# def custom_404_handler(request, exception):
#     return redirect('error-404-1')  # Replace with your target URL

# handler404 = custom_404_handler

urlpatterns = [
    path('', landingpage_views.index_page, name='index_page_url'),
    path('dashboard/', backoffice_views.dashboard_page, name='dashboard_page_url'),
    path('error-404-1/', landingpage_views.error_404_1, name='error_404_1_url'),
    path('error-500/', landingpage_views.error_500, name='error_500_url'),
]
