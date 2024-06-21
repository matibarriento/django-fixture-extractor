from django.core.management import call_command
import pytest

pytestmark = [pytest.mark.django_db]


def test_run_command(tmp_path):
    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "app": "testapp",
        "model": "artist",
        "output_dir": output_dir,
    }
    call_command("extract_fixture", "1", **options)
