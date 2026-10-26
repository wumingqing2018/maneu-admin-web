# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from uuid import uuid4

from django.db import models


class ManeuAdmin(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4, editable=False)  # The composite primary key (id, username) found, that is not supported. The first column is selected.
    username = models.CharField(max_length=36)
    password = models.CharField(max_length=36)
    nickname = models.CharField(max_length=36)
    email = models.CharField(max_length=36)
    phone = models.CharField(max_length=36)
    level = models.CharField(max_length=36)
    state = models.CharField(max_length=36)
    time = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=512, blank=True, null=True)
    location = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_admin'
        unique_together = (('id', 'username'),)


class ManeuGuest(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4, editable=False)
    admin_id = models.CharField(max_length=36, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=36, blank=True, null=True)
    phone = models.CharField(max_length=36, blank=True, null=True)
    status = models.CharField(max_length=36, blank=True, null=True)
    sex = models.CharField(max_length=36, blank=True, null=True)
    age = models.CharField(max_length=36, blank=True, null=True)
    dfh = models.CharField(max_length=36, blank=True, null=True)
    ot = models.CharField(max_length=36, blank=True, null=True)
    em = models.CharField(max_length=36, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_guest'


class ManeuOrder(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4, editable=False)
    admin_id = models.CharField(max_length=36)
    guest_id = models.CharField(max_length=36)
    store_id = models.CharField(max_length=36)
    report_id = models.CharField(max_length=36)
    time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=36, blank=True, null=True)
    phone = models.CharField(max_length=36, blank=True, null=True)
    status = models.CharField(max_length=36, blank=True, null=True)
    remark = models.CharField(max_length=512)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_order'


class ManeuReport(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4, editable=False)
    admin_id = models.CharField(max_length=36, blank=True, null=True)
    guest_id = models.CharField(max_length=36, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=36, blank=True, null=True)
    phone = models.CharField(max_length=36, blank=True, null=True)
    status = models.CharField(max_length=36, blank=True, null=True)
    plan = models.CharField(db_column='PLAN', max_length=36, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(max_length=36, blank=True, null=True)
    age = models.CharField(max_length=36, blank=True, null=True)
    dfh = models.CharField(max_length=36, blank=True, null=True)
    ot = models.CharField(max_length=36, blank=True, null=True)
    em = models.CharField(max_length=36, blank=True, null=True)
    pd = models.CharField(db_column='PD', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_al = models.CharField(db_column='OD_AL', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_ak = models.CharField(db_column='OD_AK', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_ax = models.CharField(db_column='OD_AX', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_ad = models.CharField(db_column='OD_AD', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_add = models.CharField(db_column='OD_ADD', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_bc = models.CharField(db_column='OD_BC', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_cyl = models.CharField(db_column='OD_CYL', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_cct = models.CharField(db_column='OD_CCT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_va = models.CharField(db_column='OD_VA', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_sph = models.CharField(db_column='OD_SPH', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_pr = models.CharField(db_column='OD_PR', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_fr = models.CharField(db_column='OD_FR', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_lt = models.CharField(db_column='OD_LT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    od_vt = models.CharField(db_column='OD_VT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_al = models.CharField(db_column='OS_AL', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_ak = models.CharField(db_column='OS_AK', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_ax = models.CharField(db_column='OS_AX', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_ad = models.CharField(db_column='OS_AD', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_add = models.CharField(db_column='OS_ADD', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_bc = models.CharField(db_column='OS_BC', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_cyl = models.CharField(db_column='OS_CYL', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_cct = models.CharField(db_column='OS_CCT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_va = models.CharField(db_column='OS_VA', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_sph = models.CharField(db_column='OS_SPH', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_pr = models.CharField(db_column='OS_PR', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_fr = models.CharField(db_column='OS_FR', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_lt = models.CharField(db_column='OS_LT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    os_vt = models.CharField(db_column='OS_VT', max_length=36, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_report'


class ManeuService(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4, editable=False)
    time = models.DateTimeField()
    order_id = models.CharField(max_length=36, blank=True, null=True)
    admin_id = models.CharField(max_length=36)
    guess_id = models.CharField(max_length=36)
    content = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maneu_service'


class ManeuStore(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid4, editable=False)
    order_id = models.CharField(max_length=36)
    admin_id = models.CharField(max_length=36)
    guess_id = models.CharField(max_length=36)
    time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=36, blank=True, null=True)
    phone = models.CharField(max_length=36, blank=True, null=True)
    status = models.CharField(max_length=36, blank=True, null=True)
    content = models.TextField()
    remark = models.TextField()

    class Meta:
        managed = False
        db_table = 'maneu_store'




class ManeuGuest(models.Model):
    """小程序客户（C 端用户）"""

    id = models.CharField(primary_key=True, max_length=64, editable=False, verbose_name="主键")

    # ---- 微信小程序登录核心字段 ----
    openid = models.CharField(max_length=64, unique=True, verbose_name="微信 openid")
    unionid = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=None,
        unique=True,
        verbose_name="微信 unionid",
    )

    # ---- 用户资料 ----
    nickname = models.CharField(max_length=64, blank=True, default="", verbose_name="微信昵称")
    avatar_url = models.CharField(max_length=1024, blank=True, default="", verbose_name="头像")
    name = models.CharField(max_length=36, blank=True, default="", verbose_name="真实姓名")
    phone = models.CharField(
        max_length=20, blank=True, default="", db_index=True, verbose_name="手机号"
    )
    birthday = models.DateField(blank=True, null=True, verbose_name="生日")
    remark = models.TextField(blank=True, default="", verbose_name="备注")

    # ---- 时间 ----
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="最后登录")

    class Meta:
        db_table = "maneu_guest"
        verbose_name = "小程序客户"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.nickname or self.name or self.phone or str(self.id)