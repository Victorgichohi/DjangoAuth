from django.shortcuts import render,redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from core.helpers import NextUrlMixin , RequestFormAttachMixin
from .forms import LoginForm, RegisterForm
from django.views.generic.edit import FormMixin
from .forms import LoginForm, RegisterForm, ReactivateEmailForm, UserDetailChangeForm, TemporaryCodeForm
from .models import EmailActivation
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.core.files.base import ContentFile

''' QR scan imports '''
import qrcode
import logging
import pyotp
import os
from io import StringIO, BytesIO
import settings
from django.core.files import File  # you need this somewhere

# Create your views here.
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    msg = """Your email has already been confirmed
                    """
                    messages.success(request, mark_safe(msg))
                    return redirect("login") 
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user 
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)


class QRview(CreateView):
    form_class = TemporaryCodeForm
    def form_valid(self, form):
        # next_path = self.get_next_url()
        return redirect("/")
    def get(self, request):
        user = self.request.user
        if  user.has_scanned:
            return redirect("/account/verify")
        email = user.get_short_name()
        if user is None:
            return redirect ("login")
        t = pyotp.TOTP(user.OTPkey)
        q = qrcode.make(t.provisioning_uri(email))
        img = BytesIO()
        q.save(img)
        filename = '%s.png' % email

        q.save(settings.MEDIA_ROOT + filename)
        with open(settings.MEDIA_ROOT + filename, "rb") as f:
            data = f.read()
        user.OTPQr.save(filename, ContentFile(data))
        print(user.OTPkey)
        print(t.now())
        user.has_scanned = True
        # print(user.has_scanned)
        context = {'img': user.OTPQr , 'key':user.OTPkey}
        return render(request, 'scanpage.html', context)


''' manage login '''

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    # success_url = '/account/scan/'
    template_name = 'login.html'
    # default_next = '/account/scan/'

    def form_valid(self, form):
        request = self.request
        return redirect("/account/scan")
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

class TemporaryCodeView(RequestFormAttachMixin,FormView):
    form_class = TemporaryCodeForm
    template_name = 'temporaryCode.html'
    success_url = '/'
    def form_valid(self, form):
        # next_path = self.get_next_url()
        return redirect("/")