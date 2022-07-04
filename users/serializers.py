from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import Expenses, Follower
from .utils import send_activation_email, set_activation_code
# from djmoney.contrib.django_rest_framework import MoneyField

User = get_user_model()


#USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
        ),
        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followers'] = instance.followers.all()
        return representation



#FOLLOWERS
class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followers'] = instance.followers.all()
        return representation




#REGISTRATION    
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User already exist')
        return email

    
    def validate(self, validated_data):
        password1 = validated_data.get('password')
        password2 = validated_data.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('passwords do not match')
        return validated_data   


    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('passowrd')
        print('asdasd')
        user = User.objects.create_user(email, password)
        print(user, '1231231238129083182038')
        send_activation_email.delay(user.email, user.activation_code)
        return user


    # def save(self):
    #     print('HELOOOOOOO')
    #     data = self.validated_data
    #     user = User.objects.create_user(**data)
    #     user.set_activation_code()
    #     user.send_activation_email()
    #     return user
    



#ACTIVATION
class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(min_length=8, max_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')

        if not User.objects.filter(email=email, activation_code=activation_code).exists():
            raise serializers.ValidationError('User not found')
        return attrs

    
    def save(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()





  

#LOGIN
class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, max_length=8)


    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Ivnvalid passowrd')
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs


#FORGOT PASSWORD
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.set_activation_code()
        user.send_verification_email()


#CHANGE PASSWORD
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context.get['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Your old password was entered incorrectly.Please enter it again')
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': ("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    
    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user



class MoneySerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = ('id', 'amount', 'amount_currency')


