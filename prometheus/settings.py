from dotenv import load_dotenv
from omniconf import omniconf_load, setting

def load_config():
    load_dotenv()
    setting('fuga.exporter.redis')
    setting('fuga.exporter.prometheus')
    omniconf_load()
