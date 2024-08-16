from urllib.parse import quote


class Config:
    SECRET_KEY = '7265c9aa4297a05c0b7ded86bd2e76f98b244ef5699bfbf71cefd924a66081a9'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/nepa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '308664db6f669929beb8a7e873e2be12e60ea0e9e1b1ff8cef4c8affa35b9fc4'
    UPLOAD_FOLDER = 'uploads'
