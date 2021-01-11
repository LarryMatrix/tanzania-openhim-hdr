from django.contrib.auth.models import User
from MasterData import models as master_data_models
from UserManagement import models as user_management_models
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


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.Client
        fields = '__all__'


class ClientMetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.ClientMetadata
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.Event
        fields = '__all__'


class EventMetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.EventMetadata
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.Location
        fields = '__all__'


class LocationMetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.LocationMetadata
        fields = '__all__'


class HdrClientSerializer(serializers.Serializer):
    openHimClientId = serializers.CharField()
    name = serializers.CharField()


class HdrEventSerializer(serializers.Serializer):
    eventType = serializers.CharField()
    eventDate = serializers.CharField()
    openHimClientId = serializers.CharField()
    mediatorVersion = serializers.CharField()
    payload = serializers.JSONField()


class ClientEventSerializer(serializers.Serializer):
    hdrClient = HdrClientSerializer(many=False, read_only=False)
    hdrEvents = HdrEventSerializer(many=True, read_only=False)

    class Meta:
        fields = ('hdrClient', 'hdrEvents')