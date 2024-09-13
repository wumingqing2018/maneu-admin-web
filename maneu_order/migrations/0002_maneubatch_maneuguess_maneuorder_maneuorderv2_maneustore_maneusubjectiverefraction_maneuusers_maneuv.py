# Generated by Django 3.0 on 2022-08-15 12:17

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('maneu_order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManeuBatch',
            fields=[
                ('order_id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                              serialize=False)),
                ('c_time', models.DateTimeField()),
                ('c_name', models.CharField(max_length=255)),
                ('c_phone', models.CharField(max_length=255)),
                ('maneu_order', models.TextField()),
                ('remark', models.TextField()),
            ],
            options={
                'db_table': 'maneu_batch',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuGuess',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                        serialize=False)),
                ('time', models.DateTimeField()),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=32)),
                ('sex', models.CharField(max_length=32)),
                ('age', models.DateField()),
                ('ot', models.CharField(db_column='OT', max_length=32)),
                ('em', models.CharField(db_column='EM', max_length=32)),
                ('dfh', models.CharField(db_column='DFH', max_length=32)),
                ('remark', models.TextField()),
            ],
            options={
                'db_table': 'maneu_client',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuOrder',
            fields=[
                ('order_id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                              serialize=False)),
                ('order_token', models.CharField(blank=True, max_length=32, null=True)),
                ('c_time', models.DateTimeField()),
                ('c_name', models.CharField(max_length=11)),
                ('c_phone', models.CharField(max_length=11)),
                ('maneu_order', models.TextField(blank=True, null=True)),
                ('besiness', models.CharField(max_length=16)),
                ('status', models.IntegerField()),
                ('remark', models.CharField(max_length=2048)),
            ],
            options={
                'db_table': 'maneu_order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuOrderV2',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                        serialize=False)),
                ('guess_id', models.CharField(db_column='guess_id', max_length=36)),
                ('users_id', models.CharField(db_column='users_id', max_length=36)),
                ('store_id', models.CharField(db_column='store_id', max_length=36)),
                ('visionsolutions_id', models.CharField(db_column='visionSolutions_id', max_length=36)),
                ('subjectiverefraction_id', models.TextField(db_column='subjectiveRefraction_id', max_length=36)),
            ],
            options={
                'db_table': 'maneu_order_v2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuStore',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                        serialize=False)),
                ('time', models.DateTimeField()),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'maneu_store',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuSubjectiveRefraction',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                        serialize=False)),
                ('time', models.DateTimeField()),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'maneu_subjective_refraction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuUsers',
            fields=[
                ('user_id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                             serialize=False)),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=128)),
                ('level', models.IntegerField()),
                ('state', models.IntegerField()),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'maneu_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManeuVisionSolutions',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=36, primary_key=True,
                                        serialize=False)),
                ('time', models.DateTimeField()),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'maneu_vision_solutions',
                'managed': False,
            },
        ),
    ]
