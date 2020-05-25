from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterForm, UpdateUserForm, CustomerForm
from store.models import Customer
import datetime

now = datetime.datetime.now()


# @login_required(login_url='/login/')
# def user_list(request):
#     users = User.objects.all()
#     # mysql_db = User.objects.using('mysql').get(username='user')
#     # print(mysql_db.last_login)
#
#     context = {
#         'page_title': 'User List',
#         'user_list': users,
#         'now_year': now.year,
#         'now_month': now.month,
#     }
#
#     return render(request, 'accounts/user_list.html', context)


# @login_required(login_url='/login/')
# def group_list(request):
#     groups = Group.objects.all()
#     # mysql_db = User.objects.using('mysql').get(username='user')
#     # print(mysql_db.last_login)
#
#     context = {
#         'page_title': 'Group_list',
#         'groups': groups,
#         'now_year': now.year,
#         'now_month': now.month
#     }
#
#     return render(request, 'accounts/group_list.html', context)


# def group_update(request, update_id):
#     user_update = get_object_or_404(User, id=update_id)
#
#     data = dict()
#
#     if request.method == 'POST':
#         form = AssignGroupForm(request.POST, instance=user_update)
#     else:
#         form = AssignGroupForm(instance=user_update)
#
#     if request.method == 'POST':
#         # import pdb; pdb.set_trace()
#         if form.is_valid():
#             data_group = request.POST.copy()
#             groups = data_group.getlist('groups')
#
#             if groups:
#                 user_update.groups.set(groups, clear=True)
#             else:
#                 user_update.groups.clear()
#             user_update.save()
#
#             data['form_is_valid'] = True
#         else:
#             data['form_is_valid'] = False
#
#     context = {'form': form}
#
#     data['html_form'] = render_to_string('accounts/partial_groups_update.html',context,request=request)
#
#     return JsonResponse(data)


# @login_required(login_url='/login/')
def register(request):
    user_form = RegisterForm(request.POST or None)
    customer_form = CustomerForm(request.POST or None)

    context = {
        'page_title': 'Buat akun baru',
        'form': user_form,
        'customer_form': customer_form
    }

    if request.method == "POST":
        if user_form.is_valid() and customer_form.is_valid():

            # data = request.POST.copy()
            # groups = data.getlist('groups')

            user_instance = user_form.save()

            # for group in groups:
            #     user_instance.groups.add(group)
            # user_instance.save()

            customer_instance = customer_form.save(commit=False)
            customer_instance.user = user_instance
            customer_instance.save()

            return redirect("store")

    else:

        # import pdb; pdb.set_trace()
        return render(request, "accounts/register-update.html", context)
    return render(request, "accounts/register-update.html", context)


# @login_required(login_url='/login/')
# def deactivate(request, user_id):
#     user = User.objects.get(id=user_id)
#
#     if user.is_active:
#         user.is_active = False
#         user.save()
#     else:
#         user.is_active = True
#         user.save()
#
#     return redirect('accounts:user_list')


@login_required(login_url='/login/')
def delete(request, delete_id):
    User.objects.get(id=delete_id).delete()

    return redirect('store')


@login_required(login_url='/login/')
def update(request, update_id):
    # user_update = User.objects.get(id=update_id)
    user_update = get_object_or_404(User, id=update_id)

    data = {
        'first_name': user_update.first_name,
        'last_name': user_update.last_name,
        'email': user_update.email,
        'username': user_update.username,
        'password': user_update.password,
        'groups': user_update.groups.all(),
        'is_active': user_update.is_active,
        'is_staff': user_update.is_staff,
    }

    employee_update = ''
    employee_data = ''
    try:
        employee_update = Employee.objects.get(user__id=update_id)
        employee_data = {
            'user': employee_update.user,
            'division': employee_update.division,
            'title': employee_update.title,
        }
    except:
        pass

    if request.method == 'POST':
        form = UpdateUserForm(request.POST or None, initial=data, instance=user_update)
        try:
            employee_form = EmployeeForm(request.POST or None, initial=employee_data, instance=employee_update)
        except:
            employee_form = EmployeeForm(request.POST or None)

        if form.is_valid() and employee_form.is_valid():
            data = request.POST.copy()
            groups = data.getlist('groups')

            if groups:
                user_update.groups.set(groups, clear=True)
            else:
                user_update.groups.clear()
            user_update.save()

            employee_update.user = user_update
            employee_update.save()

            return redirect('store')

        else:

            return render(request, "accounts/register-update.html",
                          context={'form': form, 'employee_form': employee_form,
                                   'page_title': 'Update User Data',
                                   'now_year': now.year, 'now_month': now.month})

    else:
        form = UpdateUserForm(initial=data, instance=user_update)
        try:
            employee_form = EmployeeForm(initial=employee_data, instance=employee_update)
        except:
            employee_form = EmployeeForm()

        return render(request, 'accounts/update.html',
                      context={'form': form, 'employee_form': employee_form,
                               'page_title': 'Update User Data',
                               'now_year': now.year, 'now_month': now.month})
