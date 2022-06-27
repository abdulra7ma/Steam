from django.contrib.auth import get_user_model
from steam.celery import app
from django.core.mail import send_mail

User = get_user_model()

    
@staticmethod
def generate_activation_code():
    from django.utils.crypto import get_random_string
    code = get_random_string(8)
    return code

def set_activation_code(user):
    code = generate_activation_code()
    user.activation_code = code
    user.save()
    send_activation_email(user)
        

@app.task
def send_activation_email(user):
    activation_url = f'http://localhost:8000/account/activate/{user.activation_code}/'
    message = f'''
            Thank you for signing up
            Please activate your account
            follow this link {activation_url}
    '''

    send_mail(
        "Activate",
        message,
        'test@gmail.com',
        [user.email,],
        fail_silently=False
    )
    

@app.task
def send_login(user):
    login_url = f'http://localhost:8000/account/login/'
    message = f'you re logged in{login_url}'

    send_mail(
        'Login',
        message,
        [user.email,],
        fail_silently=False
    )