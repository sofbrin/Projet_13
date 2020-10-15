from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import loader
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import User
from .forms import RegistrationForm, LoginForm, DivErrorList
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    """ Rendering the registration form """
    if request.method == 'POST':
        form = RegistrationForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            email = form.clean_email()
            form.clean_password2()
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte PurBeurre'
            message = render_to_string('users/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = EmailMessage(mail_subject, message, to=[email])
            to_email.send()
            messages.add_message(request, messages.INFO, "Vous avez reçu un email pour finaliser l'inscription.")
            #messages.info(request, "Vous avez reçu un email pour finaliser l'inscription.", extra_tags='toaster')
            return HttpResponseRedirect(reverse('signup'))

    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #messages.success(request, 'Vous êtes connecté.', extra_tags='toaster')
        return HttpResponseRedirect(reverse('home'))
    else:
        #messages.error(request, "L'email n'est pas valide.", extra_tags='toaster')
        return HttpResponseRedirect(reverse('signup'))


def login_view(request):
    """ Rendering the connexion form """
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #messages.success(request, 'Vous êtes connecté', extra_tags='toaster')
                    url = request.GET.get('next')
                    if not url:
                        url = reverse('home')
                    return HttpResponseRedirect(url)
                else:
                    messages.add_message(request, messages.ERROR, "Compte désactivé.")
                    return HttpResponseRedirect(reverse('login'))
        messages.add_message(
            request, messages.ERROR, "L'email et/ou le mot de passe sont invalides. "
                                     "Veuillez saisir à nouveau vos identifiants ou créer un compte.")
        #messages.error(request, 'Erreur de saisie', extra_tags='toaster')
        return HttpResponseRedirect(reverse('login'))
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """ Loging out function """
    logout(request)
    #messages.success(request, 'Vous êtes déconnecté', extra_tags='toaster')
    return HttpResponseRedirect(reverse('home'))
