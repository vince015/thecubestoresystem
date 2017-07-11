from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from django.conf import settings

from thecubestore.models import Item, Sales, Profile, Cube

# Constants
BASE_URL = '/thecubestore/{0}/'
INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."

def user_login(request):
    # Redirection
    next = request.GET.get('next', BASE_URL.format('home'))
    # context_dict = dict()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                messages.error(request, INACTIVE_USER)
                return render(request,
                              'thecubestore/login.html')
        else:
            messages.error(request, INVALID_CREDENTIALS)
            return render(request,
                          'thecubestore/login.html',
                          {'redirect_to': next})

    # context_dict['redirect_to'] = next

    return render(request,
                  'thecubestore/login.html',
                  {'redirect_to': next})

def user_logout(request):

    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


def is_member(user, group):
    return user.groups.filter(name=group).exists()

@login_required
def dashboard(request):

    try:
        context_dict = dict()

        user = User.objects.get(username=request.user.username)
        context_dict['user'] = user
        template = 'thecubestore/index.html'

        # Get user info
        if is_member(user, 'Staff'):

            items = Item.objects.all()
            context_dict['items'] = items

            sales = Sales.objects.all()
            context_dict['sales'] = sales

            context_dict['merchants'] = list()
            users = User.objects.filter(groups__name='Merchant')
            for user in users:
                profile = Profile.objects.get(user=user)
                cubes = Cube.objects.filter(profile=profile)

                context_dict['merchants'].append({'profile': profile,
                                                  'cubes': cubes})

            template = 'thecubestore/staff.html'

        else:
            profile = Profile.objects.get(user=user)
            context_dict['profile'] = profile

            cubes = Cube.objects.filter(profile=profile)
            context_dict['cubes'] = cubes
            
            context_dict['items'] = list()
            for cube in cubes:
                items = Item.objects.filter(cube=cube)
                for item in items:
                    context_dict['items'].append(item)
           
            context_dict['sales'] = list()
            for item in context_dict['items']:
                sales = Sales.objects.filter(item=item)
                for sale in sales:
                    context_dict['sales'].append(sale)

    except Exception as ex:
        raise
        messages.error(request, str(ex))
        print(ex)

    return render(request, template, context_dict)