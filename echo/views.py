from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .forms import CustomUserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
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


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books' : books})

@login_required
def book_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        Book.objects.create(title = title, author = author, price = price)
        return redirect('/')
    return render(request, 'book_add.html')

@login_required
@user_passes_test(lambda user: user.role == 'admin')
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.price = request.POST['price']
        book.save()
        return redirect('/')
    return render(request, 'book_edit.html', {'book' : book})


@login_required
@user_passes_test(lambda user: user.role == 'admin')
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.user.role != 'admin':
        messages.error(request, "У вас нет прав для удаления этой книги.")

    if request.method == 'POST':
        book.delete()
        messages.success(request, "Книга успешно удалена.")

    return redirect(request, 'book_list', {'book' : book})


def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('book_list')
