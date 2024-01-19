from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .constants import Deposit, Purchase, Borrow, Return
from book.models import Book
from .models import Transaction
from django.urls import reverse_lazy
from django.views import View
from.forms import DepositForm
from django.contrib import messages
from .models import UserAccount
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template,{
           'user': user,
           'amount': amount,
        })
  
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

def send_book_email(user,amount,subject,book,template):
    message = render_to_string(template,{
       'user': user,
       'amount':amount,
       'book':book,
    })
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()


# class DepositView(LoginRequiredMixin,CreateView):
#     template_name="deposit_form.html"
#     form_class= DepositForm
#     success_url= reverse_lazy('profile')

#     def form_valid(self, form):
#         amount=form.cleaned_data.get('amount')
#         user_account= UserAccount.objects.get(user=self.request.user)
#         user_account.balance+=amount
#         user_account.save(
#             update_fields=[
#                 'balance'
#             ]
#         )

#         transaction=form.save(commit=False)
#         transaction.user=self.request.user
#         transaction.transaction_type=Deposit
#         transaction.balance_after_transaction=user_account.balance
#         transaction.save()
#         messages.success(
#             self.request,
#             f'Successfully Deposit {"{:,.2f}".format(float(amount))}$ from your account'
#         )
#         return super().form_valid(form)

class DepositView(LoginRequiredMixin,CreateView):
    template_name="deposit_form.html"
    form_class= DepositForm
    success_url= reverse_lazy('profile_detail')

    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        user_account= self.request.user.account
        user_account.balance+=amount
        user_account.save(
            update_fields=[
                'balance'
            ]
        )

        transaction=form.save(commit=False)
        transaction.user=user_account
        transaction.transaction_type=Deposit
        transaction.balance_after_transaction=user_account.balance
        transaction.save()
        messages.success(
            self.request,
            f'Successfully Deposit {"{:,.2f}".format(float(amount))}$ from your account'
        )
        send_transaction_email(self.request.user,amount,"Deposit Message","deposit_email.html")
        return super().form_valid(form)








class BuyView(LoginRequiredMixin,View):

    def get(self,request,id):
        book=Book.objects.get(pk=id)
        user=self.request.user.account

        if book.quantity>0:
            if user.balance>=book.price:
                user.balance -= book.price
                user.save()
                messages.success(self.request,"Successfully Buying a book")
                book.quantity -=1
                book.save()
                transaction =Transaction.objects.create(
                    user = user,
                    amount = book.price,
                    balance_after_transaction = user.balance,
                    transaction_type = Purchase,
                    book=book,


                )
                send_book_email(self.request.user,book.price,"borrowing_book",book.book_name,"borrow_email.html")
               
                return redirect('profile_detail')
               
            else:
                messages.error(self.request,"Your total balance less than book price")
                return redirect("deposit")

        else:
              messages.error(self.request,"THe book out of stock")
              return redirect("homepage",pk=id)


class BorrowBookview(LoginRequiredMixin,View):
    def get(self,request,id):
        book=Book.objects.get(pk=id)
        user=self.request.user.account

        if book.quantity>0:
            if user.balance>=book.price:
                user.balance -= book.price
                user.save()
                messages.success(self.request,"Successfully Borrowing a book")
                book.quantity -=1
                book.save()
                transaction =Transaction.objects.create(
                    user = user,
                    amount = book.price,
                    balance_after_transaction = user.balance,
                    transaction_type = Borrow,
                    book=book,


                )
                send_book_email(self.request.user,book.price,"borrowing_book",book.book_name,"borrow_email.html")
                
                return redirect('profile_detail')
               
            else:
                messages.error(self.request,"Your total balance less than book price")
                return redirect("deposit")

        else:
              messages.error(self.request,"The book out of stock")
              return redirect("homepage",pk=id)

  

# class ReturnView(LoginRequiredMixin,View):
#      def get(self,request,id):
#         book=Book.objects.get(pk=id)
#         user=self.request.user.account

#         borrow= Transaction.objects.filter(user= user,book=book,is_returned=False)

#         if not borrow.is_returned:
#             borrow.is_returned =True
#             borrow.save()
#             user.balance +=book.price
#             user.save()
#             book.quantity +=1
#             book.save()

#             messages.success(self.request,"Return Successfully")
#             transaction =Transaction.objects.create(
#                     user = user,
#                     amount = book.price,
#                     balance_after_transaction = user.balance,
#                     transaction_type = Return,
#                     book=book,
#                     is_returned =True


#                 )
#             transaction.save()
#             send_book_email(self.request.user,book.price,"returning_book",book.book_name,"return_email.html")
#             return redirect('profile_detail')


#         else:
#             messages.error(self.request,'Already Return the book')
#             return redirect("homepage")




class ReturnView(LoginRequiredMixin,View):
     def get(self,request,id):
        book=Book.objects.get(pk=id)
        user=self.request.user.account

        borrows= Transaction.objects.filter(user= user,book=book,is_returned=False)
        if borrows.exists():
           for borrow in borrows:
                borrow.is_returned =True
                borrow.save()
                user.balance +=book.price
                user.save()
                book.quantity +=1
                book.save()

                messages.success(self.request,"Return Successfully")
                transaction =Transaction.objects.create(
                        user = user,
                        amount = book.price,
                        balance_after_transaction = user.balance,
                        transaction_type = Return,
                        book=book,
                        is_returned =True


                    )
                transaction.save()
                send_book_email(self.request.user,book.price,"returning_book",book.book_name,"return_email.html")
                return redirect('profile_detail')


        else:
            messages.error(self.request,'Already Return the book')
            return redirect("homepage")
