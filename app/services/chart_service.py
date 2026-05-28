from sqlalchemy import func
from app.models.document_model import Document

def document_upload_chart(db):
        results = db.query(func.date(Document.created_at),func.count(Document.id)).group_by(func.date(Document.created_at)).all()

        labels = []
        values = []

        for row in results:
                labels.append(str(row[0]))
                values.append(row[1])

        return {
                "chart_type":"line",
                "labels" : labels,
                "values":values
        }