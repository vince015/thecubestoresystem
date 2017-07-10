from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Profile, Lease

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
        success = False

        # Get user object
        user = User.objects.get(id=user_id)

        if request.method == "POST":

            context_dict['data'] = request.POST

            profile = Profile.objects.get(user=user)
            # Create Lease object
            duration = int(request.POST.get('duration'))
            promo = int(request.POST.get('promo'))
            start_date = convert_date(request.POST.get('start_date'))
            end_date = convert_date(request.POST.get('end_date'))
            next_due_date = convert_date(request.POST.get('next_due_date'))
            vat = float(request.POST.get('vat'))
            sales = float(request.POST.get('sales'))
            lease = Lease.objects.create(profile=profile,
                                         duration=duration,
                                         promo=promo,
                                         start_date=start_date,
                                         end_date=end_date,
                                         next_due_date=next_due_date,
                                         vat=vat,
                                         sales=sales)

            messages.info(request, 'Successfully added lease.')

            return redirect('/thecubestore/profile/view/{0}'.format(user_id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        raise
        messages.error(request, str(ex))
        print(ex)

    context_dict['user_id'] = user_id
    context_dict['username'] = user.username
    return render(request,
                  BASE_URL.format('lease_add.html'),
                  context_dict)

@login_required
def view(request, lease_id):

    try:
        context_dict = dict()
        lease = Lease.objects.get(id=lease_id)
        context_dict['lease'] = lease

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('lease_view.html'),
                  context_dict)

@login_required
def edit(request, lease_id):

    try:
        context_dict = dict()
        lease = Lease.objects.get(id=lease_id)
        context_dict['lease'] = lease.__dict__
        context_dict['lease']['start_date'] = datetime.strftime(lease.start_date, '%m/%d/%Y')
        context_dict['lease']['end_date'] = datetime.strftime(lease.end_date, '%m/%d/%Y')
        context_dict['lease']['next_due_date'] = datetime.strftime(lease.next_due_date, '%m/%d/%Y')

        if request.method == "POST":

            context_dict['data'] = request.POST

            duration = int(request.POST.get('duration'))
            promo = int(request.POST.get('promo'))
            start_date = convert_date(request.POST.get('start_date'))
            end_date = convert_date(request.POST.get('end_date'))
            next_due_date = convert_date(request.POST.get('next_due_date'))
            vat = float(request.POST.get('vat'))
            sales = float(request.POST.get('sales'))

            lease.duration = duration
            lease.promo = promo
            lease.start_date = start_date
            lease.end_date = end_date
            lease.next_due_date = next_due_date
            lease.vat = vat
            lease.sales = sales
            lease.save()

            messages.info(request, 'Successfully updated lease.')
            return redirect('/thecubestore/lease/view/{0}'.format(lease.id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        raise
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('lease_edit.html'),
                  context_dict)

@login_required
def delete(request, lease_id):

    try:
        context_dict = dict()
        lease = Lease.objects.get(id=lease_id)
        lease.delete()

        messages.info(request, 'Successfully deleted lease.')

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return redirect('/thecubestore/profile/view/{0}'.format(user_id))

@login_required
def list(request):

    try:
        context_dict = dict()
        leases = Lease.objects.all()
        context_dict['leases'] = leases

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('lease_list.html'),
                  context_dict)
