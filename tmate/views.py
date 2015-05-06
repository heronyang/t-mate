from django.views.decorators.csrf import requires_csrf_token

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from django.db.models import Q

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

# Used to send mail from within Django
from django.core.mail import send_mail

from django.template import Library


# App
from tmate.models import *
from tmate.forms import *
from tmate.s3 import s3_upload

import time
import operator

register = Library()

def index(request):
    is_login = False
    if request.user and request.user.is_authenticated():
        is_login = True

    profiles_programmers = Profile.objects.filter(user_type=0)
    profiles_designers = Profile.objects.filter(user_type=1)
    context = {
            'profiles_programmers': profiles_programmers,
            'profiles_designers': profiles_designers,
            'is_login': is_login,
            }
    return render(request, 'tmate/index.html', context)

def profile(request, uid):

    is_login = False
    if request.user and request.user.is_authenticated():
        is_login = True

    try:
        u = User.objects.get(id=uid)
        profile = Profile.objects.get(user=u)
    except ObjectDoesNotExist:
        return render(request, 'tmate/404.html', {})

    comments = Comment.objects.filter(user=u)

    # is not login
    if not is_login:
        form = CommentForm()
        context = {
                'profile': profile,
                'is_login': is_login,
                'form': form,
                'comments': comments,
                }
        return render(request, 'tmate/profile.html', context)

    new_comment = Comment(user=u, author=request.user)
    form = CommentForm(instance=new_comment)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=new_comment)

    if form.is_valid():
        form.save()

    context = {
            'profile': profile,
            'is_login': is_login,
            'form': form,
            'comments': comments,
            }
    return render(request, 'tmate/profile.html', context)

def register_entry(request):
    context = {}
    return render(request, 'tmate/register_entry.html', context)

def search(request):

    qs = ""
    if 'q' in request.GET:
        qs = request.GET['q']

    is_login = False
    if request.user and request.user.is_authenticated():
        is_login = True

    query_list = []

    for q in qs.split(" "):
        ss = HashTag.objects.filter(content__icontains=q)

        if q.lower() == "programmer" or q.lower() == "programmers":
            query_list.append(Q(user_type=0))
            continue
        elif q.lower() == "designer" or q.lower() == "designers":
            query_list.append(Q(user_type=1))
            continue
        else:
            query_list.append(Q(user_type=0)|Q(user_type=1))

        query_list.append(
                Q(user__last_name__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__username__icontains=q) |
                Q(skills__in=ss) |
                Q(location__icontains=q) |
                Q(position__icontains=q)
                )

    profiles = Profile.objects.filter(reduce(operator.and_, query_list)).distinct()

    context = {'profiles': profiles, 'is_login': is_login, 'key': qs}
    return render(request, 'tmate/search.html', context)

@transaction.atomic
@requires_csrf_token
def register(request):

    context = {}

    context['is_to_find'] = False
    if 'is_to_find' in request.GET:
        print 'is to find is', request.GET['is_to_find']
        if request.GET['is_to_find'] == "1":
            context['is_to_find'] = True
        else:
            context['is_to_find'] = False

    # GET: first time load
    if request.method == 'GET':
        context['form'] = ProfileForm()
        return render(request, 'tmate/register.html', context)

    # POST: check if valid
    form = ProfileForm(request.POST, request.FILES)
    context['form'] = form

    print request.POST

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
    new_profile = form.instance
    new_profile.user = new_user

    if form.cleaned_data['image']:
        url = s3_upload(form.cleaned_data['image'],
                const.PROFILE_IMAGE_PREFIX + str(new_profile.id) + str(int(time.time())) )
        new_profile.picture_url = url
        print 'url: ' + url
    else:
        print 'image is empty'

    form.save()

    ## confirm email
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to the T-Mate!  Please click the link below to
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

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'tmate/confirmed.html', {})
