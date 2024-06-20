from django.core.management import call_command


def test_run_command(tmp_path):
    call_command("extract_fixture")
