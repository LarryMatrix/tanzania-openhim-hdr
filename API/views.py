from rest_framework import viewsets, status, generics, permissions
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser, AllowAny
from django.db.models import Count, Sum
from django.conf import settings
from .serializers import ClientSerializer, ClientMetadataSerializer, \
    EventSerializer, EventMetadataSerializer, LocationSerializer, LocationMetadataSerializer, ClientEventSerializer
from MasterData.models import Event, Client, ClientMetadata, EventMetadata,Location, LocationMetadata


# Create your views here.
class ClientView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
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
            instance = master_data_models.HealthCommodityTransactions()
            instance.trans_date_time = serializer.data[x]["trans_date_time"]
            instance.quantity_available = serializer.data[x]["quantity_available"]
            instance.has_patients = serializer.data[x]["has_patients"]
            instance.stock_out_days = serializer.data[x]["stock_out_days"]
            instance.quantity_wasted = serializer.data[x]["quantity_wasted"]
            instance.quantity_consumed = serializer.data[x]["quantity_consumed"]
            instance.quantity_expired = serializer.data[x]["quantity_expired"]
            instance.number_of_clients = serializer.data[x]["number_of_clients"]
            instance.posting_schedule_id = serializer.data[x]["posting_schedule"]
            instance.user_created_id = serializer.data[x]["user_created"]
            instance.quantity_expired = serializer.data[x]["quantity_expired"]

            instance.save()

            query_transactions = master_data_models.HealthCommodityTransactions.objects.get(id=instance.id)

            query_posting_schedule = master_data_models.PostingSchedule.objects.get(id=query_transactions.
                                                                                    posting_schedule_id)
            query_posting_schedule.status = "posted"
            query_posting_schedule.save()

            query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.get \
                (id=query_transactions.posting_schedule.health_commodity_balance_id)

            query_health_commodity_balance.quantity_available = query_transactions.quantity_available
            query_health_commodity_balance.quantity_wasted = query_transactions.quantity_wasted
            query_health_commodity_balance.quantity_expired = query_transactions.quantity_expired
            query_health_commodity_balance.number_of_clients = query_transactions.number_of_clients
            query_health_commodity_balance.has_clients = query_transactions.has_patients
            query_health_commodity_balance.stock_out_days = query_transactions.stock_out_days
            query_health_commodity_balance.save()

            posting_schedule = serializer.data[x]["posting_schedule"]

            master_data_views.create_schedule_for_commodity_posted(posting_schedule)


class ClientMetadataView(viewsets.ModelViewSet):
    queryset = ClientMetadata.objects.all()
    serializer_class = ClientMetadataSerializer
    permission_classes = ()


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = ()


class EventMetadataView(viewsets.ModelViewSet):
    queryset = EventMetadata.objects.all()
    serializer_class = EventMetadataSerializer
    permission_classes = ()


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = ()


class LocationMetadataView(viewsets.ModelViewSet):
    queryset = LocationMetadata.objects.all()
    serializer_class = LocationMetadataSerializer
    permission_classes = ()


class ClientEventView(generics.CreateAPIView):
    serializer_class = ClientEventSerializer
    # permission_classes = ()

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(self.perform_create(request, serializer))

    def perform_create(self, request, serializer):
        client_data = serializer.data["hdrClient"]
        event_data = serializer.data["hdrEvents"]

        instance_client_metadata = ClientMetadata()
        instance_client_metadata.client_id = client_data["openHimClientId"]
        instance_client_metadata.name = client_data["name"]
        instance_client_metadata.save()

        for x in event_data:
            instance_event_metadata = EventMetadata()
            instance_event = Event()

            instance_event_metadata.event_type = x["eventType"]
            instance_event_metadata.event_date = x["eventDate"]
            instance_event_metadata.open_him_client_id = x["openHimClientId"]
            instance_event_metadata.mediator_version = x["mediatorVersion"]
            instance_event_metadata.save()

            instance_event.json = x["json"]
            instance_event.save()



