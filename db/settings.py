import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": [
            "models.customer",
            "models.iqama",
            "models.portfolio",  # ✅ Portfolio summary
            "models.account", # ✅ Account details
            "models.card",  # ✅ Card Details
            "models.absher",
            "models.theme_settings",  # 👈 Add this
            "aerich.models"
           ],
            "default_connection": "default",
        }
    },
    # 👇 Add this
    "use_tz": False,
    "timezone": "UTC",  # This is still needed even if use_tz=False
}
