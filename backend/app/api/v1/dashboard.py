from decimal import Decimal
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import authenticate_request as get_current_user
from app.services.cache import get_revenue_summary

router = APIRouter()


@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    tenant_id = current_user.get("tenant_id")

    if not tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Tenant information is missing from the authenticated user",
        )

    revenue_data = await get_revenue_summary(
        property_id=property_id,
        tenant_id=tenant_id,
    )

    total_revenue = Decimal(revenue_data["total"])

    return {
        "property_id": revenue_data["property_id"],
        "total_revenue": total_revenue,
        "currency": revenue_data["currency"],
        "reservations_count": revenue_data["count"],
    }