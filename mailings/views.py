from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView, DeleteView
from .models import MailingRecipient, Message, Mailing
from .forms import RecipientForm, MessageForm, MailingForm
from . import services
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Create your views here.
class MainPage(View):
    model1 = MailingRecipient
    model2 = Message
    model3 = Mailing
    template_name = 'mailings/main.html'
    context_object_name = 'main'
    context = {}

    def get(self, request, *args, **kwargs):
        user = request.user
        self.context = {
            'recipients': self.model1.objects.all(),
            'messages': self.model2.objects.all(),
            'mailings': self.model3.objects.all(),
            'active_mailings_number': services.active_mailings_number(user),
            'successful_attempts': services.successful_attempts(user),
            'unsuccessful_attempts': services.unsuccessful_attempts(user),
            'messages_count': services.messages_count(user),
            'unique_recipients': services.unique_recipients(user),
        }
        return render(request, self.template_name, self.context)

class Recipients(LoginRequiredMixin, ListView):
    model= MailingRecipient
    template_name = "mailings/recipients.html"
    context_object_name = 'recipients'

@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientDetail(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'mailings/recipient.html'
    context_object_name = 'recipient'

class RecipientCreate(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = RecipientForm
    template_name = 'mailings/form.html'
    success_url = '/'

class RecipientUpdate(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    form_class = RecipientForm
    template_name = 'mailings/form.html'
    success_url = '/'

class RecipientDelete(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = 'mailings/delete.html'
    success_url = '/'

@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetail(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailings/message.html'
    context_object_name = 'message'

class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/form.html'
    success_url = '/'

class MessageUpdate(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/form.html'
    success_url = '/'

class MessageDelete(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailings/delete.html'
    success_url = '/'

class Messages(LoginRequiredMixin, ListView):
    model= Message
    template_name = "mailings/messages.html"
    context_object_name = 'messages'

@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingDetail(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing.html'
    context_object_name = 'mailing'

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        if mailing.status == 'created':
            mailing.status = 'active'
            mailing.starting_time = timezone.now()
            mailing.save()
            services.send_mailing(mailing.pk, request.user)
            successful_count = services.successful_attempts(request.user)
            unsuccessful_count = services.unsuccessful_attempts(request.user)
        elif mailing.status == 'active':
            mailing.status = 'completed'
            mailing.ending_time = timezone.now()
            mailing.save()
        return redirect('mailing', pk=mailing.pk)

class MailingCreate(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.request.user.mailings += 1
        self.request.user.save()
        return super().form_valid(form)

class MailingUpdate(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/form.html'
    success_url = '/'

class MailingDelete(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/delete.html'
    success_url = '/'

    def form_valid(self, form):
        self.owner = self.request.user
        self.request.user.mailings -= 1
        self.request.user.save()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

class Mailings(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailings.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('users.manager'):
            return services.get_cached_mailings()
        else:
            raise PermissionDenied
