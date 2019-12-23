from app.database import SessionLocal

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
