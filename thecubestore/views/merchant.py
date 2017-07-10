import json
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from thecubestore.models import Profile, Cube, Store, Lease, Payment

# Constants
BASE_URL = 'thecubestore/{0}/'

def convert_date(str_time):

    try:
        date = datetime.strptime(str_time, '%m/%d/%Y')
        formatted = datetime.strftime(date, '%Y-%m-%d')
        return formatted

    except:
        raise

def confirm_password(password1, password2):

    if password1 == password2:
        return True

    else:
        return False

@login_required
def list(request):

    try:
        context_dict = dict()

        profiles = Profile.objects.all()
        for profile in profiles:
            cubes = Cube.objects.filter(profile=profile)
            stores = Store.objects.filter(profile=profile)
            leases = Lease.objects.filter(profile=profile)
            payments = Payment.objects.filter(profile=profile)

            details = dict()
            details['profile'] = profile
            details['cubes'] = cubes
            details['stores'] = stores
            details['leases'] = leases
            details['payments'] = payments

            context_dict[profile.id] = details

        return render(request,
                      BASE_URL.format('merchant.html'),
                      context_dict)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

        return HttpResponse(status=500)

@login_required
def add(request):

    try:
        context_dict = dict()

        if request.method == "POST":

            context_dict['data'] = request.POST

            confirm = confirm_password(request.POST.get('password'),
                                       request.POST.get('confirm_password'))
            if not confirm:
                raise Exception('Password does not match.')

            # Create a user object
            user = User.objects.create_user(request.POST.get('username'),
                                            request.POST.get('email'),
                                            request.POST.get('password'))
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.save()

            # Add to group
            group = Group.objects.get(name='Merchants') 
            group.user_set.add(user)

            '''
            # Create a Profile object
            birthday = convert_date(request.POST.get('birthday'))
            owner = Profile.objects.create(user=user,
                                           contact_number=request.POST.get('contact_number'),
                                           primary_address=request.POST.get('primary_address'),
                                           alternate_address=request.POST.get('alt_address'),
                                           birthday=birthday)
            # Create a Store object
            store = Store.objects.create(name=request.POST.get('store_name'),
                                         facebook=request.POST.get('store_fb'),
                                         instagram=request.POST.get('store_ig'),
                                         website=request.POST.get('store_web'))

            # Create Lease object
            duration = int(request.POST.get('lease_duration'))
            month_promo = int(request.POST.get('lease_promo'))
            start_date = convert_date(request.POST.get('lease_start_date'))
            end_date = convert_date(request.POST.get('lease_end_date'))
            vat = float(request.POST.get('lease_vat'))
            sales = float(request.POST.get('lease_sales'))
            lease = Lease.objects.create(duration=duration,
                                        month_promo=month_promo,
                                        start_date=start_date,
                                        end_date=end_date,
                                        vat=vat,
                                        sales=sales)

            # Create Payment object
            payment = Payment.objects.create(mode=request.POST.get('mode'),
                                            bank=request.POST.get('bank'),
                                            account=request.POST.get('bank_account'))

            # Create a Merchant object
            merchant = Merchant.objects.create(owner=owner,
                                              store=store,
                                              lease=lease,
                                              payment=payment)

            # Redirect for cube
            '''
            return HttpResponse(status=200)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    finally:
        return render(request,
                      BASE_URL.format('user_add.html'),
                      context_dict)

@login_required
def edit(request, profile_id):

    try:
        context_dict = dict()
        profile = Profile.objects.get_object_or_404(id=profile_id)
        cubes = Cube.objects.filter(profile=profile)
        stores = Store.objects.filter(profile=profile)
        leases = Lease.objects.filter(profile=profile)
        payments = Payment.objects.filter(profile=profile)

        context_dict['profile'] = profile
        context_dict['cubes'] = cubes
        context_dict['stores'] = stores
        context_dict['leases'] = leases
        context_dict['payments'] = payments

        if request.method == "POST":

            user = profile.user
            user.email = request.POST.get('email')
            user.last_name = request.POST.get('lastname')
            user.first_name = request.POST.get('firstname')
            user.save()
            profile.user = user

            birthday = convert_date(request.POST.get('birthday'))
            profile.birthday = birthday
            profile.contact_number = request.POST.get('contact_number')
            profile.primary_address = request.POST.get('primary_address')
            profile.alternate_address = request.POST.get('alt_address')
            profile.save()

            messages.info(request, 'Successfully updated merchant.')

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    finally:
        return render(request,
                      BASE_URL.format('merchant.html'),
                      context_dict)

@login_required
def delete(request, profile_id):

    try:
        context_dict = dict()
        profile = Profile.objects.get_object_or_404(id=profile_id)
        profile.delete()

        messages.info(request, 'Successfully deleted merchant.')

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    finally:
        return render(request,
                      BASE_URL.format('merchant.html'),
                      context_dict)
