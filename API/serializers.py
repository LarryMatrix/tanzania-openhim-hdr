from django.contrib.auth.models import User
from UserManagement import models as user_management_models
from Core import models as core_models
from rest_framework import serializers


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


class DeathByDiseaseCaseAtFacilityItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.DeathByDiseaseCaseAtFacilityItems
        fields = '__all__'


class DeathByDiseaseCaseAtFacilitySerializer(serializers.ModelSerializer):
    items = DeathByDiseaseCaseAtFacilityItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.DeathByDiseaseCaseAtFacility
        fields = ('org_name', 'facility_hfr_code', 'items')


class DeathByDiseaseCaseNotAtFacilityItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.DeathByDiseaseCaseNotAtFacilityItems
        fields = '__all__'


class DeathByDiseaseCaseNotAtFacilitySerializer(serializers.ModelSerializer):
    items = DeathByDiseaseCaseNotAtFacilityItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.DeathByDiseaseCaseNotAtFacility
        fields = ('org_name', 'facility_hfr_code', 'items')


class BedOccupancyItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.BedOccupancyItems
        fields = '__all__'


class BedOccupancySerializer(serializers.ModelSerializer):
    items = BedOccupancyItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.BedOccupancy
        fields = ('org_name', 'facility_hfr_code', 'items')


class RevenueReceivedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.RevenueReceived
        fields = '__all__'


class RevenueReceivedSerializer(serializers.ModelSerializer):
    items = RevenueReceivedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = core_models.RevenueReceived
        fields = ('org_name', 'facility_hfr_code', 'items')

