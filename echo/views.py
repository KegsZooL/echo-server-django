from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomAuthenticationForm, CustomUserCreationForm, BookForm, CustomUserForm
from .models import Book, CartItem, Order, OrderItem

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
    cart_items = CartItem.objects.filter(user=request.user)
    
    cart_books = {item.book.id: item.quantity for item in cart_items}
    
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'page_obj' : page_obj, 'cart_books': cart_books})


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

@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения успешно сохранены!")
            return redirect('user_profile')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'user_profile.html', {'form': form})


@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    referer = request.META.get('HTTP_REFERER', '')
    if 'cart' in referer:
        return redirect('cart')
    
    return redirect(referer)

@login_required
def remove_from_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item = CartItem.objects.filter(user=request.user, book=book).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    referer = request.META.get('HTTP_REFERER', '')
    if 'cart' in referer:
        return redirect('cart')
    
    return redirect(referer)

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', { 'cart_items': cart_items, 'total_price': total_price })

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Ваша корзина пуста")
        return redirect('cart')

    order = Order.objects.create(user=request.user)

    for item in cart_items:
        OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)

    order.calculate_total_price()
    cart_items.delete()

    messages.success(request, "Заказ успешно оформлен!")
    return redirect('cart') 

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})
