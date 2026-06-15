"""
Admin routes for system management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from models import User as UserModel, Event as EventModel, Ticket as TicketModel
from schemas import User
from utils.auth import decode_token

router = APIRouter()

# Request models
class RoleUpdate(BaseModel):
    role: str

def get_admin_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> UserModel:
    """Verify admin access"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    username = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user

# User Management endpoints
@router.get("/users", response_model=List[User])
def list_all_users(db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Get all users (admin only)"""
    users = db.query(UserModel).all()
    return users

@router.post("/users/{user_id}/role")
def update_user_role(user_id: int, role_data: RoleUpdate, db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Update user role (admin only)"""
    
    if role_data.role not in ["admin", "organizer", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be: admin, organizer, or user"
        )
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.role = role_data.role
    db.commit()
    
    return {"message": f"User role updated to {role_data.role}", "user_id": user_id}

@router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Deactivate user account (admin only)"""
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deactivated", "user_id": user_id}

@router.post("/users/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Activate user account (admin only)"""
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    return {"message": "User activated", "user_id": user_id}

# Event Management endpoints
@router.get("/events")
def list_all_events(db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Get all events (admin only)"""
    events = db.query(EventModel).all()
    return events

@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Delete event (admin only)"""
    
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(event)
    db.commit()
    
    return {"message": "Event deleted", "event_id": event_id}

# Ticket Management endpoints
@router.get("/tickets")
def list_all_tickets(db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Get all tickets (admin only)"""
    tickets = db.query(TicketModel).all()
    return tickets

@router.get("/tickets/event/{event_id}")
def get_event_tickets(event_id: int, db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Get all tickets for an event (admin only)"""
    
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    tickets = db.query(TicketModel).filter(TicketModel.event_id == event_id).all()
    return tickets

# Statistics endpoints
@router.get("/stats")
def get_system_stats(db: Session = Depends(get_db), admin: UserModel = Depends(get_admin_user)):
    """Get system statistics (admin only)"""
    
    total_users = db.query(UserModel).count()
    total_events = db.query(EventModel).count()
    total_tickets = db.query(TicketModel).count()
    used_tickets = db.query(TicketModel).filter(TicketModel.is_used == True).count()
    
    users_by_role = {
        "admin": db.query(UserModel).filter(UserModel.role == "admin").count(),
        "organizer": db.query(UserModel).filter(UserModel.role == "organizer").count(),
        "user": db.query(UserModel).filter(UserModel.role == "user").count()
    }
    
    return {
        "total_users": total_users,
        "total_events": total_events,
        "total_tickets": total_tickets,
        "tickets_used": used_tickets,
        "tickets_available": total_tickets - used_tickets,
        "users_by_role": users_by_role
    }
