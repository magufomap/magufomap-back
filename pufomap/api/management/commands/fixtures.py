from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from faker import Faker
from api.models import POI, STATUS, SEVERITIES, Rating, VOTES, Comment, POIImage
from datetime import datetime
import os
import random
import requests
import shutil

fake = Faker()
fake.seed(12345678901)


class Command(BaseCommand):
    help = 'Add fixtures'

    def handle(self, *args, **options):
        tags = ["reiki", "homeopatía", "flores de bach", "frenología"]
        superusers = create_superusers()
        users = create_users()
        pois = create_pois(superusers + users, tags)
        ratings = create_ratings(superusers + users, pois)
        comments = create_comments(superusers + users, pois)
        photos = create_photos(pois)

        #raise CommandError('Poll "%s" does not exist' % poll_id)
        self.stdout.write(self.style.SUCCESS('a tope'))


def create_photos(pois):
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

    for i in range(0,10):
        r = requests.get('https://loremflickr.com/320/240', stream=True)
        if r.status_code == 200:
            with open(PATHS[i], 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    for poi in pois:
        for i in range(0, random.randint(0, 6)):
            poi_image = POIImage()
            poi_image.photo = random.choice(IMAGES)
            poi_image.poi = poi
            poi_image.save()


def create_superusers():
    superusers = []
    yami = User.objects.create_superuser(
            username="yami",
            email="a@b.com",
            password="yami1234"
    )
    superusers.append(yami)
    david = User.objects.create_superuser(
            username="david",
            email="a@c.com",
            password="david1234"
    )
    superusers.append(david)
    return superusers



def create_users():
    users = []
    for i in range(0,10):
        name = fake.user_name()
        user = User.objects.create_user(
                name,
                fake.email(),
                "{}1234".format(name)
        )
        users.append(user)
    return users


def create_pois(users, tags):
    pois = []
    for i in range(0,30):
        lon = random.choice(range(-41542, -30309)) / 10000
        lat = random.choice(range(401348, 408554)) / 10000
        location = Point(lon, lat)
        author = random.choice(users)
        status = random.choice(STATUS[:2])[0]
        severity = random.choice(SEVERITIES)[0]
        created_date = datetime.now()
        description = ' '.join(fake.paragraphs(nb=4, ext_word_list=None))

        poi = POI.objects.create(
            name=fake.company(),
            author=author,
            location=location,
            description=description,
            status=status,
            severity=severity,
            created_date=created_date
        )
        for i in range(1,random.randint(2,4)):
            poi.tags.add(random.choice(tags))
        poi.save()
        pois.append(poi)

    return pois


def create_ratings(users, pois):
    for poi in pois:
        users_for_poi = users[:]

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])

        random.shuffle(users_for_poi)
        user = users_for_poi.pop()
        rating = Rating.objects.create(
                user=user,
                poi=poi,
                vote=random.choice(VOTES)[0])


def create_comments(users, pois):
    for poi in pois:
        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())

        user = random.choice(users)
        comment = Comment.objects.create(
                user=user,
                poi=poi,
                comment=fake.text(max_nb_chars=200, ext_word_list=None),
                created_date=datetime.now())
