# from rest_framework import viewsets, status, generics
# from rest_framework.response import Response
# from .serializers import ClientMetadataSerializer, \
#     EventSerializer, EventMetadataSerializer, LocationSerializer, LocationMetadataSerializer, ClientEventSerializer
# from MasterData.models import Client, Event, ClientMetadata, EventMetadata,Location, LocationMetadata
# import dateutil.parser
# import json
#
#
# # Create your views here.
# class ClientMetadataView(viewsets.ModelViewSet):
#     queryset = ClientMetadata.objects.all()
#     serializer_class = ClientMetadataSerializer
#     permission_classes = ()
#
#
# class EventView(viewsets.ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = ()
#
#
# class EventMetadataView(viewsets.ModelViewSet):
#     queryset = EventMetadata.objects.all()
#     serializer_class = EventMetadataSerializer
#     permission_classes = ()
#
#
# class LocationView(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer
#     permission_classes = ()
#
#
# class LocationMetadataView(viewsets.ModelViewSet):
#     queryset = LocationMetadata.objects.all()
#     serializer_class = LocationMetadataSerializer
#     permission_classes = ()
#
#
# class ClientEventView(generics.CreateAPIView):
#     serializer_class = ClientEventSerializer
#     # permission_classes = ()
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         if isinstance(data, list):
#             serializer = self.get_serializer(data=request.data, many=True)
#         else:
#             serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(self.perform_create(request, serializer))
#
#     def perform_create(self, request, serializer):
#         client_data = serializer.data["hdrClient"]
#         event_data = serializer.data["hdrEvents"]
#
#         # Store in clients table
#         instance_client = Client()
#
#         instance_client.json = client_data
#         instance_client.save()
#
#         # Store in client metadata
#         instance_client_metadata = ClientMetadata()
#
#         instance_client_metadata.client_id = instance_client.id
#         instance_client_metadata.open_him_client_id = client_data["openHimClientId"]
#         instance_client_metadata.name = client_data["name"]
#         instance_client_metadata.save()
#
#         # Store in event
#
#         for x in json.loads(json.dumps(event_data)):
#             instance_event_metadata = EventMetadata()
#             instance_event = Event()
#
#             instance_event.json = x
#             instance_event.save()
#
#             instance_event_metadata.event_id = instance_event.id
#             instance_event_metadata.event_type = x["eventType"]
#             event_date_time = dateutil.parser.parse(x["eventDate"])
#             instance_event_metadata.event_date = event_date_time
#             instance_event_metadata.open_him_client_id = x["openHimClientId"]
#             instance_event_metadata.mediator_version = x["mediatorVersion"]
#             instance_event_metadata.save()
#
#         return status.HTTP_200_OK
#
#
#
#
