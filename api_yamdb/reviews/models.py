from django.db import models


class Category(models.Model):
    """Категории произведений"""
    name = models.CharField(
        max_length=250,
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
        max_length=250,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
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
        max_length=250, 
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
        db_index=True
    )

    class Meta:
        verbose_name = 'Произведение'
    
    def __str__(self):
        return self.name
