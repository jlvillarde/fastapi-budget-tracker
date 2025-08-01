from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated, List
from app.dependencies.auth import get_current_user
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications", 
    tags=["Notifications"],
    dependencies=[Depends(get_current_user)]
)

NotificationServiceDep = Annotated[NotificationService, Depends(NotificationService)]


@router.get("", response_model=List[dict])
def get_notifications(
    notification_service: NotificationServiceDep,
    request: Request
):
    """Get all notifications for the current user only."""
    user_id = int(request.session["user"]["id"])
    return notification_service.get_notifications(user_id)

@router.post("/mark-as-read/{index}")
def mark_notification_as_read(
    index: int,
    notification_service: NotificationServiceDep,
    request: Request
):
    """Mark a specific notification as read by index for the current user."""
    user_id = request.session["user"]["id"]
    notif = notification_service.mark_as_read(user_id, index)
    if notif is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif

@router.post("/mark-all-as-read")
def mark_all_notifications_as_read(
    notification_service: NotificationServiceDep,
    request: Request   
):
    """Mark all notifications as read for the current user."""
    user_id = request.session["user"]["id"]
    count = notification_service.mark_all_as_read(user_id)
    return {"updated": count}
