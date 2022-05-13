from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

router_v1 = routers.DefaultRouter()

router_v1.register(r'titles', views.TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)
router_v1.register(r'genres', views.GenreViewSet)
router_v1.register(r'categories', views.CategoryViewSet)
router_v1.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', views.sign_up),
    path('v1/auth/token/', views.make_token),
    path('v1/', include(router_v1.urls))
]
