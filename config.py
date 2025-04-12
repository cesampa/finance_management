ALLOWED_USERS = [
    "cesampa@gmail.com",
    "rrasampa@gmail.com"
]

DB_MODE = "sqlite"  # ou "postgres"

# Para SQLite
SQLITE_URL = "sqlite:///data.db"

# Para PostgreSQL (na AWS, por exemplo)
POSTGRES_URL = "postgresql+psycopg2://username:password@endpoint.amazonaws.com:5432/dbname"
