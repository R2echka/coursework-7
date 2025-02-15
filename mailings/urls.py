from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('recipient/new', views.RecipientCreate.as_view(), name='new_recipient'),
    path('recipient/<int:pk>/update', views.RecipientUpdate.as_view(), name='update_recipient'),
    path('recipient/<int:pk>/delete', views.RecipientDelete.as_view(), name='delete_recipient'),
    path('recipient/<int:pk>', views.RecipientDetail.as_view(), name='recipient'),
    path('recipient/list', views.Recipients.as_view(), name='recipients'),
    path('message/new', views.MessageCreate.as_view(), name='new_message'),
    path('message/<int:pk>/update', views.MessageUpdate.as_view(), name='update_message'),
    path('message/<int:pk>/delete', views.MessageDelete.as_view(), name='delete_message'),
    path('message/<int:pk>', views.MessageDetail.as_view(), name='message'),
    path('message/list', views.Messages.as_view(), name='messages'),
    path('mailing/new', views.MailingCreate.as_view(), name='new_mailing'),
    path('mailing/<int:pk>/update', views.MailingUpdate.as_view(), name='update_mailing'),
    path('mailing/<int:pk>/delete', views.MailingDelete.as_view(), name='delete_mailing'),
    path('mailing/<int:pk>', views.MailingDetail.as_view(), name='mailing'),
    path('mailing/list', views.Mailings.as_view(), name='mailings'),
    ]