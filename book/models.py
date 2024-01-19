from django.db import models
from account.models import UserAccount
from categories.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=200)
    image= models.ImageField(upload_to='book/media/uploads/')
    description=models.TextField()
    price = models.IntegerField()
    quantity= models.IntegerField()
    author_name=models.CharField(max_length=200,verbose_name = "Author Name")
    category=models.ManyToManyField(Category)

    def __str__(self):
        return self.book_name

class Comment(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="comments", blank=True,null=True)  
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    body=models.TextField()
    created_on= models.DateTimeField(auto_now_add=True)
   
   
    def __str__(self):
        return f"Comments by {self.name}"       