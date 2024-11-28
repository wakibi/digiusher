from flask import Blueprint, request

from app.db import db
from app.models import CloudPriceData
from app.utilities import removeNoneAndEmptyItems

bp = Blueprint("pages", __name__)

@bp.route("/api/get-prices", methods=['GET'])
def getPrices():
    cloud_type = request.args.get('cloud_type', None)
    location = request.args.get('location', None)
    number_of_cpus = request.args.get('number_of_cpus', None)
    ram = request.args.get('memory', None)
    query_params = { 'provider': cloud_type, 'region': location, 'cpus': number_of_cpus, 'ram': ram }
    query_params = removeNoneAndEmptyItems(query_params)
    print(query_params)
    if query_params:
        price_data = db.paginate(
            db.select(CloudPriceData).filter_by(**query_params).order_by(CloudPriceData.id)
        )
    else:
        price_data = db.paginate(db.select(CloudPriceData).order_by(CloudPriceData.ram))
    return [data.to_json() for data in price_data]
