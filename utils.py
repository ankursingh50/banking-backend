from models.customer import OnboardedCustomer

async def generate_dep_reference_number():
    prefix = "DEP"
    i = 1
    while True:
        ref = f"{prefix}{i:07d}"
        exists = await OnboardedCustomer.filter(dep_reference_number=ref).exists()
        if not exists:
            return ref
        i += 1

