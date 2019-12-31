from app.database import DBSession

# Dependency
def get_db():
    try:
        db_session = DBSession()
        yield db_session
    finally:
        db_session.close()
