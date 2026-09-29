import asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.diagnostic import DiagnosticCentre, DiagnosticTest, centre_tests

async def seed_data():
    async with AsyncSessionLocal() as db:
        # create centres
        centre1 = DiagnosticCentre(
            name="Sultanpur Diagnostic Centre",
            location="Civil Lines",
            city="Sultanpur",
            address="Civil Lines, Sultanpur",
            contact_phone="9456123456",
            operating_hours="8:00 AM - 8:00 PM",
        )
        centre2 = DiagnosticCentre(
            name="Gomti Path Lab",
            location="Ayodhya Road",
            city="Sultanpur",
            address="Ayodhya Road, Sultanpur",
            contact_phone="9456234567",
            operating_hours="7:00 AM - 9:00 PM",
        )
        centre3 = DiagnosticCentre(
            name="UP Medical Centre",
            location="Lambaipur",
            city="Sultanpur",
            address="Lambaipur, Sultanpur",
            contact_phone="9456345678",
            operating_hours="9:00 AM - 6:00 PM",
        )
        db.add_all([centre1, centre2, centre3])
        await db.flush()

        #test list
        test1 = DiagnosticTest(
            name="Complete Blood Count",
            description="Measures red blood cells, white blood cells, and platelets",
            preparation_instructions="No special preparation required",
        )
        test2 = DiagnosticTest(
            name="Blood Sugar Test",
            description="Measures glucose levels in blood",
            preparation_instructions="Fasting for 8-12 hours recommended",
        )
        test3 = DiagnosticTest(
            name="Thyroid Function Test",
            description="Checks T3, T4, and TSH levels",
            preparation_instructions="No special preparation required",
        )
        test4 = DiagnosticTest(
            name="MRI Scan",
            description="Magnetic resonance imaging for detailed internal views",
            preparation_instructions="Remove all metal objects before scan",
        )
        db.add_all([test1, test2, test3, test4])
        await db.flush()

        #link center with prices
        await db.execute(
            centre_tests.insert().values([
                {"centre_id": centre1.id, "test_id": test1.id, "price": Decimal("500.00"), "duration_minutes": 30},
                {"centre_id": centre1.id, "test_id": test2.id, "price": Decimal("300.00"), "duration_minutes": 20},
                {"centre_id": centre1.id, "test_id": test3.id, "price": Decimal("800.00"), "duration_minutes": 45},
                {"centre_id": centre2.id, "test_id": test1.id, "price": Decimal("600.00"), "duration_minutes": 30},
                {"centre_id": centre2.id, "test_id": test2.id, "price": Decimal("350.00"), "duration_minutes": 20},
                {"centre_id": centre2.id, "test_id": test4.id, "price": Decimal("3500.00"), "duration_minutes": 60},
                {"centre_id": centre3.id, "test_id": test1.id, "price": Decimal("450.00"), "duration_minutes": 30},
                {"centre_id": centre3.id, "test_id": test3.id, "price": Decimal("750.00"), "duration_minutes": 45},
                {"centre_id": centre3.id, "test_id": test4.id, "price": Decimal("4000.00"), "duration_minutes": 60},
            ])
        )

        await db.commit()
        print("seedd done in db!")

if __name__ == "__main__":
    asyncio.run(seed_data())
