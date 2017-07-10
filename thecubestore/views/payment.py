from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Profile, Payment

# Constants
BASE_URL = 'thecubestore/{0}/'

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
            # Create Payment object
            payment = Payment.objects.create(profile=profile,
                                             mode=request.POST.get('mode'),
                                             bank=request.POST.get('bank'),
                                             account=request.POST.get('account'))

            messages.info(request, 'Successfully added payment.')

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
                  BASE_URL.format('payment_add.html'),
                  context_dict)

@login_required
def view(request, payment_id):

    try:
        context_dict = dict()
        payment = Payment.objects.get(id=payment_id)
        context_dict['payment'] = payment

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('payment_view.html'),
                  context_dict)

@login_required
def edit(request, payment_id):

    try:
        context_dict = dict()
        payment = Payment.objects.get(id=payment_id)
        context_dict['payment'] = payment

        if request.method == "POST":

            context_dict['data'] = request.POST

            payment.mode = request.POST.get('mode')
            payment.bank = request.POST.get('bank')
            payment.account = request.POST.get('account')
            payment.save()

            messages.info(request, 'Successfully updated payment.')
            return redirect('/thecubestore/payment/view/{0}'.format(payment.id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('payment_edit.html'),
                  context_dict)

@login_required
def delete(request, payment_id):

    try:
        context_dict = dict()
        payment = Payment.objects.get(id=payment_id)
        payment.delete()

        messages.info(request, 'Successfully deleted cube.')

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
        payments = Payment.objects.all()
        context_dict['payments'] = payments

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('payment_list.html'),
                  context_dict)
