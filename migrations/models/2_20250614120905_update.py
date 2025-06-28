from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "onboarded_customers" ADD "mobile_number" VARCHAR(15);
        CREATE TABLE IF NOT EXISTS "themesettings" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "primary_font" VARCHAR(50) NOT NULL DEFAULT 'Urbanist',
    "secondary_font" VARCHAR(50) NOT NULL DEFAULT 'Urbanist-Regular',
    "primary_color" VARCHAR(20) NOT NULL DEFAULT '#f26b23',
    "secondary_color" VARCHAR(20) NOT NULL DEFAULT '#e0e0e0'
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "onboarded_customers" DROP COLUMN "mobile_number";
        DROP TABLE IF EXISTS "themesettings";"""
