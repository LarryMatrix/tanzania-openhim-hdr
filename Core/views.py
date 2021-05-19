import csv
import json
from .models import TransactionSummaryLine
from django.http import HttpResponse
from .forms import PayloadImportForm, CPTCodeMappingImportForm
from django.shortcuts import render, redirect
from MasterData import models as master_data_models
from Core import models as core_models
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from API import validators as validators
from API import serializers as api_serializers
from  collections import OrderedDict
import asyncio
from asgiref.sync import sync_to_async


# Create your views here.
def convert_to_csv(request):
    if request.method == "POST":
        transaction_id = request.POST["item_pk"]
        transaction_lines = TransactionSummaryLine.objects.filter(transaction_id = transaction_id)
        model_fields = TransactionSummaryLine._meta.fields + TransactionSummaryLine._meta.many_to_many
        field_names = [field.name for field in model_fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response, delimiter=",")
        fields = []
        # Write a first row with header information

        json_object = transaction_lines.first().payload_object

        jsonObject = json.loads(json_object)
        for key in jsonObject:
            fields.append(key)
        writer.writerow(fields)

        for row in transaction_lines:
            json_object = row.payload_object
            values = []
            fields = []
            # for field in field_names:
            jsonObject = json.loads(json_object)
            for key in jsonObject:
                value = jsonObject[key]
                fields.append(key)
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(value)
            writer.writerow(values)
        data = response

        return  HttpResponse(data, content_type='text/csv')


@sync_to_async
def download_cpt_codes_as_csv(request):
    queryset = master_data_models.CPTCode.objects.all()
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=CPTCodesMappings.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    field_names.append('local_code')
    # Write a first row with header information
    writer.writerow(field_names)

    field_names.remove('local_code')

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


def upload_payload(request):
    if request.method == "POST":
        payload_import_form = PayloadImportForm(request.POST, request.FILES)
        if payload_import_form.is_valid():
            payload_import_form.full_clean()
            message_type = payload_import_form.cleaned_data['message_type']

            file = payload_import_form.cleaned_data['file']
            instance = master_data_models.Facility.objects.get(id=request.user.profile.facility_id)
            facility_name = instance.description
            facility_hfr_code = instance.facility_hfr_code

            if not file.name.endswith('.csv'):
                pass
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                save_payload_from_csv(request,file_path,message_type,facility_hfr_code,facility_name )
        return redirect(request.META['HTTP_REFERER'])

def upload_cpt_codes(request):
    if request.method == "POST":
        cpt_codes_import_form = CPTCodeMappingImportForm(request.POST, request.FILES)
        if cpt_codes_import_form.is_valid():
            cpt_codes_import_form.full_clean()

            file = cpt_codes_import_form.cleaned_data['file']
            instance = master_data_models.Facility.objects.get(id=request.user.profile.facility_id)
            facility_hfr_code = instance.facility_hfr_code
            facility_id = request.user.profile.facility_id

            if not file.name.endswith('.csv'):
                pass
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                save_cpt_code_entries(file_path, facility_id, facility_hfr_code)
        return redirect(request.META['HTTP_REFERER'])


def save_cpt_code_entries(file_path, facility_id, facility_hfr_code):
    # Delete all previous mappings

    instance_previous_mappings = master_data_models.CPTCodesMapping.objects.filter(facility_id=facility_id)
    instance_previous_mappings.delete()

    with open(file_path, 'r') as fp:
        lines = csv.reader(fp, delimiter=',')
        row = 0
        for line in lines:
            print(line)
            if line is not None:
                if row == 0:
                    headers = line
                    row = row + 1
                else:
                    instance_cpt_code_mappings = master_data_models.CPTCodesMapping()
                    instance_cpt_code_mappings.cpt_code_id = line[0]
                    instance_cpt_code_mappings.local_code = line[4]
                    instance_cpt_code_mappings.facility_id = facility_id

                    instance_cpt_code_mappings.save()

                row = row + 1
        fp.close()


def save_payload_from_csv(request,file_path, message_type, facility_hfr_code, facility_name):
    # Service received parents lines
    if message_type == "SVCREC":
        instance_service_received = core_models.ServiceReceived()
        instance_service_received.org_name = facility_name
        instance_service_received.facility_hfr_code = facility_hfr_code
        instance_service_received.save()
    # Death by Facility in facility parent lines
    if message_type == "DDC":
        instance_death_by_disease_case_at_facility = core_models.DeathByDiseaseCaseAtFacility()
        instance_death_by_disease_case_at_facility.org_name = facility_name
        instance_death_by_disease_case_at_facility.facility_hfr_code = facility_hfr_code
        instance_death_by_disease_case_at_facility.save()
    # Death by Disease Case Out of Faciity lines
    if message_type == "DDCOUT":
        instance_death_by_disease_case_not_at_facility = core_models.DeathByDiseaseCaseNotAtFacility()
        instance_death_by_disease_case_not_at_facility.org_name = facility_name
        instance_death_by_disease_case_not_at_facility.facility_hfr_code = facility_hfr_code
        instance_death_by_disease_case_not_at_facility.save()
        # Bed Occupany parent lines
    if message_type == "BEDOCC":
        instance_bed_occupancy = core_models.BedOccupancy()
        instance_bed_occupancy.org_name = facility_name
        instance_bed_occupancy.facility_hfr_code = facility_hfr_code
        instance_bed_occupancy.save()
    # Revenue received parent lines
    if message_type == "REV":
        instance_revenue_received = core_models.RevenueReceived()
        instance_revenue_received.org_name = facility_name
        instance_revenue_received.facility_hfr_code = facility_hfr_code
        instance_revenue_received.save()

    # open csv file, read lines
    with open(file_path, 'r') as fp:
        lines = csv.reader(fp, delimiter=',')
        # print(regenerate_services_received_json_payload(request, lines, message_type))
        if False in validators.validate_received_payload(regenerate_services_received_json_payload(request,lines, message_type)):
            return False
        else:
            row = 0
            for line in lines:

                if row==0:
                    headers = line
                    row = row + 1
                else:
                    # create a dictionary of student details
                    new_line_details = {}
                    for i in range(len(headers)):
                        new_line_details[headers[i]] = line[i]

                    # save the transaction lines and message
                    if message_type == "SVCREC":
                        instance_service_received_items = core_models.ServiceReceivedItems()
                        instance_service_received_items.service_received_id = instance_service_received.id
                        instance_service_received_items.department_name = line[0]
                        instance_service_received_items.department_id = line[1]
                        instance_service_received_items.patient_id = line[2]
                        instance_service_received_items.gender = line[3]
                        instance_service_received_items.date_of_birth = validators.convert_date_formats(line[4])
                        instance_service_received_items.med_svc_code = line[5]
                        instance_service_received_items.icd_10_code = line[6]
                        instance_service_received_items.service_date = validators.convert_date_formats(line[7])
                        instance_service_received_items.service_provider_ranking_id = line[8]
                        instance_service_received_items.visit_type = line[9]
                        instance_service_received_items.save()
                    else:
                        return False
                row = row + 1
        fp.close()


def regenerate_services_received_json_payload(request,lines, message_type):
    data_items_array = []
    instance = master_data_models.Facility.objects.get(id=request.user.profile.facility_id)
    facility_name = instance.description
    facility_hfr_code = instance.facility_hfr_code

    for line in lines:
        json_object = {"deptName": line[0], "deptId": line[1],
                       "patId": line[2],
                       "gender": line[3],
                       "dob": line[4],
                       "medSvcCode": line[5],
                       "icd10Code": line[6],
                       "serviceDate": line[7],
                       "serviceProviderRankingId": line[8],
                       "visitType": line[9]
                       }

        data_items_array.append(json_object)

    parent_object = {
        "messageType": "" + message_type + "",
        "orgName": "" + facility_name + "",
        "facilityHfrCode": "" + facility_hfr_code + "",
        "items": data_items_array
    }

    final_array = json.dumps(parent_object)

    return final_array

