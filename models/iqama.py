from tortoise import fields, models

class IqamaRecord(models.Model):
    iqama_id = fields.CharField(max_length=10, pk=True)
    mobile_number = fields.CharField(max_length=10)
    full_name = fields.CharField(max_length=100)
    date_of_birth = fields.DateField()
    gender = fields.CharField(max_length=10)
    nationality = fields.CharField(max_length=50)
    building_number = fields.CharField(max_length=10, null=True)
    street = fields.CharField(max_length=100, null=True)
    neighbourhood = fields.CharField(max_length=100, null=True)
    city = fields.CharField(max_length=50, null=True)
    postal_code = fields.CharField(max_length=10, null=True)
    country = fields.CharField(max_length=50, default="Saudi Arabia")
    issue_date = fields.DateField(null=True)
    expiry_date = fields.DateField(null=True)
    age = fields.IntField(null=True)
    additional_mobile_number = fields.CharField(max_length=10, null=True)
    arabic_name = fields.TextField(null=True)
    dob_hijri = fields.DateField(null=True)
    expiry_date_hijri = fields.DateField(null=True)

    class Meta:
        table = "iqama_records"
        unique_together = ("iqama_id", "mobile_number")
