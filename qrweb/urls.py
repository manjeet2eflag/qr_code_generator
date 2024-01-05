# from django.urls import path
# from qrweb import views
# urlpatterns = [
#         path('generate-text-file/<str:unique_identifier>/', views.generate_text_file, name='generate_text_file'),

# ]


from django.urls import path
from qrweb import views

urlpatterns = [
    path('home/', views.index, name='index'),  # Change the URL pattern to match '/generate/'
    path('home/upload/', views.upload_data, name='upload_data'),
    path('home/upload/qr/', views.generate_qr, name='generate_qr'),
    path('home/upload/qr/<int:shelter_id>/', views.generate_text_file, name='generate_text_file'),
    # Other URL patterns for qrgen app
]