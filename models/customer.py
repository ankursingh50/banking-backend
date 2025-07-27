from tortoise import fields, models
from datetime import datetime
from tortoise import timezone

class OnboardedCustomer(models.Model):
    iqama_id = fields.CharField(pk=True, max_length=10)
    full_name = fields.CharField(max_length=100, null=True)
    date_of_birth = fields.DateField(null=True)
    expiry_date = fields.DateField(null=True)
    issue_date = fields.DateField(null=True)  # ✅ add this
    age = fields.IntField(null=True)   
    gender = fields.CharField(max_length=10, null=True)
    nationality = fields.CharField(max_length=50, null=True)
    building_number = fields.CharField(max_length=10, null=True)
    street = fields.CharField(max_length=100, null=True)
    neighbourhood = fields.CharField(max_length=100, null=True)
    city = fields.CharField(max_length=50, null=True)
    postal_code = fields.CharField(max_length=10, null=True)
    country = fields.CharField(max_length=50, default="Saudi Arabia")
    mobile_number = fields.CharField(max_length=15, null=True)
    additional_mobile_number = fields.CharField(max_length=15, null=True)
    arabic_name = fields.CharField(max_length=100, null=True)
    date_of_birth_hijri = fields.CharField(max_length=20, null=True)
    expiry_date_hijri = fields.CharField(max_length=20, null=True)

    dep_reference_number = fields.CharField(max_length=10, unique=True)
    device_id = fields.CharField(max_length=100, null=True)
    device_type = fields.CharField(max_length=100, null=True)
    location = fields.CharField(max_length=255, null=True)

    status = fields.CharField(max_length=100, default="in_progress")
    created_at = fields.DatetimeField(default=timezone.now)
    updated_at = fields.DatetimeField(default=timezone.now)

    pep_flag = fields.CharField(max_length=3, null=True)
    disability_flag = fields.CharField(max_length=3, null=True)
    tax_residency_outside_ksa = fields.CharField(max_length=10, null=True)
    account_purpose = fields.CharField(max_length=500, null=True)
    estimated_withdrawal = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    mpin = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255, null=True)
    current_step = fields.CharField(max_length=100, null=True)

    #employment_status = fields.CharField(max_length=50, null=True)
    source_of_income = fields.TextField(null=True)  # comma-separated values
    employment_sector = fields.CharField(max_length=50, null=True)
    employer_industry = fields.CharField(max_length=100, null=True)
    business_industry = fields.CharField(max_length=100, null=True)

    salary_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    business_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    investment_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    rental_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    housewife_allowance = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    student_allowance = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    pension_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    hafiz_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)
    unemployed_income = fields.DecimalField(max_digits=13, decimal_places=2, null=True)

    class Meta:
        table = "onboarded_customers"
