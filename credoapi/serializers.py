from rest_framework import serializers
from credoapi.models import Device, User, Detection, Team
from credoapi.helpers import Frame, Header, Body, KeyInfo


class DeviceInfoSerializer(serializers.Serializer):
    deviceId = serializers.CharField(max_length=50)
    deviceModel = serializers.CharField(max_length=50)
    androidVersion = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return Device(
            device_id=validated_data.get('deviceId'),
            device_model=validated_data.get('deviceModel'),
            android_version=validated_data.get('androidVersion')
        )

    def update(self, instance, validated_data):
        instance.device_id = validated_data.get('deviceId', instance.device_id)
        instance.device_model = validated_data.get('deviceModel', instance.device_model)
        instance.android_version = validated_data.get('androidVersion', instance.android_version)


class UserInfoSerializer(serializers.Serializer):
    team = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=50)
    key = serializers.CharField(max_length=20, required=False)

    def create(self, validated_data):
        # TODO: handle team
        return User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            key=validated_data.get('key')
        )

    def update(self, instance, validated_data):
        instance.team = validated_data.get('team', instance.team)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.key = validated_data.get('key', instance.key)


class KeyInfoSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return KeyInfo(
            key=validated_data.get('key')
        )

    def update(self, instance, validated_data):
        instance.key = validated_data.get('key', instance.key)


class DetectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    accuracy = serializers.FloatField()
    altitude = serializers.FloatField()
    frame_content = serializers.CharField(max_length=5000)
    height = serializers.FloatField()
    width = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    provider = serializers.CharField(max_length=20)
    timestamp = serializers.IntegerField()

    def create(self, validated_data):
        return Detection(
            d_id=validated_data.get('id'),
            accuracy=validated_data.get('accuracy'),
            altitude=validated_data.get('altitude'),
            frame_content=validated_data.get('frame_content'),
            height=validated_data.get('height'),
            width=validated_data.get('width'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            provider=validated_data.get('provider'),
            timestamp=validated_data.get('timestamp')
        )

    def update(self, instance, validated_data):
        instance.d_id = validated_data.get('id', instance.d_id)
        instance.accuracy = validated_data.get('accuracy', instance.accuracy)
        instance.altitude = validated_data.get('altitude', instance.altitude)
        instance.frame_content = validated_data.get('frame_content', instance.frame_content)
        instance.height = validated_data.get('height', instance.height)
        instance.width = validated_data.get('width', instance.width)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.provider = validated_data.get('provider', instance.provider)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)


# Body

class BodySerializer(serializers.Serializer):
    device_info = DeviceInfoSerializer(required=False)
    user_info = UserInfoSerializer(required=False)
    key_info = KeyInfoSerializer(required=False)
    detection = DetectionSerializer(required=False)

    def create(self, validated_data):
        return Body(**validated_data)

    def update(self, instance, validated_data):
        instance.device_info = validated_data.get('device_info', instance.device_info)
        instance.user_info = validated_data.get('user_info', instance.user_info)
        instance.key_info = validated_data.get('key_info', instance.key_info)
        instance.detection = validated_data.get('detection', instance.detection)


# Header

class HeaderSerializer(serializers.Serializer):
    application = serializers.CharField(max_length=10)
    frame_type = serializers.CharField(max_length=10)
    protocol = serializers.CharField(max_length=10)
    time_stamp = serializers.IntegerField()

    def create(self, validated_data):
        return Header(**validated_data)

    def update(self, instance, validated_data):
        instance.application = validated_data.get('application', instance.application)
        instance.frame_type = validated_data.get('frame_type', instance.frame_type)
        instance.protocol = validated_data.get('protocol', instance.protocol)
        instance.time_stamp = validated_data.get('time_stamp', instance.time_stamp)


# Frame

class FrameSerializer(serializers.Serializer):
    #TODO: add validation of required fields, based on frametype
    header = HeaderSerializer()
    body = BodySerializer()

    def create(self, validated_data):
        return Frame(**validated_data)

    def update(self, instance, validated_data):
        instance.header = validated_data.get('header', instance.header)
        instance.body = validated_data.get('body', instance.body)

    # validate if body has all required fields
    # check if key is provided