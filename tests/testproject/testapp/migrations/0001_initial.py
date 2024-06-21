# Generated by Django 4.2 on 2024-06-20 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("release_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("instrument", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="RecordLabel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("release_date", models.DateField()),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="songs",
                        to="testapp.album",
                    ),
                ),
                (
                    "artists",
                    models.ManyToManyField(related_name="songs", to="testapp.artist"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="album",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="albums",
                to="testapp.artist",
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="record_label",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="albums",
                to="testapp.recordlabel",
            ),
        ),
    ]
