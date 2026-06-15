"""
QR Code routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Ticket as TicketModel, QRCode as QRCodeModel

router = APIRouter()

@router.get("/ticket/{ticket_id}")
def get_qr_code(ticket_id: int, db: Session = Depends(get_db)):
    """Get QR code for a ticket"""
    
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return {"qr_code": ticket.qr_code}

@router.post("/scan/{ticket_number}")
def scan_qr_code(ticket_number: str, db: Session = Depends(get_db)):
    """Scan QR code and verify ticket"""
    
    ticket = db.query(TicketModel).filter(
        TicketModel.ticket_number == ticket_number
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid QR code"
        )
    
    return {
        "valid": True,
        "ticket_number": ticket.ticket_number,
        "attendee_name": ticket.attendee_name,
        "attendee_email": ticket.attendee_email,
        "event_id": ticket.event_id,
        "is_used": ticket.is_used,
        "ticket_id": ticket.id
    }

@router.get("/lookup/{ticket_number}")
def lookup_ticket_by_qr(ticket_number: str, db: Session = Depends(get_db)):
    """Retrieve ticket details by ticket number (for QR scanning)"""
    
    ticket = db.query(TicketModel).filter(
        TicketModel.ticket_number == ticket_number
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Get the associated QR code record
    qr_code_record = db.query(QRCodeModel).filter(
        QRCodeModel.ticket_id == ticket.id
    ).first()
    
    return {
        "id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "attendee_name": ticket.attendee_name,
        "attendee_email": ticket.attendee_email,
        "event_id": ticket.event_id,
        "is_used": ticket.is_used,
        "used_at": ticket.used_at,
        "created_at": ticket.created_at,
        "qr_code_image": ticket.qr_code,
        "qr_data": qr_code_record.qr_data if qr_code_record else None
    }
