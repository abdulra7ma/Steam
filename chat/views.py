from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, UserProfile
from chat.serializers import MessageSerializer, UserSerializer


User =get_user_model()

def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method =='POST':
        email, password = request.POST['email'],  request.POST['password']
        user= authenticate(email=email, password=password)
        print(user)
        if user is None:
            login(request,user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')


@csrf_exempt
def user_list(request, pk=None):
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context = {'request':request})
        return JsonResponse(serializer.data, safe=False)

    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(email=data['email'], password=data['password'])
            UserProfile.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error':"something went wrong"}, status=400)


def message_list(request, sender=None, receiver=None):

    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(message, many=True, context={'request':request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


def register_view(request):

    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': request.user.email})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    
    else:
        # request.method == 'GET':
        return render(request, 'chat/messages.html',
                {'users': request.user.email,
                            'receiver': User.objects.get(id=receiver),
                            'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                        Message.objects.filter(sender_id=receiver, receiver_id=sender)})


