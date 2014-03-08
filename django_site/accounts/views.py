from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from accounts.forms import UserChangeForm


@login_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def update_account(request, template_name):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('accounts:profile-update-done')
            )
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, template_name, { 'form': form })

@login_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def update_account_done(request, template_name):
    return render(request, template_name, {})
