from django import template

register = template.Library()

@register.filter
def get_item(cart_books, book_id):
    return cart_books.get(book_id, None)

