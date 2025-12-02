from django.db import models
from django.urls import reverse  # Для создания URL по ID объекта
from django.contrib.auth.models import User
from datetime import date
import uuid  # Для уникальных экземпляров книг


class Genre(models.Model):
    """Модель, представляющая жанр книги (например, фантастика, поэзия)."""
    name = models.CharField(max_length=200, help_text="Введите жанр книги (например, Научная фантастика)")

    def __str__(self):
        """Строковое представление модели."""
        return self.name


class Book(models.Model):
    """Модель, представляющая книгу (но не конкретный экземпляр)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")

    def __str__(self):
        """Строковое представление модели."""
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для доступа к деталям конкретной книги."""
        return reverse('book-detail', args=[str(self.id)])
   
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Модель, представляющая конкретный экземпляр книги, находящийся в библиотеке."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для конкретной книги")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Доступность книги',
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False

class Meta:
    ordering = ['due_back']
    permissions = (("can_mark_returned", "Set book as returned"),)


    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """Строковое представление модели."""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        """Проверяет, просрочен ли срок возврата."""
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """Модель, представляющая автора книги."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """Возвращает URL для доступа к деталям автора."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Строковое представление модели."""
        return f'{self.last_name}, {self.first_name}'
