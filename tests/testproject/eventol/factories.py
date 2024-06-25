from datetime import date
from pathlib import Path

import factory.fuzzy
from factory import post_generation
from factory.django import DjangoModelFactory

from tests.testproject.eventol.models import EventTag, Event


def _generate_image(image_name: str = "image.jpg"):
    image_dir = "./tests/tmp_images/"

    image_path = Path(f"{image_dir}{image_name}")

    return factory.django.ImageField(filename=str(image_path))


def _generate_file(file_name: str = "file.html"):
    file_dir = "./tests/tmp_files/"

    file_path = Path(f"{file_dir}{file_name}")

    return factory.django.FileField(filename=str(file_path))



class EventTagFactory(DjangoModelFactory):
    class Meta:
        model = EventTag

    name = factory.fuzzy.FuzzyText(length=50)
    created_at = factory.fuzzy.FuzzyDate(start_date=date(2021, 1, 1))
    updated_at = factory.fuzzy.FuzzyDate(start_date=date(2021, 1, 1))
    background = _generate_image(image_name="background.jpg")
    logo_header = _generate_image(image_name="logo_header.jpg")
    logo_landing = _generate_image(image_name="logo_landing.jpg")
    message = factory.fuzzy.FuzzyText(length=50)
    slug = factory.fuzzy.FuzzyText(length=50)


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    created_at = factory.fuzzy.FuzzyDate(start_date=date(2021, 1, 1))
    updated_at = factory.fuzzy.FuzzyDate(start_date=date(2021, 1, 1))
    name = factory.fuzzy.FuzzyText(length=50)
    abstract = factory.fuzzy.FuzzyText(length=250)
    limit_proposal_date = factory.fuzzy.FuzzyDate(start_date=date(2021, 1, 1))
    registration_closed = factory.Faker("boolean")
    event_slug = factory.fuzzy.FuzzyText(length=100)
    cname = factory.fuzzy.FuzzyText(length=50)
    registration_code = factory.Faker("uuid4")
    external_url = factory.Faker("url")
    email = factory.Faker("email")
    schedule_confirmed = factory.Faker("boolean")
    use_installations = factory.Faker("boolean")
    use_installers = factory.Faker("boolean")
    use_collaborators = factory.Faker("boolean")
    use_proposals = factory.Faker("boolean")
    use_talks = factory.Faker("boolean")
    is_flisol = factory.Faker("boolean")
    use_schedule = factory.Faker("boolean")
    place = factory.fuzzy.FuzzyText(length=50)
    template = _generate_file(file_name="template.html")
    css_custom = _generate_file(file_name="css_custom.css")

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(EventTagFactory())
