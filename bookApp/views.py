import os
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from .models import Book, Genre, Author
from random import randint
from wsgiref.util import FileWrapper


class BookListView(ListView):
    model = Book
    slug_url_kwarg = 'genre_slug'
    paginate_by = 12

    def get_queryset(self):
        return Book.objects.filter(genres__slug=self.kwargs.get('genre_slug')).select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = Genre.objects.get(slug=self.kwargs.get('genre_slug'))

        return context


class BookDetailView(DetailView):
    model = Book
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.filter(genres__slug=context['book'].genres.first().slug)
        rand = randint(0, len(books) - 6 if 0 < len(books) - 6 else 1)
        context['books'] = books[rand:rand + 6]

        return context


class AuthorDetailView(DetailView):
    model = Author
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.filter(authors__slug=self.kwargs.get('author_slug'))
        context['books'] = books

        return context


class SearchView(ListView):
    template_name = 'bookApp/book_list.html'
    slug_url_kwarg = 'search_slug'
    context_object_name = 'book_list'
    paginate_by = 12

    def get_queryset(self):
        try:
            books = Book.objects.filter(title__icontains=self.request.GET.get('s'))
        except ValueError:
            raise Http404()
        return books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class HomeView(ListView):
    model = Book
    paginate_by = 12


class PDFView(View):

    def get(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(slug=self.kwargs.get('book_slug'))
        except Exception:
            raise Http404()
        if request.GET.get('read'):
            with open(f'media/{book.pdf}', 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'filename=some_file.pdf'
                return response
        elif request.GET.get('download'):
            if request.user.is_authenticated:
                filename = open(f'media/{book.pdf}', 'rb')
                content = FileWrapper(filename)
                response = HttpResponse(content, content_type='application/pdf')
                response['Content-Length'] = os.path.getsize(f'media/{book.pdf}')
                response['Content-Disposition'] = 'attachment; filename=%s' % book.pdf
                return response
            return redirect('login')
        raise Http404()
