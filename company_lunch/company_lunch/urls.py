from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from lunch_menu.views import RegisterAPI, GetMenusAPIView, CreateMenuAPIView, GetMenuByIdAPIView, VoteForMenuAPIView, \
    WinningMenuAPIView, GetTopMenusAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterAPI.as_view()),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/menu/', GetMenusAPIView.as_view()),
    path('api/menu/create/', CreateMenuAPIView.as_view()),
    path('api/menu/<int:pk>/', GetMenuByIdAPIView.as_view()),
    path('api/menu/vote/<int:pk>/', VoteForMenuAPIView.as_view()),
    path('api/menu/win/', WinningMenuAPIView.as_view()),
    path('api/menu/top/', GetTopMenusAPIView.as_view())
]