from faker import Faker
from django.contrib.auth import get_user_model
import random
from lostandfoundbackend.listings.models import Pet




def run():
    fake = Faker()
    User = get_user_model()

    users = list(User.objects.all())
    if not users:
        default_user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'
        )
        users = [default_user]

    PET_TYPES = ["dog", "cat", "bird", "rabbit", "fish", "other"]
    PET_STATUS = ["adopting", "selling", "breeding"]

    for _ in range(40):
        pet_type = random.choice(PET_TYPES)
        breed = fake.word()
        Pet.objects.create(
            name=fake.first_name(),
            type=pet_type,
            breed=breed,
            age=random.randint(1, 120),
            gender=random.choice(["male", "female"]),
            description=fake.paragraph(nb_sentences=3),
            status=random.choice(PET_STATUS),
            price=round(random.uniform(50, 2000), 2),
            vaccinated=random.choice([True, False]),
            city=fake.city(),
            owner=random.choice(users)
        )

    print("Successfully created 10 fake pets")

run()