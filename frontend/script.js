// API Configuration
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api'
    : `${window.location.origin}/api`;

// State management
let currentUser = null;
let currentPage = 'login';

// Check if user is logged in on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = sessionStorage.getItem('token');
    if (token) {
        // Try to verify token is still valid
        getCurrentUser();
    } else {
        navigate('login');
    }
});

// Navigation
function navigate(page) {

    // Role protection
    if (currentUser) {

        // Admin-only pages
        if (
            ['admin', 'scan'].includes(page) &&
            currentUser.role !== 'admin'
        ) {
            showAlert(
                'Access denied. Administrator privileges required.',
                'error'
            );
            return;
        }

        // Admin + Organizer pages
        if (
            page === 'create-event' &&
            !['admin', 'organizer'].includes(currentUser.role)
        ) {
            showAlert(
                'Access denied. Organizer or Administrator privileges required.',
                'error'
            );
            return;
        }
    }

    document.querySelectorAll('.page')
        .forEach(pageEl => pageEl.classList.remove('active'));

    const selectedPage = document.getElementById(page);

    if (!selectedPage) {
        console.error(`Page '${page}' not found`);
        return;
    }

    selectedPage.classList.add('active');
    currentPage = page;

    switch (page) {

        case 'events':
            loadEvents();
            break;

        case 'my-tickets':
            loadMyTickets();
            break;

        case 'admin':
            loadAdminStats();
            loadAdminUsers();
            loadAdminEvents();
            loadAdminTickets();
            break;

        case 'home':
            updateNavigation();
            break;
    }
}
function canManageEvents() {
    return currentUser &&
        (
            currentUser.role === 'admin' ||
            currentUser.role === 'organizer'
        );
}
// Update navbar visibility based on authentication
function updateNavigation() {

    const token = sessionStorage.getItem('token');
    const quickActions = document.getElementById('quickActions');
    const navbar = document.getElementById('navbar');
    const logoutBtn = document.getElementById('logoutBtn');
    const adminLink = document.getElementById('adminLink');

    const scanLinks = document.querySelectorAll('.admin-only');

    if (!token || !currentUser) {

        navbar.classList.remove('visible');

        logoutBtn.style.display = 'none';

        adminLink.style.display = 'none';

        scanLinks.forEach(el => {
            el.style.display = 'none';
        });

        return;
    }
    if (quickActions) {
        quickActions.style.display =
            canManageEvents()
                ? 'flex'
                : 'none';
    }
    navbar.classList.add('visible');

    logoutBtn.style.display = 'block';

    if (currentUser.role === 'admin') {

        adminLink.style.display = 'block';

        scanLinks.forEach(el => {
            el.style.display = 'inline-flex';
        });

    } else {

        adminLink.style.display = 'none';

        scanLinks.forEach(el => {
            el.style.display = 'none';
        });
    }

    updateUserDisplay();
}

// Auth functions
async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const button = e.target.querySelector('button[type="submit"]');
    try {
        
        setButtonLoading(button, true);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        if (handleUnauthorized(response)) return;

        const data = await response.json();

        if (response.ok) {
            sessionStorage.setItem('token', data.access_token);
            document.getElementById('loginForm').reset();
            getCurrentUser();
        } else {
            showAlert('Invalid username or password', 'error');
        }
    } catch (error) {
        console.error('Login failed:', error);
        showAlert('Login failed. Please check your connection.', 'error');
    } finally {
        setButtonLoading(button, false);
    }
}

function updateUserDisplay() {

    if (!currentUser) return;

    const brand = document.querySelector('.nav-subtitle');

    if (brand) {
        brand.innerHTML =
            `Logged in as <strong>${currentUser.full_name || currentUser.username}</strong>`;
    }

    const userName =
        document.getElementById('userName');

    const userRole =
        document.getElementById('userRole');

    const profile =
        document.getElementById('userProfile');

    if (userName)
        userName.textContent =
            currentUser.full_name || currentUser.username;

    if (userRole)
        userRole.textContent =
            currentUser.role;

    if (profile)
        profile.style.display = 'flex';
}

async function handleRegister(e) {
    e.preventDefault();

    const full_name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const button = e.target.querySelector('button[type="submit"]');
    try {
        
        setButtonLoading(button, true);

        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password, full_name })
        });
        if (handleUnauthorized(response)) return;

        const data = await response.json();

        if (response.ok) {
            showAlert('Account created successfully! Please login.', 'success');
            document.getElementById('registerForm').reset();
            navigate('login');
        } else {
            showAlert(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration failed:', error);
        showAlert('Registration failed. Please check your connection.', 'error');
    } finally {
        setButtonLoading(button, false);
    }
}

async function getCurrentUser() {
    const token = sessionStorage.getItem('token');

    if (!token) {
        navigate('login');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            currentUser = await response.json();
            updateNavigation();
            navigate('home');
        } else {
            sessionStorage.removeItem('token');
            navigate('login');
        }
    } catch (error) {
        console.error('Failed to get user:', error);
        navigate('login');
    }
}

function logout() {
    sessionStorage.removeItem('token');
    currentUser = null;
    updateNavigation();
    navigate('login');
    showAlert('You have been logged out', 'success');
}

function getAuthHeader() {
    const token = sessionStorage.getItem('token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// Alert/notification helper
function showAlert(message, type = 'info') {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '1000';
    alert.style.maxWidth = '400px';

    document.body.appendChild(alert);

    // Remove after 3 seconds
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

// Event functions
async function loadEvents() {
    try {
        const response = await fetch(`${API_URL}/events/`, {
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        const events = await response.json();
        const eventsGrid = document.getElementById('eventsGrid');

        if (events.length === 0) {
            eventsGrid.innerHTML = `
                <div class="empty-state">
                    <h3>📅 No Events Available</h3>
                    <p>No events have been created yet.</p>
                </div>
                `;
            return;
        }

        eventsGrid.innerHTML = events.map(event => `
            <div class="event-card">
                <h3>${event.title}</h3>
                <p>${event.description || 'No description'}</p>
                <p class="event-date">📅 ${new Date(event.event_date).toLocaleDateString()}</p>
                <p class="event-capacity">👥 ${event.capacity} tickets</p>
                <p>💵 $${event.ticket_price}</p>
                <button onclick="buyTicket(${event.id})" class="btn btn-primary">Buy Ticket</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load events:', error);
        showAlert('Failed to load events', 'error');
    }
}

async function createEventHandler(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('eventForm'));
    const eventData = {
        title: formData.get('title'),
        description: formData.get('description'),
        location: formData.get('location'),
        event_date: new Date(formData.get('event_date')).toISOString(),
        capacity: parseInt(formData.get('capacity')),
        ticket_price: parseFloat(formData.get('ticket_price')) || 0
    };

    try {
        const response = await fetch(`${API_URL}/events/`, {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({
                ...eventData
            })
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            showAlert('Event created successfully!', 'success');
            document.getElementById('eventForm').reset();
            loadEvents();
        } else {
            showAlert('Failed to create event', 'error');
        }
    } catch (error) {
        console.error('Failed to create event:', error);
        showAlert('Failed to create event', 'error');
    }
}

// Ticket functions
async function buyTicket(eventId) {
    // Use currently logged-in user's information
    if (!currentUser) {
        showAlert('Please log in first', 'error');
        return;
    }

    const attendeeName = currentUser.full_name;
    const attendeeEmail = currentUser.email;

    try {
        const response = await fetch(`${API_URL}/tickets/${eventId}`, {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({
                attendee_name: attendeeName,
                attendee_email: attendeeEmail
            })
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            showAlert('Ticket purchased successfully!', 'success');
            loadMyTickets();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to buy ticket', 'error');
        }
    } catch (error) {
        console.error('Failed to buy ticket:', error);
        showAlert('Failed to buy ticket', 'error');
    }
}

async function loadMyTickets() {
    try {
        // Get all tickets (simplified endpoint)
        const response = await fetch(`${API_URL}/tickets/`, {
            headers: getAuthHeader()
        });

        let tickets = [];
        if (response.ok) {
            tickets = await response.json();
            console.log('All tickets before filter:', tickets);
            console.log('Current user ID:', currentUser.id);
            console.log('Current user:', currentUser);
            
            tickets = tickets.filter(
                ticket => ticket.user_id === currentUser.id
            );
        }

        if (handleUnauthorized(response)) return;
        const ticketsList = document.getElementById('ticketsList');

        if (!tickets || tickets.length === 0) {
            ticketsList.innerHTML = `
                <div class="empty-state">
                    <h3>🎫 No Tickets Found</h3>
                    <p>You haven't purchased any tickets yet.</p>
                </div>
                `;
            return;
        }

        ticketsList.innerHTML = tickets.map(ticket => `
            <div class="ticket-item">
                <h4>${ticket.ticket_number}</h4>
                <p><strong>Name:</strong> ${ticket.attendee_name}</p>
                <p><strong>Email:</strong> ${ticket.attendee_email}</p>
                <p><strong>Status:</strong> ${ticket.is_used ? '✅ Used' : '⏳ Unused'}</p>
                ${ticket.qr_code ? `<div class="qr-code"><img src="${ticket.qr_code}" alt="QR Code" style="max-width: 200px;"></div>` : ''}
                <button onclick="downloadTicket('${ticket.ticket_number}')" class="btn btn-success">Download</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load tickets:', error);
        showAlert('Failed to load tickets', 'error');
    }
}



function downloadTicket(ticketNumber) {

    window.open(
        `${API_URL.replace('/api', '')}/ticket/${ticketNumber}`,
        '_blank'
    );
}

// QR Code scanning
async function scanTicket() {
    const ticketNumber = document.getElementById('scanInput').value;

    if (!ticketNumber) {
        showAlert('Please enter a ticket number', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/qr/scan/${ticketNumber}`, {
            method: 'POST',
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        const result = await response.json();
        const scanResult = document.getElementById('scanResult');

        if (response.ok) {
            scanResult.className = 'success';
            scanResult.innerHTML = `
                <strong>✅ Valid Ticket</strong><br>
                Name: ${result.attendee_name}<br>
                Status: ${result.is_used ? 'Already Used' : 'Valid'}
            `;
        } else {
            scanResult.className = 'error';
            scanResult.innerHTML = '<strong>❌ Invalid Ticket</strong>';
        }
    } catch (error) {
        console.error('Scan failed:', error);
        const scanResult = document.getElementById('scanResult');
        scanResult.className = 'error';
        scanResult.innerHTML = '<strong>❌ Scan Error</strong>';
    }
}

// Admin Panel Functions
function showAdminTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.admin-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

// Load admin statistics
async function loadAdminStats() {
    try {
        const response = await fetch(`${API_URL}/admin/stats`, {
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            const stats = await response.json();

            document.getElementById('stat-users').textContent = stats.total_users;
            document.getElementById('stat-events').textContent = stats.total_events;
            document.getElementById('stat-tickets').textContent = stats.total_tickets;
            document.getElementById('stat-used').textContent = stats.tickets_used;

            const roleStats = `
                <p>👨‍💼 Admin: <strong>${stats.users_by_role.admin}</strong></p>
                <p>🎯 Organizer: <strong>${stats.users_by_role.organizer}</strong></p>
                <p>👤 User: <strong>${stats.users_by_role.user}</strong></p>
            `;
            document.getElementById('role-stats').innerHTML = roleStats;
        }
    } catch (error) {
        console.error('Failed to load admin stats:', error);
    }
}

// Load all users for admin
async function loadAdminUsers() {
    try {
        const response = await fetch(`${API_URL}/admin/users`, {
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            const users = await response.json();
            const tbody = document.getElementById('usersTable');

            tbody.innerHTML = users.map(user => `
                <tr>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.full_name}</td>
                    <td>
                        <select onchange="updateUserRole(${user.id}, this.value)" class="role-select">
                            <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                            <option value="organizer" ${user.role === 'organizer' ? 'selected' : ''}>Organizer</option>
                            <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                        </select>
                    </td>
                    <td>${user.is_active ? '✅ Active' : '❌ Inactive'}</td>
                    <td>
                        <button onclick="toggleUserStatus(${user.id}, ${user.is_active})" class="btn btn-small">
                            ${user.is_active ? 'Deactivate' : 'Activate'}
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load users:', error);
        showAlert('Failed to load users', 'error');
    }
}

// Update user role
async function updateUserRole(userId, newRole) {
    try {
        const response = await fetch(`${API_URL}/admin/users/${userId}/role`, {
            method: 'POST',
            headers: getAuthHeader(),
            body: JSON.stringify({ role: newRole })
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            showAlert('User role updated successfully', 'success');
        } else {
            showAlert('Failed to update user role', 'error');
        }
    } catch (error) {
        console.error('Failed to update user role:', error);
        showAlert('Failed to update user role', 'error');
    }
}

// Toggle user status
async function toggleUserStatus(userId, currentStatus) {
    const endpoint = currentStatus ? 'deactivate' : 'activate';

    try {
        const response = await fetch(`${API_URL}/admin/users/${userId}/${endpoint}`, {
            method: 'POST',
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            showAlert(`User ${endpoint}d successfully`, 'success');
            loadAdminUsers();
        } else {
            showAlert(`Failed to ${endpoint} user`, 'error');
        }
    } catch (error) {
        console.error(`Failed to ${endpoint} user:`, error);
        showAlert(`Failed to ${endpoint} user`, 'error');
    }
}

// Load all events for admin
async function loadAdminEvents() {
    try {
        const response = await fetch(`${API_URL}/admin/events`, {
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            const events = await response.json();
            const tbody = document.getElementById('eventsTable');

            tbody.innerHTML = events.map(event => `
                <tr>
                    <td>${event.title}</td>
                    <td>${event.location}</td>
                    <td>${new Date(event.event_date).toLocaleDateString()}</td>
                    <td>${event.capacity}</td>
                    <td>${event.is_active ? '✅ Active' : '❌ Inactive'}</td>
                    <td>
                        <button onclick="deleteEvent(${event.id})" class="btn btn-small btn-danger">Delete</button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load events:', error);
        showAlert('Failed to load events', 'error');
    }
}

// Delete event
async function deleteEvent(eventId) {
    if (confirm('Are you sure you want to delete this event?')) {
        try {
            const response = await fetch(`${API_URL}/admin/events/${eventId}`, {
                method: 'DELETE',
                headers: getAuthHeader()
            });
            if (handleUnauthorized(response)) return;
            if (response.ok) {
                showAlert('Event deleted successfully', 'success');
                loadAdminEvents();
            } else {
                showAlert('Failed to delete event', 'error');
            }
        } catch (error) {
            console.error('Failed to delete event:', error);
            showAlert('Failed to delete event', 'error');
        }
    }
}

// Load all tickets for admin
async function loadAdminTickets() {
    try {
        const response = await fetch(`${API_URL}/admin/tickets`, {
            headers: getAuthHeader()
        });
        if (handleUnauthorized(response)) return;
        if (response.ok) {
            const tickets = await response.json();
            const tbody = document.getElementById('ticketsTable');

            tbody.innerHTML = tickets.map(ticket => `
                <tr>
                    <td>${ticket.ticket_number}</td>
                    <td>${ticket.attendee_name}</td>
                    <td>${ticket.attendee_email}</td>
                    <td>${ticket.event_id}</td>
                    <td>${ticket.is_used ? '✅ Used' : '⏳ Unused'}</td>
                    <td>${new Date(ticket.created_at).toLocaleDateString()}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load tickets:', error);
        showAlert('Failed to load tickets', 'error');
    }
}

function setButtonLoading(button, loading = true) {

    if (!button) return;

    if (loading) {

        button.dataset.originalText =
            button.innerHTML;

        button.disabled = true;

        button.innerHTML =
            '⏳ Please wait...';

    } else {

        button.disabled = false;

        button.innerHTML =
            button.dataset.originalText;
    }
}

function handleUnauthorized(response) {

    if (response.status === 401) {

        logout();

        showAlert(
            'Session expired. Please login again.',
            'error'
        );

        return true;
    }

    return false;
}