# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid

from django.db import models


class ManeuAftersales(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    time = models.DateTimeField()
    order_id = models.CharField(max_length=36, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_aftersales'


class ManeuBatch(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    userid = models.CharField(db_column='userID', max_length=36)  # Field name made lowercase.
    guessid = models.CharField(db_column='guessID', max_length=36)  # Field name made lowercase.
    time = models.DateTimeField()
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    contents = models.TextField()

    class Meta:
        managed = False
        db_table = 'maneu_batch'


class ManeuClass(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    user_id = models.CharField(max_length=36)
    name = models.CharField(max_length=36)
    time = models.DateTimeField()
    series = models.CharField(max_length=36)
    color = models.CharField(max_length=36)
    class_field = models.CharField(db_column='class',
                                   max_length=36)  # Field renamed because it was a Python reserved word.
    count = models.CharField(max_length=36)
    price = models.CharField(max_length=36)
    remark = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'maneu_class'


class ManeuDatalogs(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    user_id = models.CharField(max_length=36, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    order_log = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_datalogs'


class ManeuGuess(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    time = models.DateTimeField()
    name = models.CharField(max_length=36, blank=True, null=True)
    phone = models.CharField(max_length=36, blank=True, null=True)
    sex = models.CharField(max_length=36, blank=True, null=True)
    age = models.CharField(max_length=36, blank=True, null=True)
    ot = models.CharField(db_column='OT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    em = models.CharField(db_column='EM', max_length=36, blank=True, null=True)  # Field name made lowercase.
    dfh = models.CharField(db_column='DFH', max_length=36, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField()
    user_id = models.CharField(max_length=36, blank=True, null=True)
    subjective_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_guess'


class ManeuOrder(models.Model):
    order_id = models.CharField(primary_key=True, max_length=32)
    order_token = models.CharField(max_length=32, blank=True, null=True)
    c_time = models.DateTimeField()
    c_name = models.CharField(max_length=11)
    c_phone = models.CharField(max_length=11)
    order = models.TextField(blank=True, null=True)
    besiness = models.CharField(max_length=16)
    status = models.IntegerField()
    remark = models.CharField(max_length=2048)

    class Meta:
        managed = False
        db_table = 'maneu_order'


class ManeuOrderV2(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    time = models.DateTimeField()
    name = models.CharField(max_length=36)
    phone = models.CharField(max_length=36)
    guess_id = models.CharField(max_length=36)
    users_id = models.CharField(max_length=36)
    store_id = models.CharField(max_length=36)
    visionsolutions_id = models.CharField(db_column='visionSolutions_id', max_length=36)  # Field name made lowercase.
    subjectiverefraction_id = models.CharField(db_column='subjectiveRefraction_id',
                                               max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'maneu_order_v2'


class ManeuStore(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    orderid = models.CharField(db_column='orderID', max_length=36)  # Field name made lowercase.
    time = models.DateTimeField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'maneu_store'


class ManeuSubjectiveRefraction(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    guessid = models.CharField(db_column='guessID', max_length=36)  # Field name made lowercase.
    time = models.DateTimeField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'maneu_subjective_refraction'


class ManeuUsers(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    nickname = models.CharField(max_length=36)
    username = models.CharField(unique=True, max_length=36)
    password = models.CharField(max_length=36)
    email = models.CharField(max_length=36)
    phone = models.CharField(max_length=36)
    level = models.IntegerField()
    state = models.IntegerField()
    create_time = models.DateTimeField()
    remark = models.CharField(max_length=255, blank=True, null=True)
    localtion = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_users'


class ManeuVisionSolutions(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid1, editable=False)
    orderid = models.CharField(db_column='orderID', max_length=36)  # Field name made lowercase.
    time = models.DateTimeField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'maneu_vision_solutions'
