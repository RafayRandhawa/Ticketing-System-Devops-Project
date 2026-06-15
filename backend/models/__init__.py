"""
SQLAlchemy models for the application
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default='user', index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    events = relationship("Event", back_populates="organizer")

class Event(Base):
    """Event model"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location = Column(String(255))
    event_date = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    ticket_price = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organizer = relationship("User", back_populates="events")
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")

class Ticket(Base):
    """Ticket model"""
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False)
    qr_code = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    attendee_name = Column(String(100), nullable=False)
    attendee_email = Column(String(100), nullable=False)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    event = relationship("Event", back_populates="tickets")

class QRCode(Base):
    """QR Code model"""
    __tablename__ = "qr_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), unique=True, nullable=False)
    qr_data = Column(String(500), nullable=False)
    image_path = Column(String(255))
    generated_at = Column(DateTime, default=datetime.utcnow)
