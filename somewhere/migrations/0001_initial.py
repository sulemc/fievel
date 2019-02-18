# Generated by Django 2.1.7 on 2019-02-18 17:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flagged_Ad',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=100)),
                ('mp_1_name', models.CharField(max_length=100)),
                ('mp_1_url', models.CharField(max_length=500)),
                ('mp_2_name', models.CharField(max_length=100)),
                ('mp_2_url', models.CharField(max_length=500)),
                ('mp_3_name', models.CharField(max_length=100)),
                ('mp_3_url', models.CharField(max_length=500)),
                ('mp_4_name', models.CharField(max_length=100)),
                ('mp_4_url', models.CharField(max_length=500)),
                ('mp_5_name', models.CharField(max_length=100)),
                ('mp_5_url', models.CharField(max_length=500)),
            ],
        ),
    ]