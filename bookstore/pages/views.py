from django.shortcuts import render
from books.models import Book

def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'pages/index.html', context)
