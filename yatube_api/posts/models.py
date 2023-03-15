from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

MAX_LENGHT = 200


class Group(models.Model):
    '''Модель создания групп постов.'''
    title = models.CharField(
        max_length=MAX_LENGHT,
        verbose_name='Название группы',
        help_text='Введите название тематической группы',
    )
    slug = models.SlugField(
        max_length=MAX_LENGHT,
        unique=True,
        verbose_name='Номер группы',
        help_text='Укажите порядковый номер группы',
    )
    description = models.TextField(
        max_length=MAX_LENGHT,
        verbose_name='Описание группы',
        help_text='Добавьте текст описания группы',
    )

    class Meta:
        ordering = ('-title',)
        verbose_name = 'Группа статей'
        verbose_name_plural = 'Группы статей'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    '''Модель создания постов пользователей.'''
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.text


class Comment(models.Model):
    '''Модель создания комментариев пользователей к постам.'''
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    '''Модель создания подписок пользователей.'''
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Укажите подписчика',
        help_text='Подписчик',
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Укажите на кого подписываемся',
        help_text='Автор поста',
    )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                name='unique_follow',
                fields=('user', 'following')
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} follows {self.following}'
