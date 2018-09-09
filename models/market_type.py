from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, \
    BooleanAttribute


class MarketType(Model):
    """
    A market type
    """
    class Meta:
        table_name = 'market_types'

    external_id = NumberAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    market_group_id = NumberAttribute()
    volume = NumberAttribute()
    packaged_volume = NumberAttribute()
    published = BooleanAttribute()
