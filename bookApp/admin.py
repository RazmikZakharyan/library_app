from django.contrib import admin
from .models import Book, Author, Genre


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'title', 'photo')
    list_display_links = ('ISBN', 'title')
    fields = ('title', 'slug', 'published', 'pages', 'pdf', 'book_excerpt', 'authors', 'genres', 'image', 'photo')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['photo']
    save_as = True

    def thumbnail_preview(self, obj):
        return obj.photo()

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

    class Meta:
        model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'photo')
    list_display_links = ('id', 'full_name')
    fields = ('full_name', 'slug', 'info', 'avatar', 'photo')
    prepopulated_fields = {"slug": ("full_name",)}
    readonly_fields = ['photo']
    save_as = True

    def thumbnail_preview(self, obj):
        return obj.photo()

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

    class Meta:
        model = Author


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    save_as = True

    class Meta:
        model = Genre
