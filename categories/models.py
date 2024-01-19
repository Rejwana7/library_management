from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,verbose_name='Book Name', null=True,blank=True)
    slug=models.SlugField(max_length=200)

    def __str__(self):
        return self.name