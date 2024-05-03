from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MenuTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claim
        token['user_type'] = user.user_type

        return token