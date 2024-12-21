import configparser
from yaDisk import YaUpload


config = configparser.ConfigParser()
config.read("token.ini")
token = config["YaToken"]["YaToken"]
yandex = YaUpload(token)