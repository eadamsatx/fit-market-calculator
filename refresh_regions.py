import requests

from models.region import Region
from utility import get_logger
from constants import *

log = get_logger()

regions_response = requests.get(REGIONS_URI, params=DEFAULT_PARAMS)

Region.create_table(read_capacity_units=1, write_capacity_units=1)

DRY_RUN = True

for region_id in regions_response.json():
    region_exists = Region.count(region_id) != 0

    if DRY_RUN or (not region_exists):
        region_id_uri = REGIONS_URI + str(region_id) + '/'
        region_details_response = requests.get(
            region_id_uri, params=DEFAULT_PARAMS)

        region = Region()
        region.external_id = region_id
        region.name = region_details_response.json()['name']

        if not DRY_RUN:
            region.save()

        log.info(f'Added region {region.name} with id {region.external_id}')

    else:
        log.info(f'Region {region_id} already exists, skipping')