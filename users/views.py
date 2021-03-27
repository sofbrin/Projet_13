from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.views.generic.edit import DeleteView, UpdateView
from django.views.decorators.http import require_http_methods
from django import forms
from django.core.mail import send_mail, EmailMessage
from .models import User
from .forms import RegistrationForm, LoginForm, EmailForm, ForgottenPasswordForm, NewPasswordForm, \
    UpdateEmailForm, ProfileForm, ProfilePicForm, DivErrorList
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            email = form.clean_email()
            form.clean_password2()
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            link = reverse('activate', kwargs={'uidb64': body['uid'], 'token': body['token']})
            subject = 'Activez votre compte My French Platform'
            activate_url = 'http://'+current_site.domain+link

            email_text = 'Bonjour ' + user.first_name + ',\n' \
                         + 'Cliquez sur le lien ci-dessous opur activer votre compte :\n' + activate_url

            email = EmailMessage(subject, email_text, 'myfrenchplatform@gmail.com', [email],)

            email.send(fail_silently=False)

            #messages.add_message(request, messages.INFO, "Vous avez reçu un email pour finaliser l'inscription.")
            messages.info(request, "Vous avez reçu un email pour finaliser l'inscription.", extra_tags='toaster')
            return HttpResponseRedirect(reverse('home'))

    else:
        form = RegistrationForm()

    return render(request, 'users/signup.html', {'form': form, 'page_title': "S'inscrire"})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Vous êtes connecté.', extra_tags='toaster')
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.error(request, "Lien d'activation invalide.Faites une autre demande.", extra_tags='toaster')
        print('Lien invalide, faites une autre demande')
        return HttpResponseRedirect(reverse('signup'))


def login_view(request):
    """ Rendering the connexion form """
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            """email = form.clean_email()
            password = request.POST['password']"""
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #messages.success(request, 'Vous êtes connecté', extra_tags='toaster')
                    return HttpResponseRedirect(reverse('home'))
                else:
                    #messages.add_message(request, messages.ERROR, "Compte désactivé.")
                    return HttpResponseRedirect(reverse('login'))
        messages.add_message(
            request, messages.ERROR, "Oups... email ou mot de passe invalide. "
                                     "Réessayez ou créez un compte.")
        messages.error(request, 'Erreur dans la saisie', extra_tags='toaster')
        return HttpResponseRedirect(reverse('login'))
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form, 'page_title': 'Se connecter'})


def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            #context = { 'email': request.POST }

            current_site = get_current_site(request)
            user = User.objects.filter(email=email)

            if user.exists():#no sending email to existing user

                body = {
                    'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0]),
                }
                link = reverse('reset_password', kwargs={'uidb64': body['uid'], 'token': body['token']})
                subject = 'Redéfinissez votre mot de passe'
                reset_url = 'http://' + current_site.domain + link

                email_text = 'Bonjour,\n' \
                             + 'Cliquez sur le lien ci-dessous pour redéfinir votre mot depasse :\n' + reset_url

                email = EmailMessage(subject, email_text, 'myfrenchplatform@gmail.com', [email], )

                email.send(fail_silently=False)

            messages.success(request, 'Nous vous avons envoyé un email pour redéfinir votre mot de passe')
    else:
        form = EmailForm()

    return render(request, 'users/link_to_reset_password.html', {'form': form, 'page_title': "Mot de passe oublié"})


def reset_forgotten_password(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            form = ForgottenPasswordForm(user=user, data=request.POST, error_class=DivErrorList)
            if form.is_valid():
                form.clean_password2()
                form.save()
                update_session_auth_hash(request, form.user)

                user.is_active = True
                user.reset_password = False
                user.save()
                login(request, user)

                #messages.success(request, 'Vous êtes connecté.', extra_tags='toaster')
                messages.success(request, 'Votre mot de passe a bien été changé')
                return HttpResponseRedirect(reverse('home'))
            else:
                context = {'form': form, 'uid': uidb64, 'token': token}
                messages.error(request, 'Corriger l\'erreur')
                return render(request, 'users/reset_password.html', context)
        else:
            #messages.error(request, "L'email n'est pas valide.", extra_tags='toaster')
            messages.warning(request, 'Lien invalide, faites une autre demande')
            #return HttpResponseRedirect(reverse('reset_password'))

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        context = {'form': ForgottenPasswordForm(user),
                    'uid': uidb64,
                    'token': token
                    }
        print('Lien déjà utilisé')
        return render(request, 'users/reset_password.html', context)
    else:
        print('lien invalide')
        messages.warning(request, 'Lien invalide, faites une autre demande')
    return redirect('home')


def logout_view(request):
    """ Loging out function """
    logout(request)
    messages.success(request, 'Vous êtes déconnecté', extra_tags='toaster')
    return HttpResponseRedirect(reverse('home'))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = NewPasswordForm(user=request.user, data=request.POST, error_class=DivErrorList)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Corriger l\'erreur')
    else:
        form = NewPasswordForm(request.user)
    return render(request, 'users/change_password.html', {'form': form, 'page_title': 'Changer le mot de passe'})


class UserEditView(UpdateView):
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('edit_profile')

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data()
        page_title = 'Profil'
        context['page_title'] = page_title
        return context

    def get_object(self):
        return self.request.user


class UserAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwarg):
        context = super(UserAccountDeleteView, self).get_context_data()
        page_title = 'Supprimer le compte'
        context['page_title'] = page_title
        return context

    def get_object(self):
        return self.request.user


@login_required
def edit_profile_pic(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('edit_profile_pic'))
    else:
        form = ProfilePicForm(instance=request.user)
    context = {'form': form, 'page_title': 'Photo de Profil'}
    return render(request, 'users/edit_profile_pic.html', context)


@login_required
def update_email(request):
    if request.method == 'POST':
        form = UpdateEmailForm(user=request.user, data=request.POST)
        if form.is_valid:
            form.clean_email()
            form.save()
            messages.add_message(request, messages.SUCCESS, "Votre email a été changé")
            return HttpResponseRedirect(reverse('update_email'))
    else:
        form = UpdateEmailForm(user=request.user)
    context = {'form': form, 'page_title': 'Changer email'}
    return render(request, 'users/update_email.html', context)







"""@login_required
def update_email(request):
    if request.method == 'POST':
        form = UpdateEmailForm(request.POST)"""


"""@login_required
def edit_profile(request):
    user = User.objects.get(pk=request.user.pk)
    #form = ProfileForm(instance=user)
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect(reverse('edit_profile'))
        else:
            form = ProfileForm(instance=request.user)
        context = {'form': form, 'page_title': 'Profil'}
        return render(request, 'users/edit_profile.html', context)
    else:
        messages.error(request, 'Vous n\'êtes pas autorisé ici.')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('edit_profile_page'))
    else:
        form = ProfileForm(instance=request.user)
    context = {'form': form, 'page_title': 'Profil'}
    return render(request, 'users/edit_profile.html', context)"""

"""def login_view(request):

    print('LOGIN 0')
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=DivErrorList)
        print('LOGIN 1')
        if form.is_valid():
            print('LOGIN 2')
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            print('LOGIN 3')
            if user is not None:
                print('LOGIN 4')
                if user.is_active:
                    print('LOGIN 5')
                    login(request, user)
                    #messages.success(request, 'Vous êtes connecté', extra_tags='toaster')
                    return HttpResponseRedirect(reverse('home'))
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
        return render(request, 'users/login.html', {'form': form, 'page_title': 'Se connecter'})"""







