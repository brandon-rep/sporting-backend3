from rest_framework import serializers
from sporting_backend.models import (
    LawMaker,
    Profile,
    SportingReferrals,
    )

class PopUpProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
        )


class SportingReferralSerializer(serializers.ModelSerializer):
    page_views = serializers.IntegerField()
    profile = PopUpProfileSerializer()

    class Meta:
        model = SportingReferrals
        fields = (
            'page_views',
            'profile',
        )

