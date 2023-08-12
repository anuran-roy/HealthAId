from dotenv import load_dotenv
from playhouse.postgres_ext import PostgresqlExtDatabase
from python.config import settings
import os

load_dotenv(str(settings.BASE_DIR / ".env"))
# Replace 'your_database_name', 'your_username', and 'your_password' with actual values
# db = PostgresqlDatabase(
#     'neondb', user='anuran-roy', password='UXTnG6Vm3RsC', host='ep-shy-sun-750855.us-west-2.aws.neon.tech', port=5432)

db = PostgresqlExtDatabase(
    os.getenv("PG_NAME", "postgres"),
    user=os.getenv("PG_USERNAME", "postgres"),
    password=os.getenv("PG_PASSWORD", "postgres"),
    host=os.getenv("PG_HOST", "localhost"),
    port=int(os.getenv("PG_PORT", 5432)),
)
