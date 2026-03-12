import os


class Config:
    """Application configuration loaded from environment variables."""

    def __init__(self):
        # Flask
        self.SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
        self.DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

        # Database
        #
        # Preferred: provide DATABASE_URL (works for any SQLAlchemy-supported DB).
        # Otherwise defaults to MySQL, but falls back to SQLite for local dev
        # if DB_PASSWORD is empty (to avoid confusing "access denied" failures).
        database_url = (os.environ.get("DATABASE_URL") or "").strip()

        if database_url:
            self.SQLALCHEMY_DATABASE_URI = database_url
        else:
            db_user = os.environ.get("DB_USER", "root")
            db_password = os.environ.get("DB_PASSWORD", "")
            db_host = os.environ.get("DB_HOST", "localhost")
            db_port = os.environ.get("DB_PORT", "3306")
            db_name = os.environ.get("DB_NAME", "notes_db")

            use_sqlite = os.environ.get("USE_SQLITE", "1") == "1"
            if use_sqlite and db_password == "":
                self.SQLALCHEMY_DATABASE_URI = "sqlite:///notes_local.db"
            else:
                # Using PyMySQL as MySQL driver
                self.SQLALCHEMY_DATABASE_URI = (
                    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
                )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # JWT
        self.JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-secret")
        self.JWT_ALGORITHM = "HS256"
        self.JWT_EXPIRATION_MINUTES = int(os.environ.get("JWT_EXPIRATION_MINUTES", "60"))

        # Pagination
        self.DEFAULT_PAGE_SIZE = int(os.environ.get("DEFAULT_PAGE_SIZE", "10"))
        self.MAX_PAGE_SIZE = int(os.environ.get("MAX_PAGE_SIZE", "50"))

