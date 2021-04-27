from django.contrib.auth.models import User
from UserManagement import models as user_management_models
from Core import models as core_models
from rest_framework import serializers
from Core.models import FieldValidationMapping, ValidationRule
from .validators import convert_date_formats
import json

class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = user_management_models.Profile
        fields = ('user','birth_date', 'location','reg_id')


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'profile')


class TokenSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = user_management_models.TokenModel
        fields = ('key', 'user')  # there I add the `user` field ( this is my need data ).


class TransactionSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.TransactionSummary
        fields = '__all__'


class ServiceReceivedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.ServiceReceivedItems
        fields = ('service_received', 'department_name','department_id', 'patient_id', 'gender', 'date_of_birth',
                  'med_svc_code', 'icd_10_code', 'service_date','service_provider_ranking_id','visit_type' )


class ServiceReceivedSerializer(serializers.ModelSerializer):
    items = ServiceReceivedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.ServiceReceived
        fields = ('org_name','facility_hfr_code','items')


class IncomingServiceReceivedItemsSerializer(serializers.Serializer):
    deptName = serializers.CharField(max_length=255)
    deptId = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    medSvcCode = serializers.CharField(max_length=255)
    icd10Code = serializers.CharField(max_length=255)
    serviceDate = serializers.CharField(max_length=255)
    serviceProviderRankingId = serializers.CharField(max_length=255)
    visitType = serializers.CharField(max_length=255)


class IncomingServicesReceivedSerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingServiceReceivedItemsSerializer(many=True, read_only=False)

    def validate(self, data):
        validate_received_payload(dict(data))
        return data



class DeathByDiseaseCaseAtFacilityItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.DeathByDiseaseCaseAtFacilityItems
        fields = ('death_by_disease_case_at_facility','ward_name','ward_id','patient_id',
                  'gender','date_of_birth','icd_10_code','date_death_occurred')


class DeathByDiseaseCaseAtFacilitySerializer(serializers.ModelSerializer):
    items = DeathByDiseaseCaseAtFacilityItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.DeathByDiseaseCaseAtFacility
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingDeathByDiseaseCaseAtTheFacilityItemsSerializer(serializers.Serializer):
    wardId = serializers.CharField(max_length=255)
    wardName = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255)
    icd10Code = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    dateDeathOccurred = serializers.CharField(max_length=255)


class IncomingDeathByDiseaseCaseAtTheFacilitySerializer(serializers.Serializer):
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingDeathByDiseaseCaseAtTheFacilityItemsSerializer(many=True, read_only=False)


class DeathByDiseaseCaseNotAtFacilityItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.DeathByDiseaseCaseNotAtFacilityItems
        fields = ('place_of_death_id','gender','date_of_birth','icd_10_code','date_death_occurred','death_id')


class DeathByDiseaseCaseNotAtFacilitySerializer(serializers.ModelSerializer):
    items = DeathByDiseaseCaseNotAtFacilityItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.DeathByDiseaseCaseNotAtFacility
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingDeathByDiseaseCaseNotAtTheFacilityItemsSerializer(serializers.Serializer):
    deathId = serializers.CharField(max_length=255)
    placeOfDeathId = serializers.CharField(max_length=255)
    icd10Code = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    dateDeathOccurred = serializers.CharField(max_length=255)


class IncomingDeathByDiseaseCaseNotAtTheFacilitySerializer(serializers.Serializer):
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingDeathByDiseaseCaseNotAtTheFacilityItemsSerializer(many=True, read_only=False)


class BedOccupancyItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.BedOccupancyItems
        fields = ('bed_occupancy','patient_id','admission_date','discharge_date','ward_name','ward_id')


class BedOccupancySerializer(serializers.ModelSerializer):
    items = BedOccupancyItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.BedOccupancy
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingBedOccupancyItemsSerializer(serializers.Serializer):
    wardId = serializers.CharField(max_length=255)
    wardName = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255)
    admissionDate = serializers.CharField(max_length=255)
    dischargeDate = serializers.CharField(max_length=255)


class IncomingBedOccupancySerializer(serializers.Serializer):
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingBedOccupancyItemsSerializer(many=True, read_only=False)


class RevenueReceivedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.RevenueReceivedItems
        fields = ('revenue_received','system_trans_id','transaction_date','patient_id', 'gender','date_of_birth',
                  'med_svc_code', 'payer_id','exemption_category_id','billed_amount','waived_amount','service_provider_ranking_id')


class RevenueReceivedSerializer(serializers.ModelSerializer):
    items = RevenueReceivedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.RevenueReceived
        fields = ('org_name', 'facility_hfr_code', 'items')


class IncomingRevenueReceivedItemsSerializer(serializers.Serializer):
    systemTransId = serializers.CharField(max_length=255)
    transactionDate = serializers.CharField(max_length=255)
    patId = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    dob = serializers.CharField(max_length=255)
    medSvcCode = serializers.CharField(max_length=255)
    payerId = serializers.IntegerField()
    exemptionCategoryId = serializers.IntegerField()
    billedAmount = serializers.IntegerField()
    waivedAmount = serializers.IntegerField()
    serviceProviderRankingId = serializers.IntegerField()


class IncomingRevenueReceivedSerializer(serializers.Serializer):
    messageType = serializers.CharField(max_length=255)
    orgName = serializers.CharField(max_length=255)
    facilityHfrCode = serializers.CharField(max_length=255)
    items = IncomingRevenueReceivedItemsSerializer(many=True, read_only=False)


def validate_received_payload(data):
    message_type = data["messageType"]
    org_name = data["orgName"]
    facility_hfr_code = data["facilityHfrCode"]
    data_items = data["items"]

    instance_transaction_summary = core_models.TransactionSummary()
    instance_transaction_summary.message_type = message_type
    instance_transaction_summary.org_name = org_name
    instance_transaction_summary.facility_hfr_code = facility_hfr_code
    instance_transaction_summary.save()

    for val in data_items:
        # for x in val.keys():
        rules = FieldValidationMapping.objects.filter(message_type=message_type)
        for rule in rules:
            field = rule.field
            predefined_rule = ValidationRule.objects.get(id=rule.validation_rule_id)
            rule_name = predefined_rule.rule_name

            # save object
            instance_transaction_summary_lines = core_models.TransactionSummaryLine()
            instance_transaction_summary_lines.transaction_id = instance_transaction_summary.id
            instance_transaction_summary_lines.payload_object = json.dumps(val)
            try:
                if rule_name == "convert_date_formats":
                    result = convert_date_formats(val[field])

                # update passed transaction number
                previous_transaction = core_models.TransactionSummary.objects.get(id=instance_transaction_summary.id)
                previous_transaction.total_passed +=1
                previous_transaction.save()

                # Save the object status
                instance_transaction_summary_lines.has_passed = True

            except ValueError as ve:
                # save failed object
                # update passed transaction number
                previous_transaction = core_models.TransactionSummary.objects.get(
                    id=instance_transaction_summary.id)
                previous_transaction.total_failed += 1
                previous_transaction.save()

                # Save the object status
                instance_transaction_summary_lines.has_failed = True
                instance_transaction_summary_lines.error_message = ve

            except KeyError as ke:
                # save failed object
                # update passed transaction number
                previous_transaction = core_models.TransactionSummary.objects.get(
                    id=instance_transaction_summary.id)
                previous_transaction.total_failed += 1
                previous_transaction.save()

                # Save the object status
                instance_transaction_summary_lines.has_failed = True
                instance_transaction_summary_lines.error_message = ke

            except RuntimeError as re:
                # save failed object
                # update passed transaction number
                previous_transaction = core_models.TransactionSummary.objects.get(
                    id=instance_transaction_summary.id)
                previous_transaction.total_failed += 1
                previous_transaction.save()

                # Save the object status
                instance_transaction_summary_lines.has_failed = True
                instance_transaction_summary_lines.error_message = re

            except TypeError as te:
                # save failed object
                # update passed transaction number
                previous_transaction = core_models.TransactionSummary.objects.get(
                    id=instance_transaction_summary.id)
                previous_transaction.total_failed += 1
                previous_transaction.save()

                # Save the object status
                instance_transaction_summary_lines.has_failed = True
                instance_transaction_summary_lines.error_message = te

            except NameError as ne:
                # save failed object
                # update passed transaction number
                previous_transaction = core_models.TransactionSummary.objects.get(
                    id=instance_transaction_summary.id)
                previous_transaction.total_failed += 1
                previous_transaction.save()

                # Save the object status
                instance_transaction_summary_lines.has_failed = True
                instance_transaction_summary_lines.error_message = ne


            instance_transaction_summary_lines.save()
