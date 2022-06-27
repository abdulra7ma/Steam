from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from account.models import Follower
from .serializers import FollowerSerializer, ForgotPasswordSerializer, LoginSerializer, RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

User = get_user_model()



class UserAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follower
    serializer_class = FollowerSerializer

    @action(detail=True, methods=('GET'))
    def add_follow(self, request, pk):
        follow = self.get_object()
        user = request.user
        follow_obj, created = Follower.objects.get_or_create(follow=follow, user=user)
        if follow_obj.is_follow == False:
            follow_obj.is_follow = not follow_obj.is_follow
            follow_obj.save()
            return Response('followed')
        else:
            follow_obj = not follow_obj.is_follow
            follow_obj.save()
            return Response('Unfollowed')
    


    
    def follow_create(request, user):
        if Follower.objects.filter(user=request.user, follow=User.objects.get(email=user)).exists():
            return Response('you re already followed')
        elif Follower.objects.get(user=request.user, follow=User.objects.get(email=user)).delete():
            return Response('Unfollowed')
        else:
            Follower.objects.create(user=request.user, follow=User.objects.get(email=user))
        return Response('followed')


    # def profile(request, user=None):
    #     if user is None:
    #         user = request.user
    #     else:
    #         user = get_object_or_404(User, email=user)
    #     if request.user.is_authenticated:
    #         is_followed = Follower.objects.filter(follow=user, user=request.user).exists()
    #     follow = user.followers.all().count()
    #     followers = Follower.objects.filter(follow=user).count()
    #     return followers





class RegistrationView(APIView):
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = '''
                    you have successfully registered,
                    a registration email has been sent to you
                    '''
            return Response(message)
        



class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('your account succefully actiavted', status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logout', status=status.HTTP_200_OK)

class ForgotPassword(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('вам на почту выслано сообщение')


