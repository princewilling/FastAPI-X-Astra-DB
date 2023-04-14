from datetime import datetime
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from config import get_settings

settings = get_settings()
  
class Post(Model):
    __keyspace__ = settings.keyspace
    post_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    title = columns.Text()
    body = columns.Text()
    created_at = columns.DateTime(primary_key=True, default=datetime.utcnow())
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) ->  str:
        return f"Post(title={self.title})"