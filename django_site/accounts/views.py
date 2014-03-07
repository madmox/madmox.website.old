from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


@login_required
def update_account(request, template_name):
    return render(request, template_name, {})
