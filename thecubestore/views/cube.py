from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Profile, Cube, Item

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

            profile = Profile.objects.get(user=user)
            duration = int(request.POST.get('duration'))
            promo = int(request.POST.get('promo'))
            start_date = convert_date(request.POST.get('start_date'))
            end_date = convert_date(request.POST.get('end_date'))
            next_due_date = convert_date(request.POST.get('next_due_date'))

            cube = Cube.objects.create(profile=profile,
                                       unit=request.POST.get('unit'),
                                       duration=duration,
                                       promo=promo,
                                       start_date=start_date,
                                       end_date=end_date,
                                       next_due_date=next_due_date)

            messages.info(request, 'Successfully added cube.')
            context_dict['active'] = 'cube'

            return redirect('/thecubestore/profile/view/{0}'.format(user_id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    context_dict['user_id'] = user_id
    context_dict['owner'] = '{0} {1}'.format(user.first_name,
                                             user.last_name)
    return render(request,
                  BASE_URL.format('cube_add.html'),
                  context_dict)

@login_required
def view(request, cube_id):

    try:
        context_dict = dict()
        cube = Cube.objects.get(id=cube_id)
        context_dict['cube'] = cube

        items = Item.objects.filter(cube=cube)
        context_dict['items'] = items

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('cube_view.html'),
                  context_dict)

@login_required
def edit(request, cube_id):

    try:
        context_dict = dict()
        cube = Cube.objects.get(id=cube_id)
        context_dict['cube'] = cube.__dict__
        context_dict['cube']['start_date'] = datetime.strftime(cube.start_date, '%m/%d/%Y')
        context_dict['cube']['end_date'] = datetime.strftime(cube.end_date, '%m/%d/%Y')
        context_dict['cube']['next_due_date'] = datetime.strftime(cube.next_due_date, '%m/%d/%Y')

        if request.method == "POST":

            context_dict['data'] = request.POST

            duration = int(request.POST.get('duration'))
            promo = int(request.POST.get('promo'))
            start_date = convert_date(request.POST.get('start_date'))
            end_date = convert_date(request.POST.get('end_date'))
            next_due_date = convert_date(request.POST.get('next_due_date'))

            cube.unit = request.POST.get('unit')
            cube.duration = duration
            cube.promo = promo
            cube.start_date = start_date
            cube.end_date = end_date
            cube.next_due_date = next_due_date
            cube.save()

            messages.info(request, 'Successfully updated cube.')
            return redirect('/thecubestore/cube/view/{0}'.format(cube.id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('cube_edit.html'),
                  context_dict)

@login_required
def delete(request, cube_id):

    try:
        context_dict = dict()
        cube = Cube.objects.get(id=cube_id)
        cube.delete()

        messages.info(request, 'Successfully deleted cube.')

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return redirect('/thecubestore/cube/list')

@login_required
def list(request):

    try:
        context_dict = dict()
        cubes = Cube.objects.all()
        context_dict['cubes'] = cubes

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('cube_list.html'),
                  context_dict)
