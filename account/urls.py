from django.urls import path,include
from .views import UserRegistrationView, UserLoginView,ProfileView,EditProfileView
from .import views
urlpatterns = [
   
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("login/",UserLoginView.as_view(),name="login"),
    path('logout/',views.user_logout,name="logout"),
    path("profile/",ProfileView.as_view(),name="profile_detail"),
    path('edit_profile/',views.EditProfileView.as_view(),name="edit_profile"),
]