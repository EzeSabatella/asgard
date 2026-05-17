from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter()

@router.get("")
async def get_proposals() -> List[Dict[str, Any]]:
    """
    Returns pending proposals.
    Note: Auth will be added in Phase 1.
    """
    return []

@router.post("/{proposal_id}/approve")
async def approve_proposal(proposal_id: str):
    """
    Approves a given proposal.
    Note: Auth will be added in Phase 1.
    """
    raise HTTPException(status_code=404, detail="Proposal not found")
