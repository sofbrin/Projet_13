from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.utils import ErrorList
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="formerrors">%s</p>' % e for e in self])


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        }
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            #'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            #'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'}),
        }
        error_messages = {
            'email': {
                'invalid': _("Oups, l'adresse email n'est pas valide.")
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError("Oups... email déjà pris. Soit vous avez déjà un compte, soit vous vous trompez d'email !")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if len(password1) < 8:
            raise forms.ValidationError('Trop court ! Essayez avec 8 caractères minimum :)')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
        #user = User.objects.create_user(
            #self.cleaned_data['first_name'],
            #self.cleaned_data['last_name'],
            #self.cleaned_data['email'],
            #self.cleaned_data['password1'])
        #return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email ici'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe ici'
        }
    ))

    """class Meta:
        model = User
        error_messages = {
            'invalid_email': _("Oups, l'email n'est pas valide."),
            'invalid_password': _("Le mot de passe n'est pas correct")
        }

    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        if User.objects.filter(email=new_email):
            raise forms.ValidationError(
                "Oups... email déjà pris. Soit vous avez déjà un compte, soit vous vous trompez d'email !")
        if not new_email.is_valid:
            raise forms.ValidationError("Oups... Cet email n'est pas valide")
        return new_email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not """


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email ici'
        }
    ))


class ForgottenPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        }
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        }
    ))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        """error_messages = {
            'password2': {
                'password_too_short': _("Mot de passe trop court. Il vaut mieux en essayer un autre..."),
                'password_too_common': _("Ce mot de passe est trop commun. Ce serait plus sûr d'en trouver un autre..."),
                'password_too_similar': _("Ce mot de passe est trop commun. Ce serait plus sûr d'en trouver un autre...")
            }
        }"""

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user


class NewPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe actuel'
        }
    ))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        }
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        }
    ))

    class Meta:
        model = User
        fields =['old_password', 'new_password1', 'new_password2']
        error_messages = {
            'password2': {
                'password_too_short': _("Mot de passe trop court. Il vaut mieux en essayer un autre..."),
                'password_too_common': _("Ce mot de passe est trop commun. Ce serait plus sûr d'en trouver un autre..."),
                'password_too_similar': _("Ce mot de passe est trop commun. Ce serait plus sûr d'en trouver un autre...")
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user


"""class UpdatePicForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_pic',)


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'city', 'country', 'bio', 'profile_pic')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Petite bio'}),
        }"""


class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe pour confirmer'})
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateEmailForm, self).__init__(*args, **kwargs)
        print('toto')

    def clean_email(self):
        print('toto 1')
        email = self.cleaned_data.get('email')
        print(email)
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("Oups... cet email est déjà utilisé !")
        """if not email.is_valid:
            raise forms.ValidationError("Oups... Cet email n'est pas valide")"""
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError("Mot de passe incorrect")
        return password

    def save(self, commit=True):
        email = self.cleaned_data['email']
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'city', 'country', 'bio', 'profile_pic')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Petite bio'}),

        }


class ProfilePicForm(forms.ModelForm):
    profile_pic = forms.ImageField(label=_(''), required=False) #, widget=forms.FileInput)

    class Meta:
        model = User
        fields = ('profile_pic',)


class UserAccountDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'city', 'country', 'bio', 'profile_pic')


