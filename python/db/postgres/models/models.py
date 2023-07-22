from peewee import Model, CharField, TextField
from db.postgres.db import db


class MayoClinicEntry(Model):
    Name = TextField(null=True, help_text="Condition Name")
    Overview = TextField(null=True, help_text="Condition Overview")
    Symptoms = TextField(null=True, help_text="Condition Symptoms")
    Causes = TextField(null=True, help_text="Condition Causes")
    Complications = TextField(null=True, help_text="Condition Complications")
    Prevention = TextField(null=True, help_text="Condition Prevention")
    Related = TextField(null=True, help_text="Condition Related")
    Risk_factors = TextField(null=True, help_text="Condition Risk Factors")
    Types = TextField(null=True, help_text="Condition Types")

    class Meta:
        database = db


db.create_tables([MayoClinicEntry])
