# core/models.py
from django.db import models

class MasterDistrict(models.Model):
    district_id = models.BigIntegerField(primary_key=True)
    district_code = models.CharField(max_length=50, null=True, blank=True)
    state_id = models.IntegerField()
    mandal_id = models.BigIntegerField(null=True, blank=True)
    district_name_en = models.CharField(max_length=255)
    district_short_name_en = models.CharField(max_length=50, null=True, blank=True)
    district_name_local = models.CharField(max_length=255, null=True, blank=True)
    lgd_code = models.CharField(max_length=50, null=True, blank=True)
    language_id = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "master_district"
        managed = False

class MasterBlock(models.Model):
    block_id = models.BigIntegerField(primary_key=True)
    state_id = models.IntegerField()
    district_id = models.BigIntegerField()
    block_code = models.CharField(max_length=50, null=True, blank=True)
    block_name_en = models.CharField(max_length=255, null=True, blank=True)
    block_name_local = models.CharField(max_length=255, null=True, blank=True)
    rural_urban_area = models.CharField(max_length=1, null=True, blank=True)
    lgd_code = models.CharField(max_length=50, null=True, blank=True)
    language_id = models.CharField(max_length=20, null=True, blank=True)
    is_aspirational = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "master_block"
        managed = False

class MasterPanchayat(models.Model):
    panchayat_id = models.BigIntegerField(primary_key=True)
    state_id = models.IntegerField()
    district_id = models.BigIntegerField()
    block_id = models.BigIntegerField()
    panchayat_code = models.CharField(max_length=100, null=True, blank=True)
    panchayat_name_en = models.CharField(max_length=255, null=True, blank=True)
    panchayat_name_local = models.CharField(max_length=255, null=True, blank=True)
    rural_urban_area = models.CharField(max_length=1, null=True, blank=True)
    language_id = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "master_panchayat"
        managed = False

class MasterVillage(models.Model):
    village_id = models.BigIntegerField(primary_key=True)
    state_id = models.IntegerField()
    district_id = models.BigIntegerField()
    block_id = models.BigIntegerField()
    panchayat_id = models.BigIntegerField()
    village_code = models.CharField(max_length=100, null=True, blank=True)
    village_name_english = models.CharField(max_length=255, null=True, blank=True)
    village_name_local = models.CharField(max_length=255, null=True, blank=True)
    rural_urban_area = models.CharField(max_length=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "master_village"
        managed = False

class MasterUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    recovery_email = models.CharField(max_length=255, null=True, blank=True)
    recovery_mobile = models.CharField(max_length=20, null=True, blank=True)
    pass_attempt_no = models.IntegerField(default=0)
    role = models.CharField(
        max_length=50,
        choices=[
            ("bmmu", "BMMU"),
            ("dmmu", "DMMU"),
            ("smmu", "SMMU"),
            ("training_partner", "Training Partner"),
            ("crp_ld", "CRP-LD"),
            ("crp_ep", "CRP-EP"),
            ("master_trainer", "Master Trainer"),
            ("admin", "Admin"),
        ],
        default="bmmu",
    )
    user_type = models.CharField(
        max_length=10,
        choices=[("csu", "CSU"), ("dtu", "DTU"), ("btu", "BTU")],
        default="dtu",
    )
    is_active = models.BooleanField(default=True)
    last_active_on = models.DateTimeField(null=True, blank=True)
    is_suspended = models.BooleanField(default=False)
    suspended_on = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    locked_on = models.DateTimeField(null=True, blank=True)
    pass_updated_at = models.DateTimeField(null=True, blank=True)
    pass_updated_by = models.BigIntegerField(null=True, blank=True)
    TH_urid = models.CharField(max_length=36, unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    deleted_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "master_user"
        managed = False

class MasterShgList(models.Model):
    id = models.BigAutoField(primary_key=True)
    shg_code = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    nic_code = models.CharField(max_length=100, null=True, blank=True)
    block_id = models.BigIntegerField(null=True, blank=True)
    district_id = models.BigIntegerField(null=True, blank=True)
    panchayat_id = models.BigIntegerField(null=True, blank=True)
    village_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.IntegerField(null=True, blank=True)
    formation_date = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(null=True, blank=True)
    pfms_verified = models.BooleanField(null=True, blank=True)
    meeting_frequency = models.CharField(max_length=50, null=True, blank=True)
    registration_act_name = models.CharField(max_length=255, null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    guid = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "master_shg_list"
        managed = False

class MasterClfList(models.Model):
    id = models.BigAutoField(primary_key=True)
    clf_code = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    nic_code = models.CharField(max_length=100, null=True, blank=True)
    block_id = models.BigIntegerField(null=True, blank=True)
    district_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.IntegerField(null=True, blank=True)
    formation_date = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(null=True, blank=True)
    pfms_verified = models.BooleanField(null=True, blank=True)
    meeting_frequency = models.CharField(max_length=50, null=True, blank=True)
    registration_act_name = models.CharField(max_length=255, null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    guid = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "master_clf_list"
        managed = False

class MasterBeneficiary(models.Model):
    member_code = models.CharField(max_length=100, primary_key=True)
    member_id = models.BigIntegerField(null=True, blank=True, unique=True)
    shg_code = models.CharField(max_length=100)
    member_guid = models.CharField(max_length=100, null=True, blank=True)
    member_name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    father_husband = models.CharField(max_length=255, null=True, blank=True)
    relation_name = models.CharField(max_length=255, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    social_category = models.CharField(max_length=50, null=True, blank=True)
    nic_member_code = models.CharField(max_length=100, null=True, blank=True)
    aadhar_verified = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    state_id = models.IntegerField(null=True, blank=True)
    district_id = models.BigIntegerField(null=True, blank=True)
    block_id = models.BigIntegerField(null=True, blank=True)
    panchayat_id = models.BigIntegerField(null=True, blank=True)
    village_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "master_beneficiary"
        managed = False
