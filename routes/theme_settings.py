from fastapi import APIRouter, HTTPException
from models.theme_settings import ThemeSettings, ThemeSettings_Pydantic, ThemeSettingsIn_Pydantic

router = APIRouter()

@router.get("/theme-settings", response_model=ThemeSettings_Pydantic)
async def get_theme_settings():
    settings = await ThemeSettings.all().order_by("-updated_at").first()
    if not settings:
        raise HTTPException(status_code=404, detail="No theme settings found")
    return await ThemeSettings_Pydantic.from_tortoise_orm(settings)

@router.post("/theme-settings", response_model=ThemeSettings_Pydantic)
async def set_theme_settings(settings: ThemeSettingsIn_Pydantic):
    existing = await ThemeSettings.all().order_by("-updated_at").first()
    if existing:
        for field, value in settings.dict().items():
            setattr(existing, field, value)
        await existing.save()
        return await ThemeSettings_Pydantic.from_tortoise_orm(existing)
    else:
        obj = await ThemeSettings.create(**settings.dict())
        return await ThemeSettings_Pydantic.from_tortoise_orm(obj)
