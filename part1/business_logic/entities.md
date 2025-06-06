# HBnB Business Entities Specification

## User Entity
**Attributes**:
- `id`: Universally unique identifier (UUIDv4)
- `is_admin`: Boolean (default: False)
- `password`: Stored as bcrypt hash
- Audit fields: `created_at`, `updated_at` (auto-set)

**Key Methods**:
```python
def register(email, password):
    """Validates email format and password strength"""
    # Minimum 8 chars, 1 number, 1 special char

def authenticate(password):
    """Returns JWT token if password matches"""
