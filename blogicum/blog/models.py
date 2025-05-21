from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AbsctractModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True)
    created_at = models.DateTimeField(
        'Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(AbsctractModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        max_length=64,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL;'
                   ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
                   ),
        unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(AbsctractModel):
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(AbsctractModel):
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем'
                   ' — можно делать отложенные публикации.'))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Автор публикации')
    location = models.ForeignKey(
        Location, blank=True, on_delete=models.SET_NULL, null=True,
        related_name='blog_posts',
        verbose_name='Местоположение')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='blog_posts',
        verbose_name='Категория')
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comment.count()


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        verbose_name='Заголовок поста',
        on_delete=models.CASCADE,
        related_name='comment',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
