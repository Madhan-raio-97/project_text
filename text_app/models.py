from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    modified_at = models.DateTimeField('Modified at', auto_now=True)

    class Meta:
        abstract = True


class tag(BaseModel):
    title = models.CharField('tags', max_length=255, unique=True)

    def tag_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'created at': self.created_at,
            'last modified': self.modified_at
        }

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tag'


class text(BaseModel):
    tag = models.ForeignKey(tag, on_delete=models.CASCADE, related_name='texts')
    text = models.TextField('short text')

    def text_list(self):
        return {
            'id': self.id,
            'tags': self.tag.title,
            'text': self.text,
            'created at': self.created_at,
            'last modified': self.modified_at
        }

    def __str__(self):
        return self.tag.title + " : " + self.text

    class Meta:
        db_table = 'text'