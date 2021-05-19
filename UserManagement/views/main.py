from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ..tables import TransactionSummaryTable, TransactionSummaryLineTable
from Core import models as core_models
from django_tables2 import RequestConfig
from MasterData import models as master_data_models
import xlwt
from Core import forms as core_forms
import os



def get_login_page(request):
    return render(request, 'UserManagement/Auth/Login.html')

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(request.META['HTTP_REFERER'])

        else:
            messages.error(request, 'Please correct the error below.')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'UserManagement/Auth/ChangePassword.html', {
            'form': form
        })


@login_required(login_url='/')
def logout_view(request):
    logout(request)
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


def authenticate_user(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    form = core_forms.PayloadImportForm()

    if user is not None and user.is_authenticated:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            elif user.is_staff:
                login(request, user)
                facility = request.user.profile.facility
                transaction_summary = core_models.TransactionSummary.objects.filter(
                    facility_hfr_code=facility.facility_hfr_code).order_by('-transaction_date_time')
                transaction_summary_table = TransactionSummaryTable(transaction_summary)
                RequestConfig(request, paginate={"per_page": 10}).configure(transaction_summary_table)
                return redirect('/dashboard', {"transaction_summary_table": transaction_summary_table,"payload_form":form})
            else:
                messages.success(request,'Not allowed to access this portal')
                return render(request, 'UserManagement/Auth/Login.html')
        else:
            messages.success(request, 'User is not active')
            return render(request, 'UserManagement/Auth/Login.html')
    else:
        messages.success(request, 'User name or Password is wrong')
        return render(request, 'UserManagement/Auth/Login.html')


def get_admin_page(request):
    if request.user.is_super_user:
        return redirect('/admin/')
    else:
        return render(request, 'UserManagement/Auth/Login.html')



@login_required(login_url='/')
def set_changed_password(request):

    if request.POST:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password2']

        user = authenticate(request, username=request.user.username, password=old_password)

        if user is not None and user.is_authenticated:
            logged_user = User.objects.get(username = request.user.username)
            logged_user.set_password(new_password)
            logged_user.save()

            return HttpResponse(status=200)

        else:

            return HttpResponse(status=401)

def export_transaction_lines(request):
    if request.method == "POST":
        transaction_id = request.POST["item_pk"]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="TransactionSummaryLines.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('TransactionSummaryLines')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Transaction', 'CHW ID','NUMBER OF CLIENTS REGISTERED' ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        transaction_lines = core_models.TransactionSummaryLine.objects.filter(transaction_id = transaction_id)

        for row in transaction_lines:
            column_names = tuple(row)
            row_num += 1
            for col_num in range(len(column_names)):
                print(col_num)
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response


def get_dashboard(request):
    form = core_forms.PayloadImportForm()
    facility = request.user.profile.facility
    transaction_summary = core_models.TransactionSummary.objects.filter(facility_hfr_code=facility.facility_hfr_code).order_by('-transaction_date_time')
    transaction_summary_table = TransactionSummaryTable(transaction_summary)
    RequestConfig(request, paginate={"per_page": 10}).configure(transaction_summary_table)

    return render(request, 'UserManagement/Dashboard/index.html',{"transaction_summary_table": transaction_summary_table,
                                                                  "payload_form": form})


def get_transaction_summary_lines(request,item_pk):
    transaction_summary_lines = core_models.TransactionSummaryLine.objects.filter\
        (transaction_id=item_pk).order_by('-id')
    transaction_summary_lines_table = TransactionSummaryLineTable(transaction_summary_lines)
    RequestConfig(request, paginate={"per_page": 10}).configure(transaction_summary_lines_table)

    return render(request,'UserManagement/Dashboard/TransactionLines.html', {"item_pk": item_pk,
                                                                             "transaction_summary_lines_table":transaction_summary_lines_table})
