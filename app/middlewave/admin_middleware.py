from fastapi import HTTPException

def required_admin(current_user):
        if current_user.role != "admin":
                raise HTTPException(
                        status_code=403,
                        detail="Admin only"
                )
        return current_user
