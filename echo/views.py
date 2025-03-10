from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomAuthenticationForm, CustomUserCreationForm, BookForm
from .models import Book


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form' : form})


def book_list(request):
    books = Book.objects.all()
    
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'page_obj' : page_obj})


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BookForm()
    return render(request, 'book_add.html', {'form' : form})

@login_required
@user_passes_test(lambda user: user.role == 'admin')
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BookForm(instance=book)

    return render(request, 'book_edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.role == 'admin')
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
 
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Книга успешно удалена.")
    
    return redirect('book_list')
