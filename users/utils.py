from django.contrib.auth import get_user_model
from steam.celery import app
from django.core.mail import send_mail



User = get_user_model()

    

def set_activation_code(user):
    code = user.generate_activation_code()
    if User.objects.filter(activation_code=code).exists():
        user.set_activation_code()
    else:
        user.activation_code = code
        user.save()

    # user.activation_code = code
    # user.save()
    # send_activation_email(user)
        

@app.task
def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/account/activate/{activation_code}/'
    message = f'''
            Thank you for signing up
            Please activate your account
            follow this link {activation_url}
    '''

    send_mail(
        "Activate",
        message,
        'test@gmail.com',
        [email,],
        fail_silently=False
    )
    

@app.task
def send_login(email):
    login_url = f'http://localhost:8000/account/login/'
    message = f'you re logged in{login_url}'

    send_mail(
        'Login',
        message,
        [email,],
        fail_silently=False
    )