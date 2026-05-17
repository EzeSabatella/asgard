from fastapi import APIRouter, HTTPException
from chassis.models.profile import PersonalProfile, EnterpriseProfile
from typing import Union

router = APIRouter()

@router.get("", response_model=Union[PersonalProfile, EnterpriseProfile])
async def get_profile():
    """
    Returns the initialized profile.
    Note: Auth will be added in Phase 1.
    """
    raise HTTPException(status_code=404, detail="Profile not found")
