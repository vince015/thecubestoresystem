from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Cube, Item

# Constants
BASE_URL = 'thecubestore/{0}/'

@login_required
def add(request, cube_id):

    try:
        context_dict = dict()

        # Get user object
        cube = Cube.objects.get(id=cube_id)

        if request.method == "POST":

            context_dict['data'] = request.POST

            quantity = int(request.POST.get('quantity'))
            price = float(request.POST.get('price'))
            vat = float(request.POST.get('vat'))
            sales = float(request.POST.get('sales'))
            item = Item.objects.create(cube=cube,
                                       name=request.POST.get('name'),
                                       quantity=quantity,
                                       vat=vat,
                                       commission=sales)

            messages.info(request, 'Successfully added item.')

            return redirect('/thecubestore/cube/view/{0}'.format(cube_id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        raise
        messages.error(request, str(ex))
        print(ex)

    context_dict['cube_id'] = cube_id
    context_dict['cube'] = cube.unit
    return render(request,
                  BASE_URL.format('item_add.html'),
                  context_dict)

@login_required
def view(request, item_id):

    try:
        context_dict = dict()
        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('item_view.html'),
                  context_dict)

@login_required
def edit(request, item_id):

    try:
        context_dict = dict()
        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

        if request.method == "POST":

            context_dict['data'] = request.POST

            initial = int(request.POST.get('initial'))
            current = int(request.POST.get('current'))
            price = float(request.POST.get('price'))
            vat = float(request.POST.get('vat'))
            sales = float(request.POST.get('sales'))

            item.name = request.POST.get('name')
            item.initial = initial
            item.current = current
            item.price = price
            item.vat = vat
            item.commission = sales
            item.save()

            messages.info(request, 'Successfully updated item.')
            return redirect('/thecubestore/item/view/{0}'.format(item.id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('item_edit.html'),
                  context_dict)

@login_required
def delete(request, item_id):

    try:
        context_dict = dict()
        item = Item.objects.get(id=item_id)
        item.delete()

        messages.info(request, 'Successfully deleted item.')

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return redirect('/thecubestore/item/list/')

@login_required
def list(request):

    try:
        context_dict = dict()
        items = Item.objects.all()
        context_dict['items'] = items

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('item_list.html'),
                  context_dict)
