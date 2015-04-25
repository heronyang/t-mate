from django.shortcuts import render

from django.views.decorators.csrf import requires_csrf_token

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# App
from tmate.models import *
from tmate.forms import *

def index(request):
    context = {}
    return render(request, 'tmate/index.html', context)

@transaction.atomic
@requires_csrf_token
def register(request):

    context = {}

    # GET: first time load
    if request.method == 'GET':
        context['form'] = ProfileForm()
        return render(request, 'tmate/register.html', context)

    # POST: check if valid
    form = ProfileForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'tmate/register.html', context)

    # POST: is valid, add new user and profile
    ## new user
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])

    new_user.is_active = False
    new_user.save()

    ## new profile
    new_profile = Profile(user = new_user)
    new_profile.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to the Bug Killer!  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(),
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'tmate/needs-confirmation.html', context)
