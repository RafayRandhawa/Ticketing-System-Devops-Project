"""
Tickets routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime
from database import get_db
from models import Ticket as TicketModel, Event as EventModel, User as UserModel, QRCode as QRCodeModel
from schemas import TicketCreate, Ticket
from utils.qr import generate_qr_code
from utils.auth import decode_token
from services.notificaion_service import NotificationService
from config import settings
from routes.auth import get_current_user

router = APIRouter()

def get_current_user_id(authorization: Optional[str] = Header(None), db: Session = None) -> int:
    """Get current user ID from token"""
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
            detail="Invalid token"
        )
    
    username = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user.id

@router.post("/{event_id}", response_model=Ticket)
def create_ticket(event_id: int, ticket_data: TicketCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Create a new ticket for an event"""
    
    # Check if event exists
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check capacity
    existing_tickets = db.query(TicketModel).filter(
        TicketModel.event_id == event_id
    ).count()
    
    if existing_tickets >= event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event capacity reached"
        )
    
    # Generate ticket number and QR code with URL
    ticket_number = str(uuid.uuid4())[:8].upper()
    # QR code contains URL for scanning with mobile devices
    qr_code_url = (
        f"{settings.base_url}/ticket/{ticket_number}"
    )
    qr_code = generate_qr_code(qr_code_url)
    
    new_ticket = TicketModel(
        event_id=event_id,
        ticket_number=ticket_number,
        qr_code=qr_code,
        user_id=current_user.id,
        **ticket_data.dict()
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    # Save QR code data to qr_codes table
    qr_code_record = QRCodeModel(
        ticket_id=new_ticket.id,
        qr_data=qr_code_url
    )
    db.add(qr_code_record)
    db.commit()
    db.refresh(qr_code_record)
    
    try:
        NotificationService.ticket_ready(
            ticket=new_ticket,
            event=event
        )
    except Exception as e:
        print(f"Notification failed: {e}")
    
    
    return new_ticket

@router.get("/", response_model=List[Ticket])
def list_all_tickets(db: Session = Depends(get_db)):
    """List all tickets - for testing only, should be restricted in production"""
    
    tickets = db.query(TicketModel).all()
    return tickets

@router.get("/{event_id}", response_model=List[Ticket])
def list_event_tickets(event_id: int, db: Session = Depends(get_db)):
    """List all tickets for an event"""
    
    # Check if event exists
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    tickets = db.query(TicketModel).filter(
        TicketModel.event_id == event_id
    ).all()
    
    return tickets

@router.get("/ticket/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get specific ticket"""
    
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return ticket

@router.post("/verify/{ticket_number}")
def verify_ticket(ticket_number: str, db: Session = Depends(get_db)):
    """Verify and mark ticket as used"""
    
    ticket = db.query(TicketModel).filter(
        TicketModel.ticket_number == ticket_number
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    if ticket.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket already used"
        )
    
    ticket.is_used = True
    ticket.used_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Ticket verified successfully", "ticket": ticket}
