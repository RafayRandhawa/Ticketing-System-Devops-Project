-- QR Code Event Ticketing System - Database Schema
-- PostgreSQL

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS qr_codes CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    organizer_id INTEGER NOT NULL,
    location VARCHAR(255),
    event_date TIMESTAMP NOT NULL,
    capacity INTEGER NOT NULL,
    ticket_price FLOAT DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

-- Tickets table
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    qr_code TEXT,
    attendee_name VARCHAR(100) NOT NULL,
    attendee_email VARCHAR(100) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- QR Codes table
CREATE TABLE qr_codes (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL UNIQUE,
    qr_data VARCHAR(500) NOT NULL,
    image_path VARCHAR(255),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);

-- Create indexes for better query performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_events_organizer_id ON events(organizer_id);
CREATE INDEX idx_events_is_active ON events(is_active);
CREATE INDEX idx_tickets_event_id ON tickets(event_id);
CREATE INDEX idx_tickets_ticket_number ON tickets(ticket_number);
CREATE INDEX idx_tickets_is_used ON tickets(is_used);
CREATE INDEX idx_qr_codes_ticket_id ON qr_codes(ticket_id);

-- Insert sample data
INSERT INTO users (username, email, hashed_password, full_name, role) VALUES
    ('admin', 'admin@example.com', '$2b$12$eImiTXuWVxfaHNYY0iNAUeuK7w9JJ5v3a3XHOJCHPAWKhPyW8MDCO', 'Admin User', 'admin'),
    ('organizer1', 'organizer1@example.com', '$2b$12$eImiTXuWVxfaHNYY0iNAUeuK7w9JJ5v3a3XHOJCHPAWKhPyW8MDCO', 'Event Organizer', 'organizer');

INSERT INTO events (title, description, organizer_id, location, event_date, capacity, ticket_price) VALUES
    ('Tech Conference 2026', 'Annual technology conference', 2, 'Convention Center', '2026-07-15 09:00:00', 500, 99.99),
    ('Music Festival', 'Summer music festival', 2, 'Central Park', '2026-08-20 18:00:00', 1000, 49.99);

-- Commit changes
COMMIT;
