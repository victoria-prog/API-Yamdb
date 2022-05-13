from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password


CHOICES = (
    ('M', 'moderator'),
    ('U', 'user'),
    ('A', 'admin')

)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=MyUserManager.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(
            email, username, password, role='A', **extra_fields
        )


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=40, unique=True
    )
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=128, choices=CHOICES, default='U')
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=128, blank=True)
    confirmation_code = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=300, blank=True, null=True)
    year = models.IntegerField()
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='titles'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.CharField(max_length=300)
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, 'The score can not be less than 1'),
            MaxValueValidator(10, 'The score can not be higher than 10')
        ]
    )
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:15]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
