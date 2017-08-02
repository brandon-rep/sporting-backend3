# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unidecode import unidecode
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import status
from sporting_backend.serializers import (
    SportingReferralSerializer
)
from sporting_backend.models import (
    Profile,
    Address,
    SportingReferrals,

    )
from sporting_backend.functions import (
    check_keys,
    who_is_my_law_maker
    )


@api_view(['GET'])
@permission_classes((AllowAny,))
def personal_info(request):
    if 'email' not in [unidecode(k) for k in request.query_params.keys()]:
        return Response(
            "Email missing from expected params",
            status=status.HTTP_400_BAD_REQUEST
        )
    email = unidecode(request.query_params['email'])
    try:
        sporting_referral = SportingReferrals.objects.get(profile__email=email)
    except ObjectDoesNotExist:
        return Response(
            "Referral or profile with that email does not exist",
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            'referral_hash': sporting_referral.profile.referral_hash.hashid,
            'page_views': sporting_referral.page_views
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes((AllowAny,))
def who_is_my(request):
    keys = [unidecode(k) for k in request.query_params.keys()]
    needed_keys = ['city', 'state', 'street_address']
    missing_key = check_keys(needed_keys, keys)
    if missing_key:
        return Response(
                "Missing " + missing_key + " from arguments",
                status=status.HTTP_400_BAD_REQUEST
        )
    street_address = request.query_params['street_address']
    city = request.query_params['city']
    state = request.query_params['state']
    results = who_is_my_law_maker(street_address, city, state)

    if results:
        return Response(results, status=status.HTTP_200_OK)
    else:
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def profile_leaderboard(request):
    if 'referral_hash' not in [unidecode(k) for k in request.data.keys()]:
        return Response(
            "referral_hash missing",
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.data['referral_hash']:
        try:
            referral_profile = Profile.objects.get(
                referral_hash=request.data['referral_hash']
            )
        except:
            referral_profile = None
        if referral_profile:
            referral_profile.sporting_referrals.increment_page_views()
            referral_profile.sporting_referrals.save()

    referrals = SportingReferrals.objects.all().order_by('-page_views')[:5]
    serialized_referrals = SportingReferralSerializer(referrals, many=True)
    return Response(serialized_referrals.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def district_leaderboard(request):
    law_makers_dict = {}
    for referral in SportingReferrals.objects.all():
        if referral.profile and referral.profile.address:
            law_maker = referral.profile.address.get_congress()
            if law_maker:
                if law_maker.bioguide_id in law_makers_dict.keys():
                    law_makers_dict[law_maker.bioguide_id]['engagements'] += 1
                else:
                    law_makers_dict[law_maker.bioguide_id] = {
                        'engagements': 1,
                        'first_name': law_maker.first_name,
                        'middle_name': law_maker.middle_name,
                        'last_name': law_maker.last_name,
                        'district': law_maker.district,
                        'state': law_maker.state
                    }
    serialized_dict = json.dumps(law_makers_dict)
    return HttpResponse(
        serialized_dict, content_type="application/json"
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    # varify correct arguments
    keys = [unidecode(k) for k in request.data.keys()]
    needed_keys = ['first_name', 'last_name', 'email', 'referral_hash']
    missing_key = check_keys(needed_keys, keys)
    if missing_key:
        return Response(
                "Missing " + missing_key + " from arguments",
                status=status.HTTP_400_BAD_REQUEST
            )
    if any(needed_key in keys for needed_key in ['city',
                                                 'state',
                                                 'street_address',
                                                 'apartment_number',
                                                 'zipcode']):
        # validate zipcode
        if any(not d.isdigit() for d in request.data['zipcode']):
            return Response(
                "Zipcode not number", status=status.HTTP_400_BAD_REQUEST
                )

        try:
            profile = Profile.objects.get(email=request.data['email'])
        except:
            return Response(
                "No user found to append address",
                status=status.HTTP_400_BAD_REQUEST
            )

        if profile is None:
            return Response(
                "No profile with that email",
                status=status.HTTP_400_BAD_REQUEST
            )

        address = Address(
            apartment_number=request.data['apartment_number'],
            street=request.data['street_address'],
            city=request.data['city'],
            state=request.data['state'],
            zipcode=request.data['zipcode'],
        )
        address.save()
        profile.address = address
        profile.save()

        if request.data['referral_hash']:
            try:
                referral_profile = Profile.objects.get(
                    referral_hash=request.data['referral_hash']
                )
            except:
                referral_profile = None
            if referral_profile:
                profile.sporting_referrals.referred = referral_profile.sporting_referrals   # NOQA
                profile.sporting_referrals.save()

        return Response(
            {'referral_hash': profile.referral_hash.hashid},
            status=status.HTTP_201_CREATED
        )

    else:
        if Profile.objects.filter(
            email=request.data['email'], sporting_referrals__isnull=False
        ):
            return Response(
                "Email already used", status=status.HTTP_400_BAD_REQUEST
            )

        else:
            profile = Profile.objects.create(
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email=request.data['email'],
                referral_hash=request.data['referral_hash']
            )
            sporting_referral = SportingReferrals(profile=profile)
            sporting_referral.save()
            return Response(
                "Profile Created without Address",
                status=status.HTTP_201_CREATED
            )
