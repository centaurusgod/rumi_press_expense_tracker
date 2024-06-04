import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import F, Sum

# Create your views here.
# class BookHandler:
# def calculate_total_expenses(request):
#     total_expenses = Books.objects.annotate(
#         total_book_expenses=F('distribution_expenses') * F('book_num')
#     ).aggregate(total_expenses=Sum('total_book_expenses'))['total_expenses'] or 0
#     return total_expenses

def home_page(request):
    if request.method == "POST":
        action = request.POST["sign_out"]
        if action == "sign_out":
            print("signout clicked")
            logout(request)
            return redirect("user_login")
        return render(request, "index.html")
    if request.user.is_authenticated:
        expenses=0
        book_cat_items=[]
        book_cat_item_expenses=[]
        book_items =[]
        
        book_cat = BookCat.objects.order_by('cat_name')
        books =  Books.objects.select_related('book_cat').order_by('book_cat__cat_name')
        
        for cat in book_cat:
            book_cat_items.append(cat.cat_name)
        
        
        # for book in books:
        #     book_items.append(book.book_name)
        #     print(book.book_cat)
        for price in books:
            expense_per_cat = price.book_num*price.distribution_expenses
            expenses = expenses+expense_per_cat
            book_cat_item_expenses.append(expense_per_cat)
            print(expense_per_cat)
        #print(book_cat_items)
        #print(expense_per_cat)
            
        return render(
            request,
            "index.html",
            {
                "book_cat": book_cat,
                "books": books,
                "expenses": expenses,
                'book_items':json.dumps(book_items),
                'book_cat_items':json.dumps(book_cat_items),
                'book_cat_item_expenses':json.dumps(book_cat_item_expenses),
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
    try:
        if request.method == "POST":
            cat_name_add = request.POST.get('cat_name_add')
            cat_id = request.POST.get('cat_id')
            
            if cat_name_add:
                print(cat_name_add)
                book_cat_obj = BookCat()
                book_cat_obj.cat_name = cat_name_add
                book_cat_obj.save()

            elif cat_id:
                print(cat_id)
                book_cat = get_object_or_404(BookCat, id=cat_id)
                book_cat.delete()
                
        cat_name_obj = BookCat.objects.all()
    except Exception as e:
        print(e)
        cat_name_obj = None  # Assigning a default value if an exception occurs
    
    return render(request, 'add_book_cat.html', {'cat_name': cat_name_obj})