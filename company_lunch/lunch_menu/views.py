from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MealMenu
from .token_serializers import MenuTokenObtainPairSerializer
from .serializers import RegisterSerializer, MenuSerializer, UserSerializer, CreateMenuSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generating jwt token
        token_serializer = MenuTokenObtainPairSerializer()
        refresh = token_serializer.get_token(user)
        access_token = str(refresh.access_token)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "access": access_token,
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class GetMenusAPIView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
        return MealMenu.objects.filter(upload_date__range=(start_of_day, end_of_day))


class CreateMenuAPIView(generics.CreateAPIView):
    serializer_class = CreateMenuSerializer
    queryset = MealMenu.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.user_type != 'restaurant':
            return Response({"error": "Only users identified as restaurants can create menus."},
                            status=status.HTTP_403_FORBIDDEN)

        request_data = request.data.copy()
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetMenuByIdAPIView(generics.RetrieveAPIView):
    serializer_class = MenuSerializer
    queryset = MealMenu.objects.all()


class VoteForMenuAPIView(generics.UpdateAPIView):
    serializer_class = MenuSerializer
    queryset = MealMenu.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_type != 'employee':
            return Response({"error": "Only users identified as employee can vote for menus."},
                            status=status.HTTP_403_FORBIDDEN)

        menu = MealMenu.objects.get(id=kwargs['pk'])

        if menu.votes.filter(id=user.id).exists():
            menu.votes.remove(user)
            return Response({'message': 'unliked'}, status.HTTP_200_OK)
        else:
            menu.votes.add(user)
            return Response({'message': 'liked'}, status.HTTP_200_OK)


class WinningMenuAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()

        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

        # Get the menu with the highest number of votes
        menu = MealMenu.objects.filter(upload_date__range=(start_of_day, end_of_day)).annotate(
            vote_count=Count('votes')).order_by('-vote_count').first()

        if menu is not None:
            serializer = MenuSerializer(menu)
            return Response(serializer.data)
        else:
            return Response({'message': 'No menus available.'}, status=status.HTTP_404_NOT_FOUND)


class GetTopMenusAPIView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
        return MealMenu.objects.filter(upload_date__range=(start_of_day, end_of_day)).annotate(
            vote_count=Count('votes')).order_by('-vote_count')
