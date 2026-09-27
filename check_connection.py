from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg2://postgres:5636@localhost:5433/EatTime"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())