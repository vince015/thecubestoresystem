
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Constants
BASE_URL = 'thecubestore/{0}/'

def confirm_password(password1, password2):

    if password1 == password2:
        return True

    else:
        return False

@login_required
def add(request):

    try:
        context_dict = dict()
        success = False
        user_id = None

        if request.method == "POST":

            context_dict['data'] = request.POST

            confirm = confirm_password(request.POST.get('password'),
                                       request.POST.get('confirm_password'))
            if not confirm:
                raise Exception('Password does not match.')

            # Create a user object
            username = request.POST.get('username')
            user = User.objects.create_user(username,
                                            request.POST.get('email'),
                                            request.POST.get('password'))
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.save()
            user_id = user.id

            # Add to group
            group = Group.objects.get(name='Merchant') 
            group.user_set.add(user)

            messages.info(request, 'Successfully added {0}.'.format(username))
            
            success = True

    except Exception as ex:
        messages.error(request, str(ex))
        print(ex)

    finally:
        if success:
            return redirect('/thecubestore/profile/add/{0}'.format(user_id))

        return render(request,
                      BASE_URL.format('user_add.html'),
                      context_dict)
