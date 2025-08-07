from tortoise import fields, models

class CardDetails(models.Model):
    account_number = fields.BigIntField(pk=True)
    debit_card_last_four_digits_1 = fields.CharField(max_length=4)
    valid_thru_1 = fields.DateField()
    debit_card_last_four_digits_2 = fields.CharField(max_length=4)
    valid_thru_2 = fields.DateField()

    class Meta:
        table = "card_details"
