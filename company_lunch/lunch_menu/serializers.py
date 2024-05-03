from rest_framework import serializers
from .models import MealMenu, MenuUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuUser
        fields = ('id', 'username', 'name', 'user_type')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuUser
        fields = ('id', 'username', 'password', 'name', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MenuUser.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password'],
                                            name=validated_data['name'],
                                            user_type=validated_data['user_type'])
        return user

class MenuSerializer(serializers.ModelSerializer):
    count_of_votes = serializers.SerializerMethodField()

    class Meta:
        model = MealMenu
        fields = '__all__'

    def get_count_of_votes(self, obj):
        # this method returns the count of votes for each menu
        return obj.votes.count()

class CreateMenuSerializer(MenuSerializer):
    class Meta(MenuSerializer.Meta):
        fields = ['name', 'description', 'menu_content', 'price']

    def save(self, **kwargs):
        self.validated_data['restaurant'] = self.context['request'].user
        return super().save(**kwargs)

