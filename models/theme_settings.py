from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class ThemeSettings(models.Model):
    id = fields.IntField(pk=True)
    primary_color = fields.CharField(max_length=10)
    secondary_color = fields.CharField(max_length=10)
    background_color = fields.CharField(max_length=10)
    primary_font = fields.CharField(max_length=50)
    secondary_font = fields.CharField(max_length=50)
    primary_font_size = fields.CharField(max_length=10)
    secondary_font_size = fields.CharField(max_length=10)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "themesettings"  # 👈 Explicitly bind to the correct table name

ThemeSettings_Pydantic = pydantic_model_creator(ThemeSettings, name="ThemeSettings")
ThemeSettingsIn_Pydantic = pydantic_model_creator(ThemeSettings, name="ThemeSettingsIn", exclude_readonly=True)
