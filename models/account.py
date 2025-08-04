from tortoise import fields, models

class AccountDetails(models.Model):
    iqama_id = fields.CharField(pk=True, max_length=15)

    account_number_1 = fields.CharField(max_length=20, null=True)
    iban_number_1 = fields.CharField(max_length=34, null=True)
    account_balance_1 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)
    account_type_1 = fields.CharField(max_length=50, null=True)
    status_1 = fields.CharField(max_length=50, null=True)
    spending_limit_1 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)
    utlised_limit_1 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)
    debit_card_last_four_digits_1 = fields.CharField(max_length=4, null=True)
    valid_thru_1 = fields.CharField(max_length=10, null=True)
    debit_card_last_four_digits_2 = fields.CharField(max_length=4, null=True)
    valid_thru_2 = fields.CharField(max_length=10, null=True)

    recent_transaction_type_1 = fields.CharField(max_length=50, null=True)
    recent_transaction_date_1 = fields.CharField(max_length=20, null=True)
    recent_transactions_amount_1 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    recent_transaction_type_2 = fields.CharField(max_length=50, null=True)
    recent_transactions_date_2 = fields.CharField(max_length=20, null=True)
    recent_transactions_amount_2 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    recent_transactions_transaction_type_3 = fields.CharField(max_length=50, null=True)
    recent_transactions_date_3 = fields.CharField(max_length=20, null=True)
    recent_transactions_amount_3 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    bill_transaction_type_1 = fields.CharField(max_length=50, null=True)
    bill_due_date_1 = fields.CharField(max_length=20, null=True)
    bill_service_type_1 = fields.CharField(max_length=100, null=True)
    bill_amount_1 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    bill_transaction_type_2 = fields.CharField(max_length=50, null=True)
    bill_due_date_2 = fields.CharField(max_length=20, null=True)
    bill_service_type_2 = fields.CharField(max_length=100, null=True)
    bill_amount_2 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    recent_transfers_date_1 = fields.CharField(max_length=20, null=True)
    recent_transfers_beneficiary_name_1 = fields.CharField(max_length=100, null=True)
    recent_transfers_bank_name_1 = fields.CharField(max_length=100, null=True)
    recent_transfers_amount_1 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    recent_transfers_date_2 = fields.CharField(max_length=20, null=True)
    recent_transfers_beneficiary_name_2 = fields.CharField(max_length=100, null=True)
    recent_transfers_bank_name_2 = fields.CharField(max_length=100, null=True)
    recent_transfers_amount_2 = fields.DecimalField(max_digits=15, decimal_places=2, null=True)

    # (Add fields for account 2 and additional transactions and bills similar to above…)

    class Meta:
        table = "account_details"
