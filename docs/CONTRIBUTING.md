# Contributing Guide

## Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Git

### Local Development Environment

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd QR_Code_Event_Ticketing_System
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install pytest pytest-asyncio
   ```

4. **Setup database**:
   ```bash
   createdb ticketing_system
   psql ticketing_system < ../database/init.sql
   ```

5. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

6. **Run tests**:
   ```bash
   pytest
   ```

7. **Start development server**:
   ```bash
   uvicorn main:app --reload
   ```

## Code Style & Standards

### Python Code Style
- Follow PEP 8
- Use Black for code formatting
- Use flake8 for linting

```bash
pip install black flake8
black .
flake8 .
```

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private variables: `_leading_underscore`

### Type Hints
Always use type hints in function signatures:
```python
def create_event(event_data: EventCreate, db: Session) -> Event:
    pass
```

## Git Workflow

### Branch Naming
- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Hotfix: `hotfix/description`

### Commit Messages
```
[TYPE] Short description (50 chars)

Detailed explanation of changes (72 chars per line)
- Point 1
- Point 2

Closes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Process
1. Create feature branch
2. Make changes and commit
3. Push to remote
4. Create pull request
5. Request review
6. Address feedback
7. Merge when approved

## Testing

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest --cov=. --cov-report=html
```

### Test File Structure
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_utils.py
├── integration/
│   ├── test_auth.py
│   ├── test_events.py
│   └── test_tickets.py
└── conftest.py
```

## Adding New Features

### Backend: Add New API Endpoint

1. **Create model** in `models/__init__.py`
2. **Create schema** in `schemas/__init__.py`
3. **Create route** in `routes/new_feature.py`
4. **Add to main.py**: `app.include_router(new_feature.router)`
5. **Write tests**
6. **Update API_DOCUMENTATION.md**

Example:
```python
# models/__init__.py
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    rating = Column(Integer)

# schemas/__init__.py
class ReviewCreate(BaseModel):
    rating: int
    comment: str

# routes/reviews.py
@router.post("/{ticket_id}", response_model=Review)
def create_review(ticket_id: int, review: ReviewCreate, db: Session):
    # Implementation
    pass
```

### Frontend: Add New Page

1. **Add HTML section** in `index.html`
2. **Add styles** in `styles.css`
3. **Add JavaScript** in `script.js`
4. **Add navigation** link

## Documentation

- Update README.md for major changes
- Update API_DOCUMENTATION.md for API changes
- Add docstrings to all functions
- Use markdown for clarity

## Reporting Bugs

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment info
- Screenshots/logs

## Feature Requests

Include:
- Clear description
- Use cases
- Mockups/wireframes (if applicable)
- Acceptance criteria

## Performance Guidelines

- Optimize database queries (use indices)
- Cache frequently accessed data
- Paginate large result sets
- Use async functions where applicable
- Profile before optimizing

## Security Guidelines

- Validate all inputs
- Use parameterized queries
- Never log passwords
- Sanitize user inputs
- Use strong secret keys
- Keep dependencies updated

## Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] No hard-coded secrets
- [ ] No unused imports
- [ ] Error handling is proper
- [ ] Performance is acceptable
- [ ] Security best practices followed

## Questions?

- Create an issue
- Check existing documentation
- Discuss in pull request comments
- Reach out to maintainers
