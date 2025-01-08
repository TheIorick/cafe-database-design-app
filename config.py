class AppConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/vsu_3_curs_cafe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'