from tortoise import fields, models
from models.iqama import IqamaRecord

class AbsherRecord(models.Model):
    iqama = fields.OneToOneField(
        "models.IqamaRecord",
        related_name="absher_data",
        on_delete=fields.CASCADE,
        pk=True  # ✅ Makes this the primary key
    )

    pep_flag = fields.CharField(max_length=3)         # 'Yes' or 'No'
    tax_employer_flag = fields.CharField(max_length=3)
    disability_flag = fields.CharField(max_length=3)
    high_risk_flag = fields.CharField(max_length=3)

    class Meta:
        table = "absher_records"
