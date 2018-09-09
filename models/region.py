from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class Region(Model):
    """
    A region
    """
    class Meta:
        table_name = 'regions'

    external_id = NumberAttribute(hash_key=True)
    name = UnicodeAttribute()