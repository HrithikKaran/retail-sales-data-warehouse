from sqlalchemy import create_engine, text
from config.db_config import DB_CONFIG

connection_string = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(connection_string)

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print("Connected to database:", result.scalar())