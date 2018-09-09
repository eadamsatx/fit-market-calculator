from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class MarketGroup(Model):
    """
    A region
    """
    class Meta:
        table_name = 'market_groups'

    external_id = NumberAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    parent_group_id = NumberAttribute()
