from django.urls import path,include
from .views import BookDetailView
from .import views
urlpatterns = [
   
    path("detail/<int:pk>/",BookDetailView.as_view(),name="book_detail"),
   
    
]