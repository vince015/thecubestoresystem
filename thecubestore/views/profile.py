from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Profile, Store, Cube, Payment

# Constants
BASE_URL = 'thecubestore/{0}/'

def convert_date(str_time):

    try:
        date = datetime.strptime(str_time, '%m/%d/%Y')
        formatted = datetime.strftime(date, '%Y-%m-%d')
        return formatted

    except:
        raise

@login_required
def add(request, user_id):

    try:
        context_dict = dict()

        # Get user object
        user = User.objects.get(id=user_id)

        if request.method == "POST":

            context_dict['data'] = request.POST

            # Get user object
            user = User.objects.get(id=user_id)

            birthday = convert_date(request.POST.get('birthday'))
            profile = Profile.objects.create(user=user,
                                             contact_number=request.POST.get('contact_number'),
                                             primary_address=request.POST.get('primary_address'),
                                             alternate_address=request.POST.get('alternate_address'),
                                             birthday=birthday)

            messages.info(request, 'Successfully added profile.')

            return redirect('/thecubestore/profile/view/{0}'.format(user_id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    context_dict['user_id'] = user_id
    context_dict['username'] = user.username
    return render(request,
                  BASE_URL.format('profile_add.html'),
                  context_dict)

@login_required
def view(request, user_id):

    try:
        context_dict = dict()

        # Get user object
        user = User.objects.get(id=user_id)
        # context_dict['user'] = user
        # context_dict['merchant'] = user.groups.filter(name='Member').exists()

        profile = Profile.objects.get(user=user)
        context_dict['profile'] = profile

        stores = Store.objects.filter(profile=profile)
        context_dict['stores'] = stores

        cubes = Cube.objects.filter(profile=profile)
        context_dict['cubes'] = cubes

        payments = Payment.objects.filter(profile=profile)
        context_dict['payments'] = payments

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('profile_view.html'),
                  context_dict)

@login_required
def list_all(request):

    try:
        context_dict = dict()
        merchs = list()

        users = User.objects.filter(groups__name='Merchant')
        for user in users:
            profile = Profile.objects.get(user=user)
            cubes = Cube.objects.filter(profile=profile)
            stores = Store.objects.filter(profile=profile)

            merchs.append({'profile': profile,
                           'cubes': len(cubes),
                           'stores': len(stores)})
        context_dict['merchants'] = merchs

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('profile_list.html'),
                  context_dict)
