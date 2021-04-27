from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from uuid import uuid3, NAMESPACE_DNS


class Book(models.Model):
    ISBN = models.CharField(max_length=37, primary_key=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50)
    published = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField()
    image = models.ImageField(upload_to='photos')
    pdf = models.FileField(upload_to='PDF')
    book_excerpt = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField('Author', related_name='book', blank=True)
    genres = models.ManyToManyField('Genre', related_name='book')

    def __str__(self):
        return '{}'.format(self.title)

    def get_img(self):
        if not self.image:
            return '-'
        return self.image.url

    def photo(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_img())

    def save(self, *args, **kwargs):
        self.ISBN = uuid3(NAMESPACE_DNS, f'{self.title}{self.pages}{self.published}')
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_single', args=[self.slug])

    class Meta:
        verbose_name_plural = "Books"
        ordering = ["title"]


class Author(models.Model):
    full_name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='Photos/%Y/%d', null=True, blank=True)
    info = models.TextField(null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return '{}'.format(self.full_name)

    def get_img(self):
        if not self.avatar:
            return '-'
        return self.avatar.url

    def photo(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_img())

    def get_absolute_url(self):
        return reverse('author', args=[self.slug])

    class Meta:
        verbose_name_plural = "Authors"
        ordering = ["full_name"]


class Genre(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('genre', args=[self.slug])

    class Meta:
        verbose_name_plural = "Genres"
        ordering = ["title"]
