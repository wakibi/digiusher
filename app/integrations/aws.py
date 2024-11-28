from contextlib import closing
from datetime import datetime
from itertools import islice
import codecs
import csv
import re

import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import null

from app.db import db
from app.models import CloudPriceData
from .constants import AWS_BASE_URL, AWS_OFFER_CODES_TO_RUN, AWS_SERVICE_INDEX_FILE, AWS_REGION_CODE_TO_REGION_MAPPING


regex = re.compile(r"\d*\.*\d+")

def getFloatOrNull(value):
    matched = regex.findall(value)
    if matched:
      return matched[0]
    return null()
    
def download_aws_data(url):
    with requests.get(url) as response:
        return response.json()

def persist_aws_data_using_csv(region_code, url):
    # Replace .json with .csv to get csv file
    url = url.replace('.json', '.csv')
    with closing(requests.get(url, stream=True)) as response:
        aws_reader = csv.reader(codecs.iterdecode(response.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
        publication_date_index = 2
        publication_date_row = next(islice(aws_reader, publication_date_index, None))
        publication_date = datetime.strptime(publication_date_row[1], '%Y-%m-%dT%H:%M:%S%z')
        offer_code_index_after_date = 1
        offer_code_row = next(islice(aws_reader, offer_code_index_after_date, None))
        offer_code = offer_code_row[1]
        # Skip row with column headings
        next(aws_reader)
        
        aws_price_data = []
        min_price = float(0)
        # Assign region here since we are running region by region, so should be same for all items in our file
        region = AWS_REGION_CODE_TO_REGION_MAPPING[region_code]
        
        for counter, row in enumerate(aws_reader):
            price_per_unit = float(row[9])
            # Ignore items with prices = 0
            if price_per_unit <= min_price:
                continue
            rate_code = row[2]
            
            cpus = row[22] if len(row[22]) > 0 else null()
            clock_speed = getFloatOrNull(row[24])
            ram = getFloatOrNull(row[25])
            currency = row[10]
            unit = row[8]
            price_description = row[4]
            sku = row[0]
            instance_type = row[19]
            location = row[17]
            instance_family = row[21]
            aws_price_data.append(
                {
                'rate_code': rate_code, 'provider': 'aws', 'region_code': region_code, 'offer_code': offer_code, 
                'region': region, 'cpus': cpus, 'clock_speed': clock_speed, 'ram': ram, 'currency': currency, 'unit': unit,
                'price_per_unit': price_per_unit, 'price_description': price_description, 'sku': sku, 'instance_type': instance_type, 
                'location': location, 'instance_family': instance_family, 'publication_date': publication_date 
                }
            )
            
            # Limit to 2500 insertions max at a time
            # You may want to reduce this number if you get timeouts from the DB
            if counter%2500 == 0:
                stmt = insert(CloudPriceData).values(aws_price_data)
                stmt = stmt.on_conflict_do_update(
                    # Let's use the constraint name
                    constraint = "rate_code_region_code_unique",

                    # The columns that should be updated on conflict
                    set_={
                        'price_per_unit': price_per_unit,
                        'currency': currency,
                    }
                )
                db.session.execute(stmt)
                aws_price_data.clear()
        db.session.commit()
    
def import_aws_data():
    """ 
    https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json - Service index file
    https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json -  Full file
    Base URL - https://pricing.us-east-1.amazonaws.com
    https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/region_index.json - by region
    """
    # Get service index data
    service_index_data = download_aws_data(AWS_SERVICE_INDEX_FILE)
    
    region_index_urls = [
        offer['currentRegionIndexUrl'] for offer_code, offer in service_index_data['offers'].items() if offer_code in AWS_OFFER_CODES_TO_RUN
        ]
    # Get region index data
    full_region_index_url = '{base_url}{uri}'
    service_price_list_url = '{base_url}{uri}'
    for region_index_url in region_index_urls:
        region_index_data = download_aws_data(full_region_index_url.format(base_url=AWS_BASE_URL, uri=region_index_url))
        # Download service price list files and process them
        # Test using eu-west-1, after testing we remove the continue block
        for region_code, details in region_index_data['regions'].items():
            if region_code != 'eu-west-1':
                continue
            current_region_index_url = details['currentVersionUrl']
            persist_aws_data_using_csv(region_code, service_price_list_url.format(base_url=AWS_BASE_URL, uri=current_region_index_url))
