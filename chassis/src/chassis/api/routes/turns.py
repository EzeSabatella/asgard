from fastapi import APIRouter, status
from chassis.models.context import ConversationTurn

router = APIRouter()

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def post_turn(turn: ConversationTurn):
    """
    Encola un ConversationTurn para procesamiento asíncrono.
    Note: Auth will be added in Phase 1.
    """
    return {
        "turn_id": turn.turn_id,
        "status": "queued"
    }
