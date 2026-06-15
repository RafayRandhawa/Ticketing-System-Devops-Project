"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    event_date: datetime
    capacity: int
    ticket_price: float = 0.0

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    organizer_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EventWithTickets(Event):
    tickets: List['Ticket'] = []


# Ticket Schemas
class TicketBase(BaseModel):
    attendee_name: str
    attendee_email: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    event_id: int
    ticket_number: str
    user_id: int
    qr_code: Optional[str] = None
    is_used: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# QR Code Schemas
class QRCodeBase(BaseModel):
    pass

class QRCode(QRCodeBase):
    id: int
    ticket_id: int
    qr_data: str
    generated_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
    
EventWithTickets.model_rebuild()