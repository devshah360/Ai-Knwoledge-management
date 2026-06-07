from sqlalchemy import create_engine

MSSQL_URL = (
    "mssql+pymssql://"
    "sa:password@localhost/source_db"
)

engine = create_engine(
    MSSQL_URL
)