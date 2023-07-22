from peewee import PostgresqlDatabase
from playhouse.postgres_ext import PostgresqlExtDatabase

# Replace 'your_database_name', 'your_username', and 'your_password' with actual values
# db = PostgresqlDatabase(
#     'neondb', user='anuran-roy', password='UXTnG6Vm3RsC', host='ep-shy-sun-750855.us-west-2.aws.neon.tech', port=5432)

db = PostgresqlExtDatabase(
    "postgres",
    user="postgres",
    password="UcUCfxl0E3CqrJm5",
    host="db.zmdrxrkyhvumdexwtexp.supabase.co",
    port=5432,
)
