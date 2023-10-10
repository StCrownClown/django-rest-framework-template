from django.urls import path

from .views import ActivateAccount, UserProfileView, UserRegistrationView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("activate/<str:uidb64>/<str:token>/", ActivateAccount.as_view(), name="activate"),
]
