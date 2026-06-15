"""
Events routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Event as EventModel, User as UserModel
from schemas import EventCreate, Event, EventWithTickets
from routes.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Event)
def create_event(event_data: EventCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Create a new event"""
    organizer_id = current_user.id
    # Check if organizer exists
    organizer = db.query(UserModel).filter(UserModel.id == organizer_id).first()
    if not organizer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer not found"
        )
    
    new_event = EventModel(
        **event_data.dict(),
        organizer_id=organizer_id
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event

@router.get("/", response_model=List[Event])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all active events"""
    
    events = db.query(EventModel).filter(
        EventModel.is_active == True
    ).offset(skip).limit(limit).all()
    
    return events

@router.get("/{event_id}", response_model=EventWithTickets)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get specific event with tickets"""
    
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return event

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event_data: EventCreate, db: Session = Depends(get_db)):
    """Update event"""
    
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Update fields
    for key, value in event_data.dict().items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete event"""
    
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    event.is_active = False
    db.commit()
