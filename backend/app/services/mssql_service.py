from sqlalchemy import text

from app.database import engine
def fetch_documents():

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    id,
                    title,
                    content,
                    updated_at
                FROM documents
                """
            )
        )

        return [
            dict(row._mapping)
            for row in result
        ]