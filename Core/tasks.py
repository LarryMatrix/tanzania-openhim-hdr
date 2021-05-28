import requests
from celery import Celery
from Core import models as core_models
from API import validators as validators
from MasterData import models as master_data_models


app = Celery()

@app.task
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
        # if  validators.validate_received_payload(regenerate_services_received_json_payload(request,lines, message_type)) is False:
        #     return False
        # else:

        row = 0
        for line in lines:

            if row==0:
                headers = line
                row = row + 1
            else:
                # create a dictionary of student details
                transaction_id = line[1]

                new_line_details = {}
                for i in range(len(headers)):
                    new_line_details[headers[i]] = line[i]

                # save the transaction lines and message
                if message_type == "SVCREC":
                    transaction_id = line[1]

                    instance_service_received_items = core_models.ServiceReceivedItems()
                    instance_service_received_items.service_received_id = instance_service_received.id
                    instance_service_received_items.department_name = line[4]
                    instance_service_received_items.department_id = line[5]
                    instance_service_received_items.patient_id = line[6]
                    instance_service_received_items.gender = line[7]
                    instance_service_received_items.date_of_birth = validators.convert_date_formats(line[8])
                    instance_service_received_items.med_svc_code = line[9]
                    instance_service_received_items.icd_10_code = line[10]
                    instance_service_received_items.service_date = validators.convert_date_formats(line[11])
                    instance_service_received_items.service_provider_ranking_id = line[12]
                    instance_service_received_items.visit_type = line[13]
                    instance_service_received_items.save()

                    # Update transactions
                    update_transaction_summary(transaction_id)

                elif message_type == "DDC":
                    instance_death_by_disease_case_items = core_models.DeathByDiseaseCaseAtFacility()

                    instance_death_by_disease_case_items.death_by_disease_case_at_facility_id = instance_death_by_disease_case_at_facility.id
                    instance_death_by_disease_case_items.ward_name = line[5]
                    instance_death_by_disease_case_items.ward_id = line[4]
                    instance_death_by_disease_case_items.patient_id = line[6]
                    instance_death_by_disease_case_items.icd_10_code = line[7]
                    instance_death_by_disease_case_items.gender = line[8]
                    instance_death_by_disease_case_items.date_of_birth = line[9]
                    instance_death_by_disease_case_items.date_death_occurred = line[10]
                    instance_death_by_disease_case_items.save()

                    update_transaction_summary(transaction_id)

                elif message_type == "DDCOUT":
                    instance_death_by_disease_case_items_not_at_facility = core_models.DeathByDiseaseCaseNotAtFacilityItems()

                    instance_death_by_disease_case_items_not_at_facility.death_by_disease_case_not_at_facility_id = instance_death_by_disease_case_not_at_facility.id
                    instance_death_by_disease_case_items_not_at_facility.place_of_death_id = line[5]
                    instance_death_by_disease_case_items_not_at_facility.gender = line[4]
                    instance_death_by_disease_case_items_not_at_facility.date_of_birth = line[6]
                    instance_death_by_disease_case_items_not_at_facility.icd_10_code = line[7]
                    instance_death_by_disease_case_items_not_at_facility.date_death_occurred = line[8]
                    instance_death_by_disease_case_items_not_at_facility.death_id = line[9]
                    instance_death_by_disease_case_items_not_at_facility.save()

                    update_transaction_summary(transaction_id)

                elif message_type == "BEDOCC":
                    instance_bed_occupancy_items = core_models.BedOccupancyItems()

                    instance_bed_occupancy_items.bed_occupancy_id = instance_bed_occupancy.id
                    instance_bed_occupancy_items.patient_id = line(6)
                    instance_bed_occupancy_items.admission_date = line[7]
                    instance_bed_occupancy_items.discharge_date = line[8]
                    instance_bed_occupancy_items.ward_name = line[5]
                    instance_bed_occupancy_items.ward_id = line[4]
                    instance_bed_occupancy_items.save()

                    update_transaction_summary(transaction_id)

                elif message_type == "REV":
                    instance_revenue_received_items = core_models.RevenueReceivedItems()

                    instance_revenue_received_items.revenue_received_id = instance_revenue_received.id
                    instance_revenue_received_items.system_trans_id = line(4)
                    instance_revenue_received_items.transaction_date = line(5)
                    instance_revenue_received_items.patient_id = line[6]
                    instance_revenue_received_items.gender = line[7]
                    instance_revenue_received_items.date_of_birth = line[8]
                    instance_revenue_received_items.med_svc_code = line[9]
                    instance_revenue_received_items.payer_id = line[10]
                    instance_revenue_received_items.exemption_category_id = line[11]
                    instance_revenue_received_items.billed_amount = line[12]
                    instance_revenue_received_items.waived_amount = line[13]
                    instance_revenue_received_items.service_provider_ranking_id = line[14]
                    instance_revenue_received_items.save()

                    update_transaction_summary(transaction_id)

                else:
                    return False

            row = row + 1

    fp.close()

def update_transaction_summary(transaction_id):
    transaction = master_data_models.TransactionSummary.objects.get(id=transaction_id)
    transaction.total_passed += 1
    transaction.total_failed -= 1
    transaction.save()
