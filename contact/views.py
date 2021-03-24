from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.core.mail import send_mail


def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message'] #+ email
            from_email = email
            recipients = ['myfrenchplatform@gmail.com']
            try:
                send_mail(subject, message, from_email, recipients)
            except BadHeaderError:
                print('invalid header found')
                return HttpResponse('Invalid header found')
            print('cool, it worked')
            return render(request, 'contact/contact.html', {'name': name})
    print('render form')
    return render(request, 'contact/contact.html', {'form': form, 'page_title': 'Contact'})


