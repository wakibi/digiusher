CLOUD_PROVIDERS = ('aws', 'azure', 'gcp')
AWS_BASE_URL = 'https://pricing.us-east-1.amazonaws.com'
AWS_SERVICE_INDEX_FILE = f'{AWS_BASE_URL}/offers/v1.0/aws/index.json'
AWS_OFFER_CODES_TO_RUN = ['AmazonEC2']
AWS_CPU_CLOCK_SPEED_UNITS = 'GHz'
AWS_MEMORY_UNITS = 'GiB'
AWS_REGION_CODE_TO_REGION_MAPPING = {
    'us-east-2': 'US', 'us-east-1': 'US', 'us-west-1': 'US', 'us-west-2': 'US', 'af-south-1': 'Africa', 
    'ap-east-1': 'Asia Pacific', 'ap-south-2': 'Asia Pacific', 'ap-southeast-3': 'Asia Pacific', 
    'ap-southeast-5': 'Asia Pacific', 'ap-southeast-4': 'Asia Pacific', 'ap-south-1': 'Asia Pacific', 
    'ap-northeast-3': 'Asia Pacific', 'ap-northeast-2': 'Asia Pacific', 'ap-southeast-1': 'Asia Pacific', 
    'ap-southeast-2 ': 'Asia Pacific', 'ap-northeast-1': 'Asia Pacific', 'ca-central-1': 'Canada', 
    'ca-west-1': 'Canada', 'eu-central-1': 'Europe', 'eu-west-1': 'Europe', 'eu-west-2': 'Europe', 
    'eu-south-1': 'Europe', 'eu-west-3': 'Europe', 'eu-south-2': 'Europe', 'eu-north-1': 'Europe', 
    'eu-central-2': 'Europe', 'il-central-1': 'Israel', 'me-south-1': 'Middle East', 'me-central-1': 'Middle East', 
    'sa-east-1': 'South America', 'us-gov-east-1': 'AWS GovCloud', 'us-gov-west-1': 'AWS GovCloud'
}
