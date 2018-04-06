from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

__all__ = (
    'UserSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    password = serializers.CharField(min_length=5)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)
    img_profile = serializers.ImageField(allow_empty_file=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['username'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            img_profile=validated_data['img_profile'],
        )
        return user

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'img_profile',
        ]


