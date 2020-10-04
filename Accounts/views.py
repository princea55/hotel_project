from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import SignupUser, LoginUser
from django.contrib.auth import authenticate, login as Login, logout as Logout
from .models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
# Create your views here.


def home(request):
    return render(request, 'accounts/home.html')


def login(request):
    if request.method == "POST":
        forms = LoginUser(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']

            user = authenticate(username=username, password=password)
            get_user = User.objects.get(username=username)
            # print(get_user)
            # print(get_user.contact)
            if user:
                Login(request, user)
                context = {
                    "user": user,
                }
                return redirect('dashboard')
            else:
                return HttpResponse("invalid user")
        else:
            print("invalid form")
            return render(request, 'accounts/login.html', {"forms": forms})

    else:
        forms = LoginUser()
        return render(request, 'accounts/login.html', {"forms": forms})
    return render(request, 'accounts/login.html', {"forms": forms})


# def signup(request):
#     if request.method == "POST":
#         form = SignupUser(request.POST, request.FILES)
#         if form.is_valid():
#             # form.cleaned_data['username']s

#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             email = form.cleaned_data['email']
#             contact = form.cleaned_data['contact']

#             create_user = User.objects.create_user(username=username, email=email, contact=contact, image=image,password=password)
#             create_user.save()
#             get_user = User.objects.get(username=username)
#             htmly = get_template('accounts/email.html')
#             d  = {'username':username}
#             subject, from_email, to = "Welcome","princesuriya14@gmail.com",email
#             html_content = htmly.render(d)
#             msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()

#             user = authenticate(username=username, password=password)
#             Login(request, user)
#             context = {
#                 "user":user,
#                 "get_user":get_user
#             }

#             return render(request, 'accounts/dashboard.html', context)
#         else:
#             print("error in valid data")
#             return render(request, 'accounts/signup.html', {"form": form})

#     else:
#         form = SignupUser()
#         return render(request, 'accounts/signup.html', {"form": form})
#     return render(request, 'accounts/signup.html', {"form": form})

def signup(request):
    if request.method == 'POST':
        form = SignupUser(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            contact = form.cleaned_data['contact']
            user = User.objects.create_user(first_name=firstname, last_name=lastname,
                                            username=username, email=email, contact=contact, password=password1)
            # user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('accounts/account_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration.')
            return render(request, 'accounts/account_active_sent.html')
        else:
            print("error in valid data")
            return render(request, 'accounts/signup.html', {"form": form})
    else:
        form = SignupUser()
        return render(request, 'accounts/signup.html', {'form': form})
    return render(request, 'accounts/signup.html', {"form": form})


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            reset_email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=reset_email)
            user_id = associated_users[0].id
            if associated_users is not None:
                current_site = get_current_site(request)
                message = render_to_string('accounts/password_reset_sent_email.html',
                                           {
                                               'user': associated_users[0],
                                               'domain': current_site.domain,
                                               'uid': urlsafe_base64_encode(force_bytes(user_id)),
                                               'token': default_token_generator.make_token(associated_users[0])
                                           })
                mail_subject = "password Reset Requested"
                email = EmailMessage(mail_subject, message, to=[reset_email])
                email.send()
                return render(request, 'accounts/password_reset_done.html')
            else:
                return HttpResponse("Invlid Email")
        else:
            return render(request, "accounts/password_reset.html", {"password_reset_form": password_reset_form})
    else:
        password_reset_form = PasswordResetForm()
        return render(request, "accounts/password_reset.html", {"password_reset_form": password_reset_form})
    return render(request, "accounts/password_reset.html", {"password_reset_form": password_reset_form})


def update(request, pk):
    obj = get_object_or_404(User, id=pk)
    forms = SignupUser(request.POST or None, instance=obj)
    if request.method == "POST":
        print("POST method")
        if forms.is_valid():
            forms.save()
            return HttpResponse("Updated succesfully")
        return render(request, "accounts/update.html", {"forms": forms})
    else:
        form = SignupUser(instance=obj)
        return render(request, 'accounts/update.html', {"forms": form})
    return render(request, 'accounts/update.html', {"forms": forms})


def dashboard(request):
    # try:
    #     get_user = User.objects.get(username=request.user.username)
    # except:
    #     return render(request, 'accounts/dashboard.html')
    # context = {
    #     "get_user":get_user
    # }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    Logout(request)
    return redirect('login')
