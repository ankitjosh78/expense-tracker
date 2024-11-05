# Expense Tracker API

This Expense Tracker API is a backend application designed to manage expenses, split them among multiple users, and track outstanding balances between users. It supports flexible split types (equal, exact, percentage) and allows users to settle debts through transactions.

## Features

- **Expense Management**: Create, view, and manage expenses with multiple splitting options.
- **Balance Management**: Track outstanding balances between users to help users see who owes whom.
- **Transaction Handling**: Settle debts through transactions that update balances accordingly.
- **User Authentication**: Secure user authentication using JWT (JSON Web Tokens) for access control.

## Requirements

- Python 3.8+
- Django 4.0+
- Django REST Framework
- PostgreSQL (recommended for production)
- SimpleJWT (for JWT-based authentication)

## Getting Started

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/expense-tracker-api.git
   cd expense-tracker-api
   ```
2. **Create a virtual environment**

  ```bash
  python -m venv venv
  source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
  ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the server**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
```
POST /api/token/: Obtain JWT token for authentication.
POST /api/token/refresh/: Refresh JWT token.
```

### Expense Management
```
POST /api/expenses/: Create a new expense (only accessible by authenticated users).
GET /api/expenses/: List all expenses.
GET /api/expenses/<id>/: Retrieve, update, or delete a specific expense.
```

### Balances
```
GET /api/balances/: View all outstanding balances between users.
```

### Transactions
```
POST /api/transactions/: Create a transaction to settle balance between two users.
```

## Sample Payloads (Authentication must be provided)

### Create Expense

```json
{
  "title": "Team Lunch",
  "amount": 300,
  "split_type": "exact",
  "splits": [
    {"user": 1, "split_value": 100},
    {"user": 2, "split_value": 50},
    {"user": 3, "split_value": 150}
  ]
}
```

### Create Transaction

```json
{
  "payee": 2,
  "amount": 50.00
}
```
