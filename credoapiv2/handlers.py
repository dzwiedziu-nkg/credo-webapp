# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

from django.db.utils import IntegrityError

from credoapi.helpers import generate_key
from credoapi.models import User, Team, Detection, Device

from credoapiv2.exceptions import CredoAPIException, RegistrationException, LoginException


def handle_registration(request):
    try:
        key = generate_key()
        while User.objects.filter(key=key).exists():
            key = generate_key()
        User.objects.create_user(
            team=Team.objects.get_or_create(name=request.data['team'])[0],
            display_name=request.data['display_name'],
            key=key,
            password=key,
            username=request.data['username'],
            email=request.data['email']
        )
        # TODO: Send email
    except IntegrityError:
        RegistrationException("User with given username or email already exists.")


def handle_login(request):
    pass


def handle_detection(request):
    Detection.objects.create(
        accuracy=request.data['accuracy'],
        altitude=request.data['altitude'],
        frame_content=base64.b64decode(request.data['frame_content']),
        height=request.data['height'],
        width=request.data['height'],
        d_id=request.data['id'],
        latitude=request.data['latitude'],
        longitude=request.data['longitude'],
        provider=request.data['provider'],
        timestamp=request.data['timestamp'],
        device=Device.objects.get_or_create(
            device_id=request.data['device_id'],
            device_model=request.data['device_model'],
            android_version=request.data['android_version'],
            user=request.user
        )[0],
        user=request.user
    )


def handle_ping(request):
    pass