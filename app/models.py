from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from currencies import Currency

from app.db import db
from .integrations.constants import AWS_MEMORY_UNITS

"""
    flask db init
    flask db migrate
    flask db upgrade
 """


class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class CloudPriceData(db.Model):
    __tablename__ = "cloud_price_data"

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    rate_code = mapped_column(db.String(100), nullable=False, unique=True)
    region_code = mapped_column(db.String(15), nullable=False)
    provider = mapped_column(db.String(10), nullable=False)
    offer_code = mapped_column(db.String(30), nullable=False)
    region = mapped_column(db.String(30), nullable=True)
    cpus = mapped_column(db.Integer, nullable=True)
    clock_speed = mapped_column(db.DECIMAL(5, 3), nullable=True)
    ram = mapped_column(db.DECIMAL(8, 2), nullable=True)
    currency = mapped_column(db.String(5), nullable=False)
    unit = mapped_column(db.String(30), nullable=False)
    price_per_unit = mapped_column(db.DECIMAL(20, 10), nullable=False)
    price_description = mapped_column(db.String(200), nullable=False)
    sku = mapped_column(db.String(30), nullable=False)
    instance_type = mapped_column(db.String(30), nullable=True)
    location = mapped_column(db.String(30), nullable=True)
    instance_family = mapped_column(db.String(50), nullable=True)
    publication_date = mapped_column(db.DateTime(timezone=True), nullable=False)
    created_at = mapped_column(db.DateTime(timezone=True), server_default=UtcNow())
    updated_at = mapped_column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (db.UniqueConstraint("rate_code", "region_code", name="rate_code_region_code_unique"),)

    def register_cloud_price_if_not_exist(self):
        db_cloud_price = CloudPriceData.query.filter(CloudPriceData.rate_code == self.rate_code).all()
        if not db_cloud_price:
            db.session.add(self)
            db.session.commit()

        return True

    def get_by_rate_code(self, rate_code):
        db_cloud_price = CloudPriceData.query.filter(CloudPriceData.rate_code == rate_code).first()
        return db_cloud_price

    def to_json(self):
        return {
            "cpu": self.cpus,
            "ram": f"{self.ram} {AWS_MEMORY_UNITS}",
            "description": str(self),
        }

    def __str__(self):
        currency = Currency(self.currency)
        price = currency.get_money_format(float(self.price_per_unit))
        return f"{self.instance_type} / {self.location} {self.instance_family} {price} per {self.unit}"
