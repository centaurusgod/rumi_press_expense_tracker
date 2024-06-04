from django.db import models

# Create your models here.

class BookCat(models.Model):
    cat_name = models.CharField(max_length=254)
    def __str__(self):
        return self.cat_name

class Books(models.Model):
    book_name = models.CharField(max_length=254)
    book_auth_name = models.CharField(max_length=254, default="Author")
    book_cat = models.ForeignKey(BookCat, on_delete=models.CASCADE)
    distribution_expenses = models.IntegerField()
    book_image = models.ImageField(upload_to='images')
    book_num = models.IntegerField(default=1)
    
    def __str__(self):
        return self.book_name
    
    
    
