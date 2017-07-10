from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from thecubestore.models import Profile, Store

# Constants
BASE_URL = 'thecubestore/{0}/'

@login_required
def add(request, user_id):

    try:
        context_dict = dict()

        # Get user object
        user = User.objects.get(id=user_id)

        if request.method == "POST":

            context_dict['data'] = request.POST

            profile = Profile.objects.get(user=user)
            store = Store.objects.create(profile=profile,
                                         name=request.POST.get('name'),
                                         facebook=request.POST.get('facebook'),
                                         instagram=request.POST.get('instagram'),
                                         website=request.POST.get('website'))

            messages.info(request, 'Successfully added store.')

            return redirect('/thecubestore/profile/view/{0}'.format(user_id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    context_dict['user_id'] = user_id
    context_dict['username'] = user.username
    return render(request,
                  BASE_URL.format('store_add.html'),
                  context_dict)

@login_required
def view(request, store_id):

    try:
        context_dict = dict()
        store = Store.objects.get(id=store_id)
        context_dict['store'] =store

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('store_view.html'),
                  context_dict)

@login_required
def edit(request, store_id):

    try:
        context_dict = dict()
        store = Store.objects.get(id=store_id)
        context_dict['store'] =store

        if request.method == "POST":

            context_dict['data'] = request.POST

            store.name = request.POST.get('name')
            store.facebook = request.POST.get('facebook')
            store.instagram = request.POST.get('instagram')
            store.website = request.POST.get('website')
            store.save()

            messages.info(request, 'Successfully updated store.')
            return redirect('/thecubestore/store/view/{0}'.format(store.id))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('store_edit.html'),
                  context_dict)

@login_required
def delete(request, store_id):

    try:
        context_dict = dict()
        store = Store.objects.get(id=store_id)
        store.delete()

        messages.info(request, 'Successfully deleted store.')

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
        stores = Store.objects.all()
        context_dict['stores'] = stores

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    return render(request,
                  BASE_URL.format('store_list.html'),
                  context_dict)
