from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.forms import UserChangeForm


@login_required
def update_account(request, template_name):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, template_name, { 'form': form })
