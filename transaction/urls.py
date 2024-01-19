from django.urls import path,include
from .views import DepositView,BuyView,BorrowBookview,ReturnView
from .import views
urlpatterns = [
   
    path("deposit/",DepositView.as_view(),name="deposit"),
    path("buy/<int:id>",BuyView.as_view(),name="buy"),
    path("borrow/<int:id>",BorrowBookview.as_view(),name="borrow_book"),
    path("return/<int:id>",ReturnView.as_view(),name="return_book"),
    
]