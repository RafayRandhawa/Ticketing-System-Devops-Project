"""
QR Code Event Ticketing System - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from pathlib import Path
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends

# Import routers
from routes import events, tickets, qr_codes, auth, admin

# Initialize FastAPI app
app = FastAPI(
    title="QR Code Event Ticketing System",
    description="A system for managing events and generating QR code tickets",
    version="1.0.0"
)

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(qr_codes.router, prefix="/api/qr", tags=["QR Codes"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "QR Code Event Ticketing System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/ticket/{ticket_number}", response_class=HTMLResponse)
def view_ticket(ticket_number: str,db: Session = Depends(get_db)):
    """Display ticket details when QR code is scanned"""
    from models import Ticket as TicketModel, Event as EventModel
    
    # We need to get the db session manually since this is a special route
    
    ticket = db.query(TicketModel).filter(
        TicketModel.ticket_number == ticket_number
    ).first()
    
    if not ticket:
        return """
        <html>
            <head>
                <title>Ticket Not Found</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background-color: #f0f0f0; }
                    .container { background-color: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #d32f2f; }
                    p { color: #666; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>❌ Ticket Not Found</h1>
                    <p>The ticket you're looking for does not exist.</p>
                </div>
            </body>
        </html>
        """
    
    event = db.query(EventModel).filter(EventModel.id == ticket.event_id).first()
    status_badge = "✅ Valid" if not ticket.is_used else "🔴 Already Used"
    
    html_content = f"""
    <html>
        <head>
            <title>Ticket - {ticket.ticket_number}</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{ 
                    background-color: white; 
                    padding: 40px; 
                    border-radius: 15px; 
                    max-width: 600px; 
                    margin: 0 auto; 
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                }}
                h1 {{ 
                    color: #333; 
                    margin-top: 0;
                    text-align: center;
                    font-size: 28px;
                }}
                .ticket-number {{ 
                    background-color: #f5f5f5;
                    padding: 15px;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 20px;
                    text-align: center;
                    font-weight: bold;
                    color: #667eea;
                    margin: 20px 0;
                }}
                .field {{ 
                    margin: 15px 0; 
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-left: 4px solid #667eea;
                    border-radius: 4px;
                }}
                .label {{ 
                    font-weight: bold; 
                    color: #667eea; 
                    font-size: 12px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .value {{ 
                    color: #333; 
                    font-size: 16px;
                    margin-top: 5px;
                }}
                .status {{
                    text-align: center;
                    padding: 20px;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .status.valid {{
                    background-color: #e8f5e9;
                    color: #2e7d32;
                    border: 2px solid #4caf50;
                }}
                .status.used {{
                    background-color: #ffebee;
                    color: #c62828;
                    border: 2px solid #f44336;
                }}
                .qr-code {{
                    text-align: center;
                    margin: 30px 0;
                }}
                .qr-code img {{
                    max-width: 250px;
                    border: 3px solid #667eea;
                    border-radius: 8px;
                    padding: 10px;
                    background-color: white;
                }}
                .footer {{
                    text-align: center;
                    color: #999;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎟️ Your Event Ticket</h1>
                
                <div class="ticket-number">{ticket.ticket_number}</div>
                
                <div class="status {'valid' if not ticket.is_used else 'used'}">
                    {status_badge}
                </div>
                
                <div class="field">
                    <div class="label">Attendee Name</div>
                    <div class="value">{ticket.attendee_name}</div>
                </div>
                
                <div class="field">
                    <div class="label">Attendee Email</div>
                    <div class="value">{ticket.attendee_email}</div>
                </div>
                
                <div class="field">
                    <div class="label">Event</div>
                    <div class="value">{event.title if event else 'Unknown Event'}</div>
                </div>
                
                <div class="field">
                    <div class="label">Event Date</div>
                    <div class="value">{event.event_date.strftime('%B %d, %Y at %I:%M %p') if event else 'Unknown'}</div>
                </div>
                
                <div class="field">
                    <div class="label">Location</div>
                    <div class="value">{event.location if event and event.location else 'TBD'}</div>
                </div>
                
                <div class="qr-code">
                    <img src="{ticket.qr_code}" alt="QR Code">
                </div>
                
                <div class="footer">
                    <p>Ticket created on {ticket.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>Please present this ticket at the event entrance</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return html_content
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
