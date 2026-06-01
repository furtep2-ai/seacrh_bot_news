from admin_tools.database import SessionLocal, User
from sqlalchemy import delete, insert

def delete_user(user_id: int):
    with SessionLocal() as session:
        query = delete(User).where(User.user_id == user_id)
        result = session.execute(query)
        session.commit()
        return True if result.rowcount>0 else False
    
def create_user(user_id: int, user_name: str, is_admin: bool):
    with SessionLocal() as session:
        query = insert(User).values(
        user_id=user_id,
        user_name=user_name,
        is_admin=is_admin)
        result = session.execute(query)
        session.commit()
        return True if result.rowcount>0 else False
    


