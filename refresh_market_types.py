from json import JSONDecodeError
from time import sleep

import requests
from pynamodb.exceptions import QueryError, PutError, VerboseClientError

from constants import DEFAULT_PARAMS, MARKET_GROUPS_URI, MARKET_TYPES_URI
from models.market_group import MarketGroup
from models.market_type import MarketType
from utility import get_logger

log = get_logger()

MarketGroup.create_table(read_capacity_units=1, write_capacity_units=1)
MarketType.create_table(read_capacity_units=1, write_capacity_units=1)

market_groups_response = requests.get(MARKET_GROUPS_URI, params=DEFAULT_PARAMS)
market_group_ids = market_groups_response.json()

for market_group_id in market_group_ids:
    market_group_exists = False
    try:
        market_group_exists = MarketGroup.count(market_group_id) != 0
    except (QueryError, KeyError) as e:
        pass

    market_group_uri = MARKET_GROUPS_URI + str(market_group_id) + '/'

    try:
        market_group_details = requests.get(market_group_uri, params=DEFAULT_PARAMS).json()
    except JSONDecodeError as e:
        pass

    mg = MarketGroup()
    mg.external_id = market_group_id
    mg.name = market_group_details['name']
    if 'parent_group_id' in market_group_details:
        mg.parent_group_id = market_group_details['parent_group_id']

    for type_id in market_group_details['types']:
        while True:
            try:
                exists = MarketType.count(type_id) > 0
                break
            except (QueryError, VerboseClientError):
                log.info('Sleeping')
                sleep(5)

        if exists:
            log.info(f'id {type_id} already exists, skipping')
            continue

        market_type_uri = MARKET_TYPES_URI + str(type_id) + '/'

        market_type_details = requests.get(market_type_uri, params=DEFAULT_PARAMS).json()
        type = MarketType()
        type.external_id = type_id
        type.name = market_type_details['name']
        type.description = market_type_details.get('description', 'No description')
        type.packaged_volume = market_type_details['packaged_volume']
        type.volume = market_type_details['volume']
        type.published = market_type_details['published']
        type.market_group_id = market_type_details['market_group_id']
        try:
            type.save()
            log.info(f'Added market type "{type.name}" with id {str(type_id)}')
        except (PutError, VerboseClientError):
            sleep(5)
            type.save()