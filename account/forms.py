from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserAccount

class UserRegistrationForm(UserCreationForm):
    first_name=forms.CharField(label='First Name', widget=forms.TextInput(attrs={'id':'required'}))
    last_name=forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'id':'required'}))
    email=forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'id':'required'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','gender','account_type']


    def save(self,commit=True):
            user=super().save(commit=False)   

            if commit:
                user.save()
                gender= self.cleaned_data.get("gender")  
                account_type =self.cleaned_data.get("account_type") 


                UserAccount.objects.create(
                    user=user,
                    gender=gender,
                    account_type= account_type ,
                    
                )
            return user    

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'id':'required'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
         # jodi user er account thake 
        def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs) 
           if self.instance:
                try:
                    user_account=self.instance.account #account model er data
                
                except UserBankAccount.DoesNotExist:
                    user_account=None

                if user_account:
                    self.fields['account_type'].initial= user_account.account_type
                    self.fields['gender'].initial = user_account.gender  
                

                def save(self,commit=True):
                    user=super.save(commit=False)  

                    if commit:
                        user.save()

                        user_account,created= UserBankAccount.objects.get_or_create(user=user)
                    
                    
                        user_account.account_type = self.cleaned_data['account_type']
                        user_account.gender = self.cleaned_data['gender']
                    
                        user_account.save()

                    

                    return user

        



