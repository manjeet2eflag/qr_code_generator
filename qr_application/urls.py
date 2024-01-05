from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from qrweb import views

# from qrgen.admin import qr_gen_admin_site


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page as home page

    # Protected URL pattern for qrweb after login
    # path('qrweb/', include('qrweb.urls'), name='qrweb'),///
    # path('homepage/', include('qrweb.urls')), 
    path("", include("pages.urls")),


    path('home/', views.index, name='index'),
    path('home/upload/', views.upload_data, name='upload_data'),
    path('home/upload/qr/', views.generate_qr, name='generate_qr'),
    path('home/upload/qr/<int:shelter_id>/', views.show_shelter_details, name='shelter_details'),
    
    # path('qr_gen_admin/', qr_gen_admin_site.urls),
]
