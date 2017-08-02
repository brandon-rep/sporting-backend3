import json
from sporting_backend.models import LawMaker
import requests
from django.core.files.base import ContentFile


def run():
    print("---- Begin LawMaker Script ----")
    json_data = json.load(open("sporting_backend/scripts/legislators-current.json"))
    data = {}
    print("LawMaker Count:", LawMaker.objects.count())
    for person in json_data:
        # gender
        gender = person['bio']['gender']
        if gender == "M":
            data['gender'] = 1
        elif gender == "F":
            data['gender'] = 2
        else:
            data['gender'] = 0
            print('reached inside loop')
        # birthday
        data['birthday'] = person['bio']['birthday']

        # religion
        try:
            data['religion'] = person['bio']['religion']
        except:
            data['religion'] = None

        # name
        data['first_name'] = person['name']['first']
        data['last_name'] = person['name']['last']
        try:
            data['middle_name'] = person['name']['middle']
        except:
            data['middle_name'] = None
        try:
            data['suffix'] = person['name']['suffix']
        except:
            data['suffix'] = None

        # terms
        try:
            data['rss_url'] = person['terms'][-1]['rss_url']
        except:
            data['rss_url'] = None
        data['url'] = person['terms'][-1]['url']
        try:
            data['fax_number'] = person['terms'][-1]['fax']
        except:
            data['fax_number'] = None
        data['phone_number'] = person['terms'][-1]['phone']
        data['office'] = person['terms'][-1]['office']
        try:
            data['contact_form'] = person['terms'][-1]['contact_form']
        except:
            data['contact_form'] = None
        data['state'] = person['terms'][-1]['state']
        try:
            data['district'] = int(person['terms'][-1]['district'])
        except:
            data['district'] = None
        # try: clss = person['terms'][-1]['class']
        # except: clss = None
        # print clss
        try:
            data['senate_rank'] = person['terms'][-1]['state_rank']
        except:
            data['senate_rank'] = None
        party = person['terms'][-1]['party']
        if party == "republican":
            data['party'] = 3
        elif party == "democrat":
            data['party'] = 1
        else:
            data['party'] = 0
        position = person['terms'][-1]['type']
        if position == "rep":
            data['title'] = 2
        elif position == "sen":
            data['title'] = 1
        else:
            data['title'] = 0

        # ids
        try:
            data['thomas_id'] = person['id']['thomas']
        except:
            data['thomas_id'] = None

        try:
            data['maplight_id'] = person['id']['maplight']
        except:
            data['maplight_id'] = None


        try:
            data['icpsr_id'] = person['id']['icpsr']
        except:
            data['icpsr_id'] = None
        try:
            data['opensecrets_id'] = person['id']['opensecrets']
        except:
            data['opensecrets_id'] = None
        data['fec_id'] = person['id']['fec'][0]
        try:
            data['votesmart_id'] = person['id']['votesmart']
        except:
            data['votesmart_id'] = None
        data['govtrack_id'] = person['id']['govtrack']

        #Error Catching 
        try:
            data['cspan_id'] = person['id']['cspan']
        except:
            data['cspan_id'] = None
        try:
            data['house_history_id'] = person['id']['house_history']
        except:
            data['house_history_id'] = None
        try:
            data['bioguide_id'] = person['id']['bioguide']
        except:
            data['bioguide_id'] = None

        data['address'] = person['terms'][-1]['address']

        l = LawMaker(**data)

        # response = requests.get("https://theunitedstates.io/images/congress/225x275/" + person['id']['bioguide'] + ".jpg")
        # if response.status_code == 200:
        #     l.picture.save(person['id']['bioguide'] + '.jpg', ContentFile(response.content), save=True)
        l.save()
    print("---- End LawMaker Script ----")