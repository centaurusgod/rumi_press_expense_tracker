from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
# class BookHandler:


def home_page(request):
    if request.method == "POST":
        action = request.POST["sign_out"]
        if action == "sign_out":
            print("signout clicked")
            logout(request)
            return redirect("user_login")
        return render(request, "index.html")
    if request.user.is_authenticated:
        book_cat = BookCat.objects.all()
        books = Books.objects.all()
        expenses = (
            Books.objects.aggregate(total_expenses=models.Sum("distribution_expenses"))[
                "total_expenses"
            ]
            or 0
        )
        return render(
            request,
            "index.html",
            {
                "book_cat_count": len(book_cat),
                "books_count": len(books),
                "expenses": expenses,
            },
        )
    return redirect("user_login")


def user_login(request):
    if request.method == "POST":
        print("Inside post")
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("Inside login")
                return redirect("home_page")
        except Exception as e:
            print(e)
            print("Some error")

    return render(request, "login.html")


def view_books(request):
     if request.user.is_authenticated:
        books = Books.objects.all()  # Replace this with actual queryset of books
        for book in books:
            print(book.book_name)
            print(book.book_image)
        return render(request, "books.html", {"books": books})
     return redirect("user_login")

def add_books(request):
    if request.user.is_authenticated:
        cat_name = BookCat.objects.values_list("cat_name", flat=True)
        if request.method == "POST":
            book_name = request.POST["book_name"]
            book_cat = request.POST["book_cat"]
            book_num= request.POST["book_num"]
            book_auth_name= request.POST["book_auth_name"]
            distribution_expenses = request.POST["distribution_expenses"]
            #image = request
            print(book_name)
            image_file = request.FILES.get("book_image")
            try:
                book = Books()
                book.book_name=book_name
                
                book_cat_instance = BookCat.objects.get(cat_name=book_cat)
                book.book_cat = book_cat_instance
                
                book.book_num=book_num
                book.book_auth_name = book_auth_name
                book.distribution_expenses = distribution_expenses
                book.book_image=image_file
                book.save()
                return render(request, "add_books.html", {"cat_name": cat_name, 'save_sucess':True})
            except Exception as e:
                print(e)
        return render(request, "add_books.html", {"cat_name": cat_name})
    return redirect("user_login")

def add_book_cat(request):
    cat_name_obj = BookCat.objects.all()
    if request.method=="POST":
        print("sdads")
        cat_name = request.POST['cat_name']
        print(cat_name)
        book_cat_obj = BookCat()
        book_cat_obj.cat_name = cat_name
        try:
            book_cat_obj.save()
        except Exception as e:
            print(e)
    return render(request, 'add_book_cat.html',{'cat_name':cat_name_obj})
