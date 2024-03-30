from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password']

        extra_kwargs = {'password': {'write_only':True, 'required':True}
                        }
    def create(self, validated_data):
            user = CustomUser.objects.create_user(
                validated_data['email'],
                validated_data['username'],
                validated_data['password']
            )
            user.save()
            return user
        
    def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                if attr == 'password':
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)
            instance.save()
            return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    '''
    Handles password reset request
    '''
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    '''
    Handles actual password reset operation
    '''
    new_password = serializers.CharField(style={'input_type':'password'})
    re_password = serializers.CharField(style={'input_type':'password'})
