from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from faker import Faker
from api.models import POI, STATUS, SEVERITIES, Rating, VOTES, Comment
import random
from datetime import datetime

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

        #raise CommandError('Poll "%s" does not exist' % poll_id)
        self.stdout.write(self.style.SUCCESS('a tope'))


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
        poi_tags = random.choice(tags)
        created_date = datetime.now()

        poi = POI.objects.create(
            name=fake.word(),
            author=author,
            location=location,
            description=fake.paragraph(),
            status=status,
            severity=severity,
            created_date=created_date
        )
        poi.tags.add(poi_tags)
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
