from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.utils import timezone
import random
from django.http import HttpResponse
from website.models import Userdata, Messages


class Recaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")


def index(request):
    return render(request, 'base.html', {'title_page': 'first'})


def inbox(request):
    return render(request, 'messages.html', {'title_page': 'ההודעות שלי'})


def get_frealancers(request):
    return render(request, 'freelancers.html')


def send_email(toemail, mysubject, mymessage):
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = mysubject
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [toemail, ]
        message = mymessage
        EmailMessage(subject, message, email_from,
                     recipient_list, connection=connection).send()


def send_vaildation_email(email, name, user_id, token):
    mes = f'שלום {name}, \n תודה שנרשמת לאתר! רצינו לוודא שזה באמת המייל שלך מאחר ותוכל להגדיר שאתה מעוניין לקבל הודעות ממשתמשים שיתעניינו בדירות שתפרסם באתר.\n על מנת להשלים את תהליך ההרשמה יש ללחוץ על הקישור המופיע במייל זה. לאחר לחיצה עליו, חשבונך יופעל.\n הקישור: \n{settings.MY_URL}vaild/{user_id}/{token} \n תודה!'
    send_email(email, 'אימות כתובת המייל', mes)


def login_page(request):
    user = request.user
    if user.is_authenticated:
        if user.last_name != '1':
            if request.method == 'GET':
                return render(request, 'login.html', {'title_page': 'Log-in'})
        else:
            return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_authenticated:
                logout(request)
            login(request, user)
            if user.last_name != '1':
                return render(request, 'login.html', {'log': 'נא לאמת את כתובת המייל באמצעות מייל לאימות סיסמא שנשלח אליך בעת ההרשמה', 'title_page': 'Log-in'})
            else:
                return redirect('index')
        else:
            messages.error(request, f"log")
        return render(request, 'login.html', {'username1': username, 'log': 'כנראה הזנת שם משתמש או סיסמא לא נכונים', 'title_page': 'Log-in'})

    next = request.GET.get('next')
    if next:
        mes = ''
        if next == '/rest_password_sent/':
            mes = 'אם המייל שהזנת רשום, נשלח אליך קישור לאיפוס הסיסמא, נא לבדוק בתיבת המייל או בתיבת הודעות הספאם'
        elif next == 'set':
            mes = 'סיסמתך שונתה בהצלחה, ניתן להתחבר'
        return render(request, 'login.html', {'reset': mes, 'title_page': 'Log-in'})
    return render(request, 'login.html', {'title_page': 'Log-in'})


def logout_page(request):
    logout(request)
    return redirect('index')


def vaild_account(request, user_id=0, token=None):
    mes = None
    if request.user:
        if request.user.is_authenticated and request.user.last_name == '1':
            return redirect('index')

    if user_id and token:
        user = User.objects.filter(pk=user_id).all()
        if user:
            user = user[0]
            if user.last_name == token:
                user.last_name = '1'
                user.save()
                mes = 'אימות כתובת המייל הושלמה, ניתן להתחבר כעת'
                if request.user.is_authenticated:
                    return redirect('index')
            elif user.last_name == '1':
                mes = 'נראה שכבר אישרת את כתובת המייל, ניתן להתחבר'
            if mes:
                return render(request, 'login.html', {'reset': mes, 'title_page': 'Log-in'})
    return render(request, 'login.html', {'log': 'שגיאה באימות החשבון', 'title_page': 'Log-in'})

# custom 404 view


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        firstname = request.POST.get('firstname')
        email = request.POST.get('email')
        msg = []
        if username:
            if len(username) < 4:
                msg.append('שם המשתמש צריך להכיל לפחות 4 תווים')
        if User.objects.filter(email=email).all():
            msg.append('מייל זה נמצא בשימוש')
        if User.objects.filter(username=username).all():
            msg.append('שם משתמש זה נמצא בשימוש')
        elif repassword == password and password and username and email and firstname and not msg:
            try:
                options = 'Aa5B1b2C3r4Df5q6E4o7u28F9Q1mRS'
                vaildation = [options[random.randint(
                    0, len(options)-1)] for k in range(16)]
                user = User.objects.create_user(
                    username=username, email=email, first_name=firstname, last_name=''.join(vaildation), password=password)
                user.save()
            except Exception as e:
                msg.append(e)
            user1 = authenticate(request, username=username, password=password)
            if user1:
                login(request, user1)
                send_vaildation_email(
                    user1.email, user1.first_name, user.id, user1.last_name)
                return render(request, 'login.html', {'reset': 'שלחנו לך מייל לאימות כתובת המייל שהזנת, מאחר שתוכל לבחור לקבל מיילים ממתעניינים בדירה נבקש לאשר שזאת כתובת המייל שלך. תודה', 'title_page': 'Log-in'})
        elif repassword != password:
            msg.append('הסיסמאות לא תואמות')
        if not username or not password or not firstname or not firstname or not email:
            msg.append('נא למלא את כל השדות')

        return render(request, 'login.html', {'username2': username, 'email': email, 'firstname': firstname, 'reg': 'reg', 'msg': msg, 'title_page': 'Log-in'})
    return render(request, 'login.html', {'reg': 'reg', 'msg': [], 'title_page': 'Log-in'})


def search(request):
    expertise_to_search = [2]
    query = Userdata.objects.filter(
        userexpertise__id__in=expertise_to_search).distinct()
    return JsonResponse([k.toJSON() for k in query.all()], safe=False)

def myprofile(request):
    return render(request, 'myprofile.html', {'title_page': 'הפרופיל שלי'})
