from pathlib import Path
import pytest
from django.core.management import call_command

from tests.utils import (
    date_repr,
    datetime_repr,
    get_json_from_file,
)
from tests.testproject.eventol.factories import EventFactory, EventTagFactory

pytestmark = [pytest.mark.django_db]


def test_run_command_only_simple_model(tmp_path):
    event_tag_1 = EventTagFactory.create()
    EventTagFactory.create()

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "app": "eventol",
        "model": "eventtag",
        "output_dir": output_dir,
    }
    call_command("extract_fixture", event_tag_1.id, **options)

    output_file = Path(output_dir).joinpath(
        f"eventtag_{event_tag_1.id}/eventol.eventtag.json"
    )
    expected_json = [
        {
            "model": "eventol.eventtag",
            "fields": {
                "id": 1,
                "name": event_tag_1.name,
                "created_at": datetime_repr(event_tag_1.created_at),
                "updated_at": datetime_repr(event_tag_1.updated_at),
                "background": event_tag_1.background,
                "logo_header": event_tag_1.logo_header,
                "logo_landing": event_tag_1.logo_landing,
                "message": event_tag_1.message,
                "slug": event_tag_1.slug,
            },
        }
    ]

    output_json = get_json_from_file(output_file)

    assert output_json == expected_json


def test_run_command_multiple_related_model(tmp_path):
    event_tag_1 = EventTagFactory.create()
    event_tag_2 = EventTagFactory.create()
    event_1 = EventFactory.create(tags=[event_tag_1, event_tag_2])

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "app": "eventol",
        "model": "eventtag",
        "output_dir": output_dir,
    }
    call_command("extract_fixture", event_tag_1.id, **options)

    output_file = Path(output_dir).joinpath(
        f"eventtag_{event_tag_1.id}/eventol.eventtag.json"
    )
    expected_json = [
        {
            "model": "eventol.eventtag",
            "fields": {
                "id": event_tag_1.id,
                "name": event_tag_1.name,
                "created_at": datetime_repr(event_tag_1.created_at),
                "updated_at": datetime_repr(event_tag_1.updated_at),
                "background": event_tag_1.background,
                "logo_header": event_tag_1.logo_header,
                "logo_landing": event_tag_1.logo_landing,
                "message": event_tag_1.message,
                "slug": event_tag_1.slug,
            },
        },
        {
            "model": "eventol.event",
            "fields": {
                "id": event_1.id,
                "created_at": datetime_repr(event_1.created_at),
                "updated_at": datetime_repr(event_1.updated_at),
                "name": event_1.name,
                "abstract": event_1.abstract,
                "limit_proposal_date": date_repr(event_1.limit_proposal_date),
                "registration_closed": event_1.registration_closed,
                "event_slug": event_1.event_slug,
                "cname": event_1.cname,
                "registration_code": str(event_1.registration_code),
                "external_url": event_1.external_url,
                "email": event_1.email,
                "schedule_confirmed": event_1.schedule_confirmed,
                "use_installations": event_1.use_installations,
                "use_installers": event_1.use_installers,
                "use_collaborators": event_1.use_collaborators,
                "use_proposals": event_1.use_proposals,
                "use_talks": event_1.use_talks,
                "is_flisol": event_1.is_flisol,
                "use_schedule": event_1.use_schedule,
                "place": event_1.place,
                "template": event_1.template,
                "css_custom": event_1.css_custom,
                "tags": [event_tag_1.id, event_tag_2.id],
            },
        },
        {
            "model": "eventol.eventtag",
            "fields": {
                "id": event_tag_2.id,
                "name": event_tag_2.name,
                "created_at": datetime_repr(event_tag_2.created_at),
                "updated_at": datetime_repr(event_tag_2.updated_at),
                "background": event_tag_2.background,
                "logo_header": event_tag_2.logo_header,
                "logo_landing": event_tag_2.logo_landing,
                "message": event_tag_2.message,
                "slug": event_tag_2.slug,
            },
        },
    ]

    expected_json = sorted(expected_json, key=lambda x: x["model"])

    output_json = sorted(get_json_from_file(output_file), key=lambda x: x["model"])

    assert output_json == expected_json


def test_run_command_multiple_related_model_from_otherside(tmp_path):
    event_tag_1 = EventTagFactory.create()
    event_tag_2 = EventTagFactory.create()
    event_1 = EventFactory.create(tags=[event_tag_1, event_tag_2])

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "app": "eventol",
        "model": "event",
        "output_dir": output_dir,
    }
    call_command("extract_fixture", event_1.id, **options)

    output_file = Path(output_dir).joinpath(
        f"event_{event_tag_1.id}/eventol.event.json"
    )
    expected_json = [
        {
            "model": "eventol.eventtag",
            "fields": {
                "id": event_tag_1.id,
                "name": event_tag_1.name,
                "created_at": datetime_repr(event_tag_1.created_at),
                "updated_at": datetime_repr(event_tag_1.updated_at),
                "background": event_tag_1.background,
                "logo_header": event_tag_1.logo_header,
                "logo_landing": event_tag_1.logo_landing,
                "message": event_tag_1.message,
                "slug": event_tag_1.slug,
            },
        },
        {
            "model": "eventol.event",
            "fields": {
                "id": event_1.id,
                "created_at": datetime_repr(event_1.created_at),
                "updated_at": datetime_repr(event_1.updated_at),
                "name": event_1.name,
                "abstract": event_1.abstract,
                "limit_proposal_date": date_repr(event_1.limit_proposal_date),
                "registration_closed": event_1.registration_closed,
                "event_slug": event_1.event_slug,
                "cname": event_1.cname,
                "registration_code": str(event_1.registration_code),
                "external_url": event_1.external_url,
                "email": event_1.email,
                "schedule_confirmed": event_1.schedule_confirmed,
                "use_installations": event_1.use_installations,
                "use_installers": event_1.use_installers,
                "use_collaborators": event_1.use_collaborators,
                "use_proposals": event_1.use_proposals,
                "use_talks": event_1.use_talks,
                "is_flisol": event_1.is_flisol,
                "use_schedule": event_1.use_schedule,
                "place": event_1.place,
                "template": event_1.template,
                "css_custom": event_1.css_custom,
                "tags": [event_tag_1.id, event_tag_2.id],
            },
        },
        {
            "model": "eventol.eventtag",
            "fields": {
                "id": event_tag_2.id,
                "name": event_tag_2.name,
                "created_at": datetime_repr(event_tag_2.created_at),
                "updated_at": datetime_repr(event_tag_2.updated_at),
                "background": event_tag_2.background,
                "logo_header": event_tag_2.logo_header,
                "logo_landing": event_tag_2.logo_landing,
                "message": event_tag_2.message,
                "slug": event_tag_2.slug,
            },
        },
    ]

    expected_json = sorted(expected_json, key=lambda x: x["model"])

    output_json = sorted(get_json_from_file(output_file), key=lambda x: x["model"])

    assert output_json == expected_json
