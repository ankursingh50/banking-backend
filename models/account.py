from tortoise import fields, models

class AccountDetails(models.Model):
    account_number = fields.CharField(pk=True, max_length=20)
    iban_number = fields.CharField(max_length=34)
    account_balance = fields.IntField()
    account_type = fields.CharField(max_length=20)
    status = fields.CharField(max_length=20)
    spending_limit = fields.IntField()
    utilised_limit = fields.IntField()
    account_holder_name = fields.CharField(max_length=100)
    swift_code = fields.CharField(max_length=20)
    account_currency = fields.CharField(max_length=20)
    account_nickname = fields.CharField(max_length=50, null=True)
    account_creation_date = fields.DateField(null=True)

    class Meta:
        table = "account_details"
