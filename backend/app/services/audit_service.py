from app.models.audit_model import AuditLog

def create_log(
    db,
    #user_id,
    action
):
    log = AuditLog(
        #user_id=user_id,
        action=action
    )

    db.add(log)
    db.commit()

    return log