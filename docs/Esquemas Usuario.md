# User Schemas Documentation

## Overview

Pydantic schemas for user operations in the Blog System API. These schemas handle validation and serialization for user registration, login, and responses.

## UsuarioBase

Base schema with common user fields.

**Fields:**

- `nombre_usuario` (str): Username
- `correo` (EmailStr): Email address with automatic validation

## UsuarioCreate

Used for user registration.

**Endpoint:** `POST /api/v1/auth/register`

**Fields:**

- `nombre_usuario` (str): Username (1-100 characters)
- `correo` (EmailStr): Valid email address  
- `contrasena` (str): Password (minimum 8 characters)

**Validation Rules:**

- Username: 1-100 characters
- Password: Minimum 8 characters
- Email: Valid format (handled by EmailStr)

**Example:**

```json
{
  "nombre_usuario": "john_doe",
  "correo": "john@example.com",
  "contrasena": "mypassword123"
}
```

## UsuarioLogin

Used for user authentication.

**Endpoint:** `POST /api/v1/auth/login`

**Fields:**

- `correo` (EmailStr): Email address
- `contrasena` (str): Password

**Example:**

```json
{
  "correo": "john@example.com",
  "contrasena": "mypassword123"
}
```

## UsuarioResponse

Used in API responses. Excludes sensitive fields like passwords.

**Fields:**

- `id` (int): User ID
- `nombre_usuario` (str): Username
- `correo` (EmailStr): Email address
- `created_at` (datetime): Account creation date
- `updated_at` (datetime): Last update date
- `ultimo_login` (datetime, optional): Last login date

**Example:**

```json
{
  "id": 1,
  "nombre_usuario": "john_doe",
  "correo": "john@example.com",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "ultimo_login": "2024-01-15T14:30:00Z"
}
```

## TokenResponse

Returned after successful login.

**Fields:**

- `access_token` (str): JWT access token
- `refresh_token` (str): JWT refresh token
- `token_type` (str): Always "bearer"
- `user` (UsuarioResponse): User profile data

**Example:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nombre_usuario": "john_doe",
    "correo": "john@example.com",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "ultimo_login": null
  }
}
```

## Security Features

- **Email validation**: Automatic format checking
- **Password protection**: Passwords never included in responses
- **Input validation**: All user input validated before processing
- **Length limits**: Prevents overly long inputs

## Error Responses

When validation fails, the API returns:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "contrasena"],
      "msg": "Contraseña debe tener mínimo 8 caracteres"
    }
  ]
}
```

## Usage in Code

```python
# Creating a user
user_data = UsuarioCreate(
    nombre_usuario="testuser",
    correo="test@example.com",
    contrasena="password123"
)

# Response serialization
user_response = UsuarioResponse.model_validate(db_user)
```
