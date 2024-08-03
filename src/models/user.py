from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute


class UserModel(Model):
  class Meta:
    table_name = 'animind_Users'
    region = 'us-east-1'
    
  id = NumberAttribute()
  email = UnicodeAttribute(hash_key=True)
  name = UnicodeAttribute()
  age = NumberAttribute()
  gender = UnicodeAttribute()
  psychological_state = UnicodeAttribute()