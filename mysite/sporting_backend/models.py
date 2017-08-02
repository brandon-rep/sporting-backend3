from __future__ import unicode_literals

# Create your models here.

# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from unidecode import unidecode
from hashid_field import HashidField
from sporting_backend.functions import who_is_my_law_maker
from sporting_backend.enums import (
    Race,
    Verified,
    Gender,
    Party,
    Position,
    State,
    Status,
    Title,
)


class SportingReferrals(models.Model):
    page_views = models.PositiveIntegerField(default=0)
    sign_ups = models.PositiveIntegerField(default=0)
    profile = models.OneToOneField(
        'sporting_backend.Profile',
        on_delete=models.SET_NULL,
        related_name='sporting_referrals',
        null=True
    )
    referred = models.ForeignKey(
        'sporting_backend.SportingReferrals',
        on_delete=models.SET_NULL,
        related_name='referrals',
        null=True,
        blank=True
    )

    def increment_page_views(self):
        self.page_views += 1

    def __str__(self):
        return (
            self.profile.first_name + " "
            + self.profile.last_name + ": "
            + self.profile.email
        )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        null=True
    )
    first_name = models.CharField(
        max_length=32
    )
    last_name = models.CharField(
        max_length=32
    )
    middle_name = models.CharField(
        max_length=32
    )
    salutation = models.CharField(
        null=True,
        max_length=8
    )
    # picture = models.ImageField(
    #     upload_to='law_maker_profiles/',
    #     default='no_img.png'
    # )
    verified = models.IntegerField(
        choices=Verified,
        default=0
    )
    birthday = models.DateField(
        null=True
    )
    race = models.IntegerField(
        choices=Race,
        default=0,
        null=True
    )
    bio = models.CharField(
        max_length=256,
        default=""
    )
    address = models.OneToOneField(
        'sporting_backend.Address',
        related_name='user_profile',
        on_delete=models.CASCADE,
        null=True
    )
    email = models.EmailField(
        max_length=128,
        unique=True
    )
    from_pop_up = models.CharField(
        max_length=32,
        null=True
    )
    referral_hash = HashidField(
        min_length=4,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.first_name + " " + self.last_name + ": " + self.email

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        self.referral_hash = self.id
        super(Profile, self).save(update_fields=['referral_hash'])



class Address(models.Model):
    street = models.CharField(max_length=64)
    apartment_number = models.CharField(max_length=16, null=True)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    zipcode = models.CharField(max_length=5)
    district = models.CharField(max_length=8, null=True)
    senator_1 = models.ForeignKey(
        'sporting_backend.LawMaker',
        on_delete=models.SET_NULL,
        related_name='senator_1',
        null=True
    )
    senator_2 = models.ForeignKey(
        'sporting_backend.LawMaker',
        on_delete=models.SET_NULL,
        related_name='senator_2',
        null=True
    )
    congress_person = models.ForeignKey(
        'sporting_backend.LawMaker',
        on_delete=models.SET_NULL,
        related_name='congress_person',
        null=True
    )

    def get_congress(self):
        if self.congress_person:
            return self.congress_person
        else:
            return None

    def save(self, *args, **kwargs):
        super(Address, self).save(*args, **kwargs)
        if self.street and self.city and self.state:
            law_makers = who_is_my_law_maker(
                self.street, self.city, self.state
            )
            if not law_makers:
                return
            first_senator = True
            print(law_makers)
            print('law_makers')
            for lm in law_makers:
                if lm['district']:
                    self.district = unidecode(
                        lm['state']) + "-" + str(lm['district'])
                    print(lm['bioguide_id'])
                    self.congress_person = LawMaker.objects.get(
                        bioguide_id=lm['bioguide_id']
                    )
                elif first_senator and lm['district'] is None:
                    self.senator_1 = LawMaker.objects.get(
                        bioguide_id=lm['bioguide_id']
                    )
                    first_senator = False
                elif not first_senator and lm['district'] is None:
                    self.senator_2 = LawMaker.objects.get(
                        bioguide_id=lm['bioguide_id']
                    )
            super(Address, self).save(update_fields=[
                'district', 'congress_person', 'senator_1', 'senator_2'
            ])

    def __str__(self):
        return self.street
        + " "
        + self.city
        + " "
        + self.state
        + " "
        + self.zipcode


class LawMaker(models.Model):
    title = models.IntegerField(
        choices=Title,
        default=0
    )
    first_name = models.CharField(
        max_length=32
    )
    last_name = models.CharField(
        max_length=32
    )
    middle_name = models.CharField(
        max_length=32,
        null=True
    )
    suffix = models.CharField(
        max_length=8,
        null=True
    )
    # picture = models.ImageField(
    #     upload_to='law_maker_profiles/',
    #     default='no_img.png'
    # )
    gender = models.IntegerField(
        choices=Gender,
        default=0
    )
    party = models.IntegerField(
        choices=Party,
        default=0
    )
    position = models.IntegerField(
        choices=Position,
        default=0
    )
    senate_rank = models.CharField(
        max_length=6,
        null=True
    )
    state = models.CharField(
        max_length=2,
        choices=State,
        default=0
    )
    religion = models.CharField(
        max_length=32,
        null=True
    )
    district = models.IntegerField(
        null=True
    )
    address = models.CharField(
        max_length=64,
        null=True
    )
    office = models.CharField(
        max_length=64,
        null=True
    )
    rss_url = models.URLField(
        null=True
    )
    contact_form = models.URLField(
        null=True
    )
    url = models.URLField(
        null=True
    )
    phone_number = models.CharField(
        max_length=12,
        null=True
    )
    fax_number = models.CharField(
        max_length=12,
        null=True
    )
    birthday = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True
    )
    bioguide_id = models.CharField(
        max_length=16,
        primary_key=True
    )
    thomas_id = models.CharField(
        max_length=16,
        null=True
    )
    govtrack_id = models.CharField(
        max_length=16,
        null=True
    )
    opensecrets_id = models.CharField(
        max_length=16,
        null=True
    )
    votesmart_id = models.CharField(
        max_length=16,
        null=True
    )
    fec_id = models.CharField(
        max_length=16,
        null=True
    )
    cspan_id = models.CharField(
        max_length=16,
        null=True
    )
    maplight_id = models.CharField(
        max_length=16,
        null=True
    )
    house_history_id = models.CharField(
        max_length=16,
        null=True
    )
    icpsr_id = models.CharField(
        max_length=16,
        null=True
    )

    def __str__(self):
        return self.first_name + " " + self.last_name
