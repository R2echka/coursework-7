from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.urls import reverse
from users.models import CustomUser

@permission_required("users.can_block_users")
def block_user(self, pk):
    user = CustomUser.objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect(reverse("users:user_list"))

