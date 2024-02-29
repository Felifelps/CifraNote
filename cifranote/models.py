import peewee as pw

db = pw.SqliteDatabase('data.db')

class ModelBase(pw.Model):
    class Meta:
        database = db

class Note(ModelBase):
    title = pw.CharField(max_length=40, unique=True)
    text = pw.TextField()

    def __str__(self) -> str:
        return f'<Note title={self.title}>'


db.connect()

db.create_tables([Note], safe=True)
