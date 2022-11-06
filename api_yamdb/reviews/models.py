from tabnanny import verbose
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User #даша - импортнула юзера, дабы без ошибок было


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории'
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведения (база)"""
    name = models.CharField(
        max_length=256, 
        verbose_name='Название',
        help_text='Введите название',
    )
    #поле year не обязательное, думаю, тут нужна валидация, но позже
    year = models.IntegerField(
        null=True,
        blank=True, 
        verbose_name='Год',
        help_text='Введите год релиза',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения',
        help_text='Введите описание',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True,
        help_text='Введите категорию произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        verbose_name='Жанр',
        help_text='Введите жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
    
    def __str__(self):
        return self.name
        

class Review(models.Model):
    """Отзывы."""
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Напишите отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name='Название',
    )
    score = models.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        verbose_name="Оценка",
        help_text='Введите оценку'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации отзыва"
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев"""
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Отзыв',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации коммента",
        help_text='Дата публикации коммента'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментраии'
        
    def __str__(self):
        return self.text
