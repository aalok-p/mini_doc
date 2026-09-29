from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.diagnostic import DiagnosticCentre, DiagnosticTest, centre_tests
from app.schemas.diagnostic import DiagnosticCentreResponse, DiagnosticTestResponse, CentreTestResponse

router = APIRouter(tags=["Diagnostics"])


@router.get("/centres", response_model=list[DiagnosticCentreResponse])
async def list_centres(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DiagnosticCentre).where(DiagnosticCentre.is_active == True))
    return result.scalars().all()


@router.get("/centres/{centre_id}", response_model=DiagnosticCentreResponse)
async def get_centre(centre_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DiagnosticCentre).where(DiagnosticCentre.id == centre_id)
    )
    centre = result.scalar_one_or_none()
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    return centre


@router.get("/centres/{centre_id}/tests", response_model=list[CentreTestResponse])
async def get_centre_tests(centre_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            DiagnosticTest.id,
            DiagnosticTest.name,
            DiagnosticTest.description,
            DiagnosticTest.preparation_instructions,
            centre_tests.c.price,
            centre_tests.c.duration_minutes,
        )
        .join(centre_tests, DiagnosticTest.id == centre_tests.c.test_id)
        .where(centre_tests.c.centre_id == centre_id)
    )
    rows = result.all()
    return [
        {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "preparation_instructions": row.preparation_instructions,
            "price": row.price,
            "duration_minutes": row.duration_minutes,
        }
        for row in rows
    ]


@router.get("/tests", response_model=list[DiagnosticTestResponse])
async def list_tests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DiagnosticTest).where(DiagnosticTest.is_active == True))
    return result.scalars().all()


@router.get("/tests/{test_id}", response_model=DiagnosticTestResponse)
async def get_test(test_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DiagnosticTest).where(DiagnosticTest.id == test_id)
    )
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test
