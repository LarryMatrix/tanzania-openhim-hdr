from rest_framework import viewsets, status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .serializers import TransactionSummarySerializer, IncomingDeathByDiseaseCaseAtTheFacilitySerializer, \
    DeathByDiseaseCaseAtFacilityItemsSerializer, \
    DeathByDiseaseCaseNotAtFacilityItemsSerializer, RevenueReceivedItemsSerializer,BedOccupancyItemsSerializer, \
    ServiceReceivedItemsSerializer, IncomingDeathByDiseaseCaseNotAtTheFacilitySerializer, \
    IncomingServicesReceivedSerializer, IncomingBedOccupancySerializer, IncomingRevenueReceivedSerializer
from Core.models import TransactionSummary, RevenueReceived, DeathByDiseaseCaseAtFacility, \
    DeathByDiseaseCaseNotAtFacility,ServiceReceived, BedOccupancy, RevenueReceivedItems, ServiceReceivedItems, \
    DeathByDiseaseCaseAtFacilityItems, DeathByDiseaseCaseNotAtFacilityItems, BedOccupancyItems

from . import validators

# Create your views here.
class TransactionSummaryView(viewsets.ModelViewSet):
    queryset = TransactionSummary.objects.all()
    serializer_class = TransactionSummarySerializer
    permission_classes = ()


class ServiceReceivedView(viewsets.ModelViewSet):
    queryset = ServiceReceived.objects.all()
    serializer_class = IncomingServicesReceivedSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if False in validators.validate_received_payload(dict(serializer.data)):
                headers = self.get_exception_handler(serializer.data)
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, headers=headers)
            else:
                status_array = self.perform_create(request, serializer)

                if 400 in status_array:
                    headers = self.get_exception_handler(serializer.data)
                    headers = status.HTTP_400_BAD_REQUEST
                    response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                else:
                    headers = self.get_success_headers(serializer.data)
                    response = {"message": "Success", "status": status.HTTP_201_CREATED}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):

        # validate payload
        instance_service_received = ServiceReceived()

        instance_service_received.org_name = serializer.data["orgName"]
        instance_service_received.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_service_received.save()

        status = []

        for val in serializer.data["items"]:
            try:
                instance_service_received_item = ServiceReceivedItems()

                instance_service_received_item.service_received_id= instance_service_received.id
                instance_service_received_item.department_name = val["deptName"]
                instance_service_received_item.department_id = val["deptId"]
                instance_service_received_item.patient_id = val["patId"]
                instance_service_received_item.gender = val["gender"]
                instance_service_received_item.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_service_received_item.med_svc_code = val["medSvcCode"]
                instance_service_received_item.icd_10_code = val["icd10Code"]
                instance_service_received_item.service_date = validators.convert_date_formats(val["serviceDate"])
                instance_service_received_item.service_provider_ranking_id = val["serviceProviderRankingId"]
                instance_service_received_item.visit_type = val["visitType"]

                instance_service_received_item.save()

                status_code = 200
                status.append(status_code)

            except:
                ServiceReceived.objects.get(id=instance_service_received.id).delete()
                status_code = 400
                status.append(status_code)

        return  status


    def list(self, request):
        queryset = ServiceReceivedItems.objects.all().order_by('-id')
        serializer = ServiceReceivedItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class DeathByDiseaseCaseAtFacilityView(viewsets.ModelViewSet):
    queryset = DeathByDiseaseCaseAtFacility.objects.all()
    serializer_class = IncomingDeathByDiseaseCaseAtTheFacilitySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if False in validators.validate_received_payload(dict(serializer.data)):
                headers = self.get_success_headers(serializer.data)
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, headers=headers)
            else:
                status_array = self.perform_create(request, serializer)
                headers = self.get_success_headers(serializer.data)
                if 400 in status_array:
                    response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                else:
                    response = {"message": "Success", "status": status.HTTP_201_CREATED}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):

        # validate payload
        instance_death_by_disease_case_at_facility = DeathByDiseaseCaseAtFacility()

        instance_death_by_disease_case_at_facility.org_name = serializer.data["orgName"]
        instance_death_by_disease_case_at_facility.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_death_by_disease_case_at_facility.save()

        status = []

        for val in serializer.data["items"]:
            # validate payload
            try:
                instance_death_by_disease_case_at_facility_item = DeathByDiseaseCaseAtFacilityItems()

                instance_death_by_disease_case_at_facility_item.death_by_disease_case_at_facility_id = instance_death_by_disease_case_at_facility.id
                instance_death_by_disease_case_at_facility_item.ward_name = val["wardName"]
                instance_death_by_disease_case_at_facility_item.ward_id = val["wardId"]
                instance_death_by_disease_case_at_facility_item.patient_id = val["patId"]
                instance_death_by_disease_case_at_facility_item.gender = val["gender"]
                instance_death_by_disease_case_at_facility_item.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_death_by_disease_case_at_facility_item.icd_10_code = val["icd10Code"]
                instance_death_by_disease_case_at_facility_item.date_death_occurred = validators.convert_date_formats(val["dateDeathOccurred"])

                instance_death_by_disease_case_at_facility_item.save()

                status_code = 200
                status.append(status_code)
            except:
                ServiceReceived.objects.get(id=instance_death_by_disease_case_at_facility.id).delete()
                status_code = 400
                status.append(status_code)

        return status

    def list(self, request):
        queryset = DeathByDiseaseCaseAtFacilityItems.objects.all().order_by('-id')
        serializer = DeathByDiseaseCaseAtFacilityItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class DeathByDiseaseCaseNotAtFacilityView(viewsets.ModelViewSet):
    queryset = DeathByDiseaseCaseNotAtFacility.objects.all()
    serializer_class = IncomingDeathByDiseaseCaseNotAtTheFacilitySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if False in validators.validate_received_payload(dict(serializer.data)):
                headers = self.get_success_headers(serializer.data)
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, headers=headers)
            else:
                status_array = self.perform_create(request, serializer)
                headers = self.get_success_headers(serializer.data)
                if 400 in status_array:
                    response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                else:
                    response = {"message": "Success", "status": status.HTTP_201_CREATED}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):
        # validate payload
        instance_death_by_disease_case_not_at_facility = DeathByDiseaseCaseNotAtFacility()

        instance_death_by_disease_case_not_at_facility.org_name = serializer.data["orgName"]
        instance_death_by_disease_case_not_at_facility.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_death_by_disease_case_not_at_facility.save()

        status = []
        for val in serializer.data["items"]:
            # validate payload
            try:
                instance_death_by_disease_case_not_at_facility_items = DeathByDiseaseCaseNotAtFacilityItems()

                instance_death_by_disease_case_not_at_facility_items.place_of_death_id = val["placeOfDeathId"]
                instance_death_by_disease_case_not_at_facility_items.gender = val["gender"]
                instance_death_by_disease_case_not_at_facility_items.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_death_by_disease_case_not_at_facility_items.icd_10_code = val["icd10Code"]
                instance_death_by_disease_case_not_at_facility_items.date_death_occurred = validators.convert_date_formats(val["dateDeathOccurred"])
                instance_death_by_disease_case_not_at_facility_items.death_id = val["deathId"]

                instance_death_by_disease_case_not_at_facility_items.save()
                status_code = 200
                status.append(status_code)
            except:
                ServiceReceived.objects.get(id=instance_death_by_disease_case_not_at_facility.id).delete()
                status_code = 400
                status.append(status_code)

        return status

    def list(self, request):
        queryset = DeathByDiseaseCaseNotAtFacilityItems.objects.all().order_by('-id')
        serializer = DeathByDiseaseCaseNotAtFacilityItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class RevenueReceivedView(viewsets.ModelViewSet):
    queryset = RevenueReceived.objects.all()
    serializer_class = IncomingRevenueReceivedSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if False in validators.validate_received_payload(dict(serializer.data)):
                headers = self.get_success_headers(serializer.data)
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, headers=headers)
            else:
                status_array = self.perform_create(request, serializer)
                headers = self.get_success_headers(serializer.data)
                if 400 in status_array:
                    response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                else:
                    response = {"message": "Success", "status": status.HTTP_201_CREATED}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):
        # validate payload
        instance_revenue_received = RevenueReceived()

        instance_revenue_received.org_name = serializer.data["orgName"]
        instance_revenue_received.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_revenue_received.save()

        status = []
        for val in serializer.data["items"]:
            # validate payload
            try:
                instance_revenue_received_items = RevenueReceivedItems()

                instance_revenue_received_items.system_trans_id = val["systemTransId"]
                instance_revenue_received_items.transaction_date = validators.convert_date_formats(val["transactionDate"])
                instance_revenue_received_items.patient_id = val["patId"]
                instance_revenue_received_items.gender = val["gender"]
                instance_revenue_received_items.date_of_birth = validators.convert_date_formats(val["dob"])
                instance_revenue_received_items.med_svc_code = val["medSvcCode"]
                instance_revenue_received_items.payer_id = val["payerId"]
                instance_revenue_received_items.exemption_category_id = val["exemptionCategoryId"]
                instance_revenue_received_items.billed_amount = val["billedAmount"]
                instance_revenue_received_items.waived_amount = val["waivedAmount"]
                instance_revenue_received_items.service_provider_ranking_id = val["serviceProviderRankingId"]

                instance_revenue_received_items.save()
                status_code = 200
                status.append(status_code)
            except:
                ServiceReceived.objects.get(id=instance_revenue_received.id).delete()
                status_code = 400
                status.append(status_code)

    def list(self, request):
        queryset = RevenueReceivedItems.objects.all().order_by('-id')
        serializer = RevenueReceivedItemsSerializer(queryset, many=True)
        return Response(serializer.data)


class BedOccupancyView(viewsets.ModelViewSet):
    queryset = BedOccupancy.objects.all()
    serializer_class = IncomingBedOccupancySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if False in validators.validate_received_payload(dict(serializer.data)):
                headers = self.get_success_headers(serializer.data)
                response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                return Response(response, headers=headers)
            else:
                status_array = self.perform_create(request, serializer)
                headers = self.get_success_headers(serializer.data)
                if 400 in status_array:
                    response = {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}
                else:
                    response = {"message": "Success", "status": status.HTTP_201_CREATED}

                return Response(response, headers=headers)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, request, serializer):

        # validate payload
        instance_bed_occupancy = BedOccupancy()

        instance_bed_occupancy.org_name = serializer.data["orgName"]
        instance_bed_occupancy.facility_hfr_code = serializer.data["facilityHfrCode"]
        instance_bed_occupancy.save()

        status = []
        for val in serializer.data["items"]:
            # validate payload
            try:

                instance_bed_occupancy_item = BedOccupancyItems()
                instance_bed_occupancy_item.patient_id = val["patId"]
                instance_bed_occupancy_item.admission_date = validators.convert_date_formats(val["admissionDate"])
                instance_bed_occupancy_item.discharge_date = validators.convert_date_formats(val["dischargeDate"])
                instance_bed_occupancy_item.ward_name = val["wardName"]
                instance_bed_occupancy_item.ward_id = val["wardId"]

                instance_bed_occupancy_item.save()
                status_code = 200
                status.append(status_code)
            except:
                ServiceReceived.objects.get(id=instance_bed_occupancy.id).delete()
                status_code = 400
                status.append(status_code)

        return status

    def list(self, request):
        queryset = BedOccupancyItems.objects.all().order_by('-id')
        serializer = BedOccupancyItemsSerializer(queryset, many=True)
        return Response(serializer.data)






