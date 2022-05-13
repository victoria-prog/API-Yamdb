import datetime as dt
from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import Category, Genre, MyUser, Review, Title, Comment


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'confirmation_code': {'write_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    rating = serializers.FloatField(required=False)
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'author', 'name', 'description',
            'year', 'category', 'genres', 'rating'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'genres', 'category'
        )

    def validate_year(self, value):
        print(dt.date.today().year)
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Please, enter a valid year',
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date'
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
