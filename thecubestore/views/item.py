from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from thecubestore.models import Cube, Item

# Constants
BASE_URL = 'thecubestore/{0}/'

@login_required
def view(request, item_id):

    try:
        context_dict = dict()
        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

    except ObjectDoesNotExist:
        raise Http404()

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('item_view.html'),
                  context_dict)

@login_required
def list_all(request):

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

@login_required
@permission_required('thecubestore.add_item', raise_exception=True)
def add(request, cube_id):

    try:
        context_dict = dict()

        # Get user object
        cube = Cube.objects.get(id=cube_id)
        context_dict['cube_id'] = cube_id
        context_dict['cube'] = cube.unit

        if request.method == "POST":

            context_dict['data'] = request.POST

            quantity = int(request.POST.get('quantity'))
            price = float(request.POST.get('price'))
            vat = float(request.POST.get('vat'))
            sales = float(request.POST.get('sales'))
            item = Item.objects.create(cube=cube,
                                       name=request.POST.get('name'),
                                       price=price,
                                       quantity=quantity,
                                       vat=vat,
                                       commission=sales)

            messages.info(request, 'Successfully added item.')

            return redirect('/thecubestore/cube/view/{0}#cube-item'.format(cube_id))

    except ObjectDoesNotExist:
        raise Http404()

    except Exception as ex:
        raise
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('item_add.html'),
                  context_dict)

@login_required
@permission_required('thecubestore.change_item', raise_exception=True)
def edit(request, item_id):

    try:
        context_dict = dict()
        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

        if request.method == "POST":

            context_dict['data'] = request.POST

            quantity = int(request.POST.get('quantity'))
            price = float(request.POST.get('price'))
            vat = float(request.POST.get('vat'))
            sales = float(request.POST.get('sales'))

            item.name = request.POST.get('name')
            item.quantity = quantity
            item.price = price
            item.vat = vat
            item.commission = sales
            item.save()

            messages.info(request, 'Successfully updated item.')
            return redirect('/thecubestore/item/view/{0}'.format(item.id))

    except ObjectDoesNotExist:
        raise Http404()

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('item_edit.html'),
                  context_dict)

@login_required
@permission_required('thecubestore.delete_item', raise_exception=True)
def delete(request, item_id):

    try:
        context_dict = dict()
        item = Item.objects.get(id=item_id)
        item.delete()

        messages.info(request, 'Successfully deleted item.')

    except ObjectDoesNotExist:
        raise Http404()

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return redirect('/thecubestore/item/list')
