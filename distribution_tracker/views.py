from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
# class BookHandler:
    

def home_page(request):
    if request.method=='POST':
        action = request.POST["sign_out"]
        if action=="sign_out":
            print("signout clicked")
            logout(request)
            return redirect('user_login')
        return render(request, 'index.html')  
    if request.user.is_authenticated:
        book_cat = BookCat.objects.all()
        books = Books.objects.all()
        expenses = Books.objects.aggregate(total_expenses=models.Sum('distribution_expenses'))['total_expenses'] or 0
        return render(request, 'index.html', {'book_cat_count':len(book_cat), 'books_count':len(books), 'expenses':expenses})  
    return redirect('user_login')


def user_login(request):
    if request.method=="POST":
        print("Inside post")
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                 login(request, user)
                 print("Inside login")
                 return redirect('home_page')
        except Exception as e:
            print(e)
            print("Some error")
            
    return render(request, 'login.html')


def view_books(request):
    books = Books.objects.all() # Replace this with actual queryset of books
    for book in books:
        print(book.book_name)
        print(book.book_image)
    return render(request, 'books.html', {'books': books})

def add_books(request):
    cat_name = BookCat.objects.values_list('cat_name', flat=True)
    return render(request, 'add_books.html', {'cat_name':cat_name})
    

# def view_book_cat(request):
    