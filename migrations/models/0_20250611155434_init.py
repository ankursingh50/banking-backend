from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "onboarded_customers" (
    "iqama_id" VARCHAR(10) NOT NULL PRIMARY KEY,
    "full_name" VARCHAR(100),
    "date_of_birth" DATE,
    "expiry_date" DATE,
    "gender" VARCHAR(10),
    "nationality" VARCHAR(50),
    "building_number" VARCHAR(10),
    "street" VARCHAR(100),
    "neighbourhood" VARCHAR(100),
    "city" VARCHAR(50),
    "postal_code" VARCHAR(10),
    "country" VARCHAR(50) NOT NULL DEFAULT 'Saudi Arabia',
    "dep_reference_number" VARCHAR(10) NOT NULL UNIQUE,
    "device_id" VARCHAR(100),
    "device_type" VARCHAR(100),
    "location" VARCHAR(255),
    "status" VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "iqama_records" (
    "iqama_id" VARCHAR(10) NOT NULL PRIMARY KEY,
    "mobile_number" VARCHAR(10) NOT NULL,
    "full_name" VARCHAR(100) NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "gender" VARCHAR(10) NOT NULL,
    "nationality" VARCHAR(50) NOT NULL,
    "building_number" VARCHAR(10),
    "street" VARCHAR(100),
    "neighbourhood" VARCHAR(100),
    "city" VARCHAR(50),
    "postal_code" VARCHAR(10),
    "country" VARCHAR(50) NOT NULL DEFAULT 'Saudi Arabia',
    "expiry_date" DATE,
    CONSTRAINT "uid_iqama_recor_iqama_i_f8fc39" UNIQUE ("iqama_id", "mobile_number")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
