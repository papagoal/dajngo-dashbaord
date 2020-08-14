from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Family, Person
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import UserRegistrationForm, \
                    UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages

from authy.api import AuthyApiClient
from .forms import VerificationForm, TokenForm
from django.conf import settings
from .forms import UserRegistrationForm as UR

authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)

# Create your views here.
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):
    return render(request, 'a_thing/home.html', {'section': 'home'})

@login_required
def index(request):
    family = Family.objects.all()
    return render(request, 'a_thing/index.html', {'family': family})


class DetailView(generic.DetailView):
    model = Family
    template_name = 'a_thing/detail.html'


class BioView(generic.DetailView):
    model = Person
    template_name = 'a_thing/bio.html'

@login_required
def dash_1(request):
    return render(request, 'a_thing/dash_1.html')


def dash_2(request):
    return render(request, 'a_thing/dash_2.html')


def dash_3(request):
    return render(request, 'a_thing/dash_3.html')


def dash_4(request):
    return render(request, 'a_thing/dash_4.html')


def dash_5(request):
    return render(request, 'a_thing/dash_5.html')


def dash_cb_1(request):
    return render(request, 'a_thing/dash_cb_1.html')


def dash_OE(request):
    return render(request, 'a_thing/dash_OE.html')


def dash_OE_2(request):
    return render(request, 'a_thing/dash_OE_2.html')


def dash_cb_4(request):
    return render(request, 'a_thing/dash_cb_4.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'a_thing/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'a_thing/register.html',
                  {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile update '\
                                        'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'a_thing/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def tw(request):
    return render(request, 'a_thing/tw_2.html', {'phone': UR.clean_phone(request)})

# def tw(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         print("130********************************************")
#         # create a form instance and populate it with data from the request:
#         form = UR(request.POST)
#         # check whether it's valid:
#         print("134*********************************************")
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             print(form.clean_phone())
#             # redirect to a new URL:
#             return HttpResponseRedirect('/a_thing/tw_2.html')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         print("144*********************************************")
#         form = UR()
#
#     return render(request, 'a_thing/tw_2.html', {'phone': form})

def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        form_2 = UR(request.POST)
        if form.is_valid():
            # request.session['phone_number'] = form.cleaned_data['phone_number']
            # request.session['country_code'] = form.cleaned_data['country_code']
            authy_api.phones.verification_start(
                # form.cleaned_data['phone_number'],
                # form.cleaned_data['country_code'],
                country_code='+1',
                phone_number="2048070812",
                via=form.cleaned_data['via']
            )
            # change this
            # return redirect('token_validation')
            return redirect('/verification/token/')

    else:
        form = VerificationForm()
    return render(request, 'a_thing/phone_verification.html', {'form': form})

def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = authy_api.phones.verification_check(
                # request.session['phone_number'],
                # request.session['country_code'],
                "2048070812",
                '+1',
                form.cleaned_data['token']
            )
            if verification.ok():
                request.session['is_verified'] = True
                return redirect('/verified/')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'a_thing/token_validation.html', {'form': form})

def verified(request):
    if not request.session.get('is_verified'):
        return redirect('phone_verification')
    # return render(request, 'a_thing/verified.html')
    return render(request, 'a_thing/home.html')