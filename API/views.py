from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .serializers import TransactionSummarySerializer, ServiceReceivedSerializer, \
    DeathByDiseaseCaseAtFacilitySerializer, DeathByDiseaseCaseNotAtFacilitySerializer, \
    RevenueReceivedSerializer, BedOccupancySerializer
from Core.models import TransactionSummary, RevenueReceived, DeathByDiseaseCaseAtFacility, \
    DeathByDiseaseCaseNotAtFacility,ServiceReceived, BedOccupancy, RevenueReceivedItems, ServiceReceivedItems, \
    DeathByDiseaseCaseAtFacilityItems, DeathByDiseaseCaseNotAtFacilityItems, BedOccupancyItems
from django.db import IntegrityError


# Create your views here.
class TransactionSummaryView(viewsets.ModelViewSet):
    queryset = TransactionSummary.objects.all()
    serializer_class = TransactionSummarySerializer
    permission_classes = ()


class ServiceReceivedView(viewsets.ModelViewSet):
    queryset = ServiceReceived.objects.all()
    serializer_class = ServiceReceivedSerializer
    permission_classes = ()

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=False):
                self.perform_create(request, serializer)
                headers = self.get_success_headers(serializer.data)
        except IntegrityError:
            # save transaction logs
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, request, serializer):

            # validate payload
            instance_service_received = ServiceReceived()
            instance_service_received.org_name = serializer.data["orgName"]
            instance_service_received.facility_hfr_code = serializer.data["facilityHfrCode"]
            instance_service_received.save()

            for x in range(0, len(serializer.data["items"])):
                instance = ServiceReceivedItems()
                instance.service_received_id= instance_service_received.id
                instance.department_name = serializer.data[x]["deptName"]
                instance.department_id = serializer.data[x]["deptId"]
                instance.patient_id = serializer.data[x]["patId"]
                instance.gender = serializer.data[x]["gender"]
                instance.date_of_birth = serializer.data[x]["dob"]
                instance.med_svc_code = serializer.data[x]["medSvcCode"]
                instance.icd_10_code = serializer.data[x]["icd10Code"]
                instance.service_date = serializer.data[x]["serviceDate"]
                instance.service_provider_ranking_id = serializer.data[x]["serviceProviderRankingId"]
                instance.visit_type = serializer.data[x]["visitType"]

                instance.save()


class DeathByDiseaseCaseAtFacilityView(viewsets.ModelViewSet):
    queryset = DeathByDiseaseCaseAtFacility.objects.all()
    serializer_class = DeathByDiseaseCaseAtFacilitySerializer
    permission_classes = ()

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, request, serializer):

        for x in range(0, len(serializer.data)):
            # validate payload
            instance = DeathByDiseaseCaseAtFacility()
            instance.org_name = serializer.data[x]["orgName"]
            instance.facility_hfr_code = serializer.data[x]["facilityHfrCode"]
            instance.ward_name = serializer.data[x]["wardName"]
            instance.ward_id = serializer.data[x]["wardId"]
            instance.patient_id = serializer.data[x]["patId"]
            instance.gender = serializer.data[x]["gender"]
            instance.date_of_birth = serializer.data[x]["dob"]
            instance.icd_10_code = serializer.data[x]["icd10Code"]
            instance.date_death_occurred = serializer.data[x]["dateDeathOccurred"]

            instance.save()


class DeathByDiseaseCaseNotAtFacilityView(viewsets.ModelViewSet):
    queryset = DeathByDiseaseCaseNotAtFacility.objects.all()
    serializer_class = DeathByDiseaseCaseNotAtFacilitySerializer
    permission_classes = ()

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, request, serializer):

        for x in range(0, len(serializer.data)):
            # validate payload
            instance = DeathByDiseaseCaseNotAtFacility()
            instance.org_name = serializer.data[x]["orgName"]
            instance.facility_hfr_code = serializer.data[x]["facilityHfrCode"]
            instance.place_of_death_id = serializer.data[x]["placeOfDeathId"]
            instance.gender = serializer.data[x]["gender"]
            instance.date_of_birth = serializer.data[x]["dob"]
            instance.icd_10_code = serializer.data[x]["icd10Code"]
            instance.date_death_occurred = serializer.data[x]["dateDeathOccurred"]
            instance.death_id = serializer.data[x]["deathId"]

            instance.save()


class RevenueReceivedView(viewsets.ModelViewSet):
    queryset = RevenueReceived.objects.all()
    serializer_class = RevenueReceivedSerializer
    permission_classes = ()

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, request, serializer):

        for x in range(0, len(serializer.data)):
            # validate payload
            instance = RevenueReceived()
            instance.system_trans_id = serializer.data[x]["systemTransId"]
            instance.org_name = serializer.data[x]["orgName"]
            instance.facility_hfr_code = serializer.data[x]["facilityHfrCode"]
            instance.tra = serializer.data[x]["transactionDate"]
            instance.patient_id = serializer.data[x]["patId"]
            instance.date_of_birth = serializer.data[x]["dob"]
            instance.med_svc_code = serializer.data[x]["medSvcCode"]
            instance.payer_id = serializer.data[x]["payerId"]
            instance.exemption_category_id = serializer.data[x]["exemptionCategoryId"]
            instance.billed_amount = serializer.data[x]["billedAmount"]
            instance.waived_amount = serializer.data[x]["waivedAmount"]
            instance.service_provider_ranking_id = serializer.data[x]["serviceProviderRankingId"]

            instance.save()


class BedOccupancyView(viewsets.ModelViewSet):
    queryset = BedOccupancy.objects.all()
    serializer_class = BedOccupancySerializer
    permission_classes = ()

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, request, serializer):

        for x in range(0, len(serializer.data)):
            # validate payload
            instance = BedOccupancy()
            instance.org_name = serializer.data[x]["orgName"]
            instance.facility_hfr_code = serializer.data[x]["facilityHfrCode"]
            instance.patient_id = serializer.data[x]["patId"]
            instance.admission_date = serializer.data[x]["admissionDate"]
            instance.discharge_date = serializer.data[x]["dischargeDate"]
            instance.ward_name = serializer.data[x]["wardName"]
            instance.ward_id = serializer.data[x]["wardId"]

            instance.save()





