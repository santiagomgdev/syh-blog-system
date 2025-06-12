# Database Models Documentation

## Overview

This document describes the database models used in the Blog System API, their relationships, and usage patterns.

## User Models

### Usuario Model

**File**: `app/core/models/user/user.py`

**Description**: Core user model for authentication and user management.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `nombre_usuario` | String(50) | Unique, Not Null | Username for login and display |
| `correo` | String(100) | Unique, Not Null | Email address for authentication |
| `contrasena_hash` | String(255) | Not Null | Bcrypt hashed password |
| `sal` | String(50) | Not Null | Cryptographic salt for password |
| `ultimo_login` | DateTime | Nullable | Last successful login timestamp |
| `created_at` | DateTime | Not Null, Auto | Account creation timestamp |
| `updated_at` | DateTime | Not Null, Auto | Last modification timestamp |

#### Relationships

- **tokens**: One-to-Many with `Token` model (JWT refresh tokens)
- **roles**: One-to-Many with `RolUsuario` model (user permissions)
- **posts**: One-to-Many with `Post` model (authored blog posts)
- **comentarios**: One-to-Many with `Comentario` model (user comments)

#### Indexes

- `ix_usuarios_correo`: Unique index on email field
- `ix_usuarios_nombre_usuario`: Unique index on username field
- `ix_usuarios_deleted_at`: Index for soft delete queries

#### Usage Examples

```python
# Create a new user
from app.core.models.user.user import Usuario
from app.utils.security import hash_password, generate_salt

salt = generate_salt()
hashed_password = hash_password("user_password")

user = Usuario(
    nombre_usuario="john_doe",
    correo="john@example.com",
    contrasena_hash=hashed_password,
    sal=salt
)

# Check if user is active
if user.is_active:
    print(f"User {user.display_name} is active")

# Soft delete user
user.soft_delete()
```

#### Security Considerations

- Passwords are never stored in plain text
- All passwords use bcrypt hashing with individual salts
- Email addresses are case-sensitive and globally unique
- Soft deletion preserves referential integrity
- Last login tracking for security monitoring

---

### Token Model

**File**: `app/core/models/user/token.py`

**Description**: JWT refresh token management for user sessions.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Token identifier |
| `usuario_id` | Integer | Foreign Key, Not Null | Reference to Usuario |
| `token_refresco` | String(255) | Not Null | JWT refresh token |
| `emitido_en` | DateTime | Not Null, Auto | Token issue timestamp |
| `expira_en` | DateTime | Not Null | Token expiration timestamp |
| `revocado` | Boolean | Default False | Token revocation status |

#### Relationships

- **usuario**: Many-to-One with `Usuario` model

---

### RolUsuario Model

**File**: `app/core/models/user/role.py`

**Description**: User role assignment for authorization.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Role assignment identifier |
| `usuario_id` | Integer | Foreign Key, Not Null | Reference to Usuario |
| `nombre_rol` | String(50) | Not Null | Role name (USER, ADMIN, etc.) |

#### Relationships

- **usuario**: Many-to-One with `Usuario` model

#### Available Roles

- `USER`: Default role for registered users
- `ADMIN`: Administrative privileges
- `MODERATOR`: Content moderation privileges

---

## Blog Models

### Post Model

**File**: `app/core/models/blog/post.py`

**Description**: Blog post content and metadata.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Post identifier |
| `usuario_id` | Integer | Foreign Key, Not Null | Author reference |
| `titulo` | String(255) | Not Null | Post title |
| `enlace` | String(255) | Unique, Not Null | URL slug |
| `contenido` | Text | Not Null | Post content |
| `resumen` | Text | Nullable | Post summary/excerpt |
| `estado` | Enum | Not Null | Publication status |
| `created_at` | DateTime | Not Null, Auto | Creation timestamp |
| `updated_at` | DateTime | Not Null, Auto | Last update timestamp |
| `deleted_at` | DateTime | Nullable | Soft deletion timestamp |

#### Post States

- `borrador`: Draft post, not published
- `publicado`: Published and visible
- `archivado`: Archived, not visible

#### Relationships

- **usuario**: Many-to-One with `Usuario` model (author)
- **comentarios**: One-to-Many with `Comentario` model

---

### Comentario Model

**File**: `app/core/models/blog/comment.py`

**Description**: User comments on blog posts with threading support.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Comment identifier |
| `post_id` | Integer | Foreign Key, Not Null | Reference to Post |
| `usuario_id` | Integer | Foreign Key, Not Null | Reference to Usuario |
| `padre_id` | Integer | Foreign Key, Nullable | Parent comment for threading |
| `contenido` | Text | Not Null | Comment content |
| `estado` | Enum | Not Null | Moderation status |
| `created_at` | DateTime | Not Null, Auto | Creation timestamp |
| `updated_at` | DateTime | Not Null, Auto | Last update timestamp |

#### Comment States

- `pendiente`: Awaiting moderation
- `aprobado`: Approved and visible
- `spam`: Marked as spam
- `rechazado`: Rejected by moderator

#### Relationships

- **post**: Many-to-One with `Post` model
- **usuario**: Many-to-One with `Usuario` model (author)
- **padre**: Self-referential for comment threading
- **respuestas**: One-to-Many self-referential for replies

---

## Database Schema Diagram

```txt
Usuario (users)
├── id (PK)
├── nombre_usuario
├── correo
├── contrasena_hash
├── sal
├── ultimo_login
├── created_at
├── updated_at
└── deleted_at

Token (tokens)
├── id (PK)
├── usuario_id (FK → Usuario.id)
├── token_refresco
├── emitido_en
├── expira_en
└── revocado

RolUsuario (roles_usuario)
├── id (PK)
├── usuario_id (FK → Usuario.id)
└── nombre_rol

Post (posts)
├── id (PK)
├── usuario_id (FK → Usuario.id)
├── titulo
├── enlace
├── contenido
├── resumen
├── estado
├── created_at
└── updated_at

Comentario (comentarios)
├── id (PK)
├── post_id (FK → Post.id)
├── usuario_id (FK → Usuario.id)
├── padre_id (FK → Comentario.id)
├── contenido
├── estado
├── created_at
└── updated_at
```
