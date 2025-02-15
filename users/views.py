from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import RegisterForm
from django.views.generic import CreateView, ListView, View
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .services import block_user
from django.shortcuts import redirect, get_object_or_404

# Create your views here.
class UserCreate(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'users/user_form.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Приветствие на сайте',
            message='Поздравляем с успешной регистрацией на сайте',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email,])
        return super().form_valid(form)
    
class UserList(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    context = {}
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('users.manager'):
            return CustomUser.objects.all()
        else:
            raise PermissionDenied

class DetailUser(LoginRequiredMixin, View):
    model = CustomUser
    template_name = 'users/user.html'
    context_object_name = 'custom_user'

    def get_object(self):
        return get_object_or_404(CustomUser)

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object()
        return render(request, self.template_name, {self.context_object_name: user})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        block_user(user)
        return redirect('user_list')