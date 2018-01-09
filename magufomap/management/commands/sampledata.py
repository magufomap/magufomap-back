from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.gis.geos import Point
from faker import Faker

from datetime import datetime

import os
import random
import requests
import shutil

from api.models import (ChangeRequest,
                        Comment,
                        POIMImage, POIM,
                        Rating,
                        User)

from api.choices import (change_requests as change_requests_choices,
                         poims as poims_choices,
                         ratings as ratings_choices)


fake = Faker()
fake.seed(12345678901)


class Command(BaseCommand):
    help = 'Add sample data'

    def handle(self, *args, **options):
        tags = ["reiki", "homeopatía", "flores de bach", "frenología"]

        superusers = create_superusers()
        users = create_users()
        poims = create_poims(superusers + users, tags)

        create_photos(poims)
        create_ratings(superusers + users, poims)
        create_comments(superusers + users, poims)
        create_change_requests(superusers + users, poims)

        self.stdout.write(self.style.SUCCESS('Sample data created'))


def create_photos(poims):
    if not os.path.exists('media/uploads'):
        os.makedirs('media/uploads')

    PATHS = ['media/uploads/uno.png', 'media/uploads/dos.png',
             'media/uploads/tres.png', 'media/uploads/cuatro.png',
             'media/uploads/cinco.png', 'media/uploads/seis.png',
             'media/uploads/siete.png', 'media/uploads/ocho.png',
             'media/uploads/nueve.png', 'media/uploads/diez.png']

    IMAGES = ['uploads/uno.png', 'uploads/dos.png',
              'uploads/tres.png', 'uploads/cuatro.png',
              'uploads/cinco.png', 'uploads/seis.png',
              'uploads/siete.png', 'uploads/ocho.png',
              'uploads/nueve.png', 'uploads/diez.png']

    for i in range(0, 10):
        r = requests.get('https://loremflickr.com/320/240', stream=True)
        if r.status_code == 200:
            with open(PATHS[i], 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    for poim in poims:
        for i in range(0, random.randint(0, 6)):
            poim_image = POIMImage()
            poim_image.photo = random.choice(IMAGES)
            poim_image.poim = poim
            poim_image.save()


def create_superusers():
    superusers = []
    yami = User.objects.create_superuser(
        username="yami",
        email="a@b.com",
        password="yami1234",
        full_name="Yami"
    )
    superusers.append(yami)
    david = User.objects.create_superuser(
        username="david",
        email="a@c.com",
        password="david1234",
        full_name="David"
    )
    superusers.append(david)
    return superusers


def create_users():
    users = []
    for i in range(0, 10):
        name = fake.user_name()
        user = User.objects.create_user(
            name,
            fake.email(),
            "{}1234".format(name),
            full_name=fake.name(),
            is_staff=True,
        )
        users.append(user)

        try:
            group = Group.objects.get(name='Editors')
            group.user_set.add(user)
        except Group.DoesNotExist:
            pass
    return users


def create_poims(users, tags):
    poims = []
    for i in range(0, 30):
        lon = random.choice(range(-41542, -30309)) / 10000
        lat = random.choice(range(401348, 408554)) / 10000
        location = Point(lon, lat)
        owner = random.choice(users)
        status = random.choice(poims_choices.STATUSES[:2])[0]
        severity = random.choice(poims_choices.SEVERITIES)[0]
        created_date = datetime.now()
        description = ' '.join(fake.paragraphs(nb=4, ext_word_list=None))

        poim = POIM.objects.create(
            name=fake.company(),
            owner=owner,
            location=location,
            description=description,
            status=status,
            severity=severity,
            created_date=created_date
        )
        for i in range(1, random.randint(2, 4)):
            poim.tags.add(random.choice(tags))
        poim.save()
        poims.append(poim)

    return poims


def create_ratings(users, poims):
    for poim in poims:
        users_for_poim = users[:]
        for i in range(1, random.randint(0, 8)):
            random.shuffle(users_for_poim)
            user = users_for_poim.pop()
            Rating.objects.create(
                owner=user,
                poim=poim,
                vote=random.choice(ratings_choices.VOTES)[0]
            )


def create_comments(users, poims):
    for poim in poims:
        for i in range(0, random.randint(0, 16)):
            Comment.objects.create(
                owner=random.choice(users),
                poim=poim,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now()
            )


def create_change_requests(users, poims):
    for poim in poims:
        for i in range(0, random.randint(0, 8)):
            ChangeRequest.objects.create(
                owner=random.choice(users),
                poim=poim,
                change=fake.text(max_nb_chars=200, ext_word_list=None),
                status=random.choice(change_requests_choices.STATUSES)[0],
                created_date=datetime.now()
            )
