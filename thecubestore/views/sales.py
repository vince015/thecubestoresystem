from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Item, Sales

# Constants
BASE_URL = 'thecubestore/{0}/'

def compute_net(amount, vat, sales):

    vat_deduct = amount * (vat / 100)
    sales_deduct = amount * (sales / 100)
    return amount - vat_deduct - sales_deduct

def current_date():

    try:
        now = datetime.utcnow()
        # Add 8hrs for PH time
        pst = now + timedelta(hours=8)
        formatted = datetime.strftime(pst, '%Y-%m-%d')
        return formatted

    except:
        raise

@login_required
def add(request):

    try:
        context_dict = dict()

        if request.method == "POST":
            item = Item.objects.get(id=request.POST.get('item'))
            
            quantity = int(request.POST.get('quantity'))
            net = compute_net(item.price*quantity, item.vat, item.commission)
            sales = Sales.objects.create(item=item,
                                         date=current_date(),
                                         quantity=quantity,
                                         net=net)

            item.quantity = item.quantity - quantity
            item.save()

            return redirect('/thecubestore')

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        raise
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('staff.html'),
                  context_dict)

@login_required
def list(request):

    try:
        context_dict = dict()
        sales = Sales.objects.all()
        context_dict['sales'] = sales

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('sales_list.html'),
                  context_dict)
