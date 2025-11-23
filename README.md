# Late Show API

A RESTful API built with Flask for managing late show episodes, guests, and their appearances. This API allows you to track episodes, manage guest information, and record guest appearances with ratings.

## Features

- **Episodes Management**: Create and manage late show episodes with dates and episode numbers
- **Guests Management**: Track guest information including name and occupation
- **Appearances Tracking**: Record guest appearances on episodes with ratings (1-5 scale)
- **RESTful API**: Clean REST endpoints for all resources
- **Database Migrations**: Uses Flask-Migrate for database schema management
- **Testing**: Comprehensive test suite with pytest

## Tech Stack

- **Flask** 2.3.0 - Web framework
- **Flask-SQLAlchemy** 3.0.3 - ORM for database operations
- **Flask-Migrate** 4.0.4 - Database migration tool
- **Flask-RESTful** 0.3.10 - REST API framework
- **SQLAlchemy-serializer** 1.4.1 - Model serialization
- **SQLite** - Database (development)
- **pytest** 7.3.1 - Testing framework

## Project Structure

```
late-show-api/
├── server/
│   ├── app.py              # Main Flask application and API routes
│   ├── config.py           # Database configuration
│   ├── models.py           # SQLAlchemy models (Episode, Guest, Appearance)
│   ├── seed.py             # Database seeding script
│   ├── migrations/         # Alembic database migrations
│   ├── testing/            # Test files
│   │   ├── conftest.py     # Pytest fixtures
│   │   ├── app_test.py     # API endpoint tests
│   │   └── models_test.py  # Model tests
│   └── instance/
│       └── app.db          # SQLite database file
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd late-show-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**
   ```bash
   cd server
   flask db upgrade
   ```

6. **Seed the database (optional)**
   ```bash
   python seed.py
   ```

## Running the Application

Start the Flask development server:

```bash
cd server
python app.py
```

The API will be available at `http://localhost:5555`

## API Endpoints

### Episodes

- **GET /episodes**
  - Returns a list of all episodes
  - Response: `[{"id": 1, "date": "1/11/99", "number": 1}, ...]`

- **GET /episodes/<id>**
  - Returns a specific episode with its appearances
  - Response includes episode details and nested guest information for each appearance

- **DELETE /episodes/<id>**
  - Deletes an episode and its associated appearances (cascade delete)
  - Returns 204 No Content on success

### Guests

- **GET /guests**
  - Returns a list of all guests
  - Response: `[{"id": 1, "name": "Michael J. Fox", "occupation": "Actor"}, ...]`

### Appearances

- **POST /appearances**
  - Creates a new appearance record
  - Required fields: `rating` (1-5), `episode_id`, `guest_id`
  - Validates that episode and guest exist
  - Validates rating is between 1 and 5
  - Returns the created appearance with nested episode and guest data

## Database Models

### Episode
- `id` (Integer, Primary Key)
- `date` (String) - Episode date
- `number` (Integer) - Episode number
- Relationships: `appearances`, `guests` (through appearances)

### Guest
- `id` (Integer, Primary Key)
- `name` (String) - Guest name
- `occupation` (String) - Guest occupation
- Relationships: `appearances`, `episodes` (through appearances)

### Appearance
- `id` (Integer, Primary Key)
- `rating` (Integer) - Rating from 1 to 5 (validated)
- `episode_id` (Integer, Foreign Key) - Reference to Episode
- `guest_id` (Integer, Foreign Key) - Reference to Guest
- Relationships: `episode`, `guest`

## Example Usage

### Get all episodes
```bash
curl http://localhost:5555/episodes
```

### Get a specific episode
```bash
curl http://localhost:5555/episodes/1
```

### Get all guests
```bash
curl http://localhost:5555/guests
```

### Create an appearance
```bash
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "episode_id": 1,
    "guest_id": 1
  }'
```

### Delete an episode
```bash
curl -X DELETE http://localhost:5555/episodes/1
```

## Testing

Run the test suite using pytest:

```bash
cd server
pytest testing/
```

The test suite includes:
- API endpoint tests
- Model validation tests
- Database relationship tests

Tests use an in-memory SQLite database for isolation and speed.

## Database Migrations

This project uses Flask-Migrate (Alembic) for database migrations.

**Create a new migration:**
```bash
cd server
flask db migrate -m "Description of changes"
```

**Apply migrations:**
```bash
flask db upgrade
```

**Rollback a migration:**
```bash
flask db downgrade
```

## Development

### Seeding the Database

The `seed.py` script populates the database with sample data:

```bash
cd server
python seed.py
```

This creates:
- 5 sample episodes
- 6 sample guests
- 10 sample appearances

### Configuration

Database configuration is set in `server/app.py`:
- Development: SQLite database at `instance/app.db`
- Testing: In-memory SQLite database

## License

This project is part of a learning exercise and is available for educational purposes.

