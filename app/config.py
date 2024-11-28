class PostgreSQLConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://digiusher_db:digiusher_db@db:5432/digiusher_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False