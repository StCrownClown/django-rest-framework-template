from django.urls import path

from .views import FlowerImageView, FlowerUploadView, UserFlowerListView

urlpatterns = [
    path('upload/', FlowerUploadView.as_view(), name='flower-upload'),
    path('', UserFlowerListView.as_view(), name='my-flowers'),
    path('<int:flower_id>/', FlowerImageView.as_view(), name='view_flower_image'),
]