from functools import partial
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Avg
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import AuthenticatedOrReadOnly, IsAdminOrReadOnly, IsAdmin
from .tokens import account_activation_token
from .models import MyUser, Review, Title, Comment, Genre, Category
from .serializers import (
    UserSerializer, TitleReadSerializer,
    TitleCreateSerializer, ReviewSerializer, CommentSerializer,
    GenreSerializer, CategorySerializer
)


@api_view(['POST'])
def sign_up(request):
    email = request.data.get('email')
    username = request.data.get('username')
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        new_user = get_object_or_404(MyUser, email=email, username=username)
        code = account_activation_token.make_token(new_user)
        new_user.confirmation_code = code
        new_user.save()
        send_mail(
            'Your confirmation code',
            f'your confirmation code is {code}',
            'kolomietsvvv@gmail.com',
            [email],
            fail_silently=False
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_token(request):
    code = request.data.get('confirmation_code')
    username = request.data.get('username')
    if (code is None) or (username is None):
        return Response('username and confirmation code are required', status=status.HTTP_400_BAD_REQUEST)
    user = MyUser.objects.filter(confirmation_code=code, username=username).first()
    if not user:
        return Response('Confirmation code or username does not exists', status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (AuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return TitleCreateSerializer
        return TitleReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permision_classes = (AuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = Review.objects.filter(title=title_id)
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments = Comment.objects.filter(review=review_id)
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug',)
    pagination_class = PageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        current_user = get_object_or_404(MyUser, email=request.user.email)
        if request.method == 'GET':
            serializer = UserSerializer(current_user)
        elif request.method == 'PATCH':
            serializer = UserSerializer(
                current_user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
