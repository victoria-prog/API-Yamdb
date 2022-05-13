import imp
from django.contrib import admin
from .models import MyUser, Title, Genre, Category, Review, Comment
from .forms import CustomUserChangeForm, CustomUserCreationForm


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'role')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'year', 'description', 'category', 'pub_date')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'title', 'score')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')
    empty_value_display = '-пусто-'


admin.site.register(MyUser, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)