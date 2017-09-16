
from frontera.settings.default_settings import MIDDLEWARES

BACKEND = 'frontera.contrib.backends.sqlalchemy.revisiting.Backend'
SQLALCHEMYBACKEND_ENGINE = 'sqlite:///olx_frontier_v2.db'
SQLALCHEMYBACKEND_ENGINE_ECHO = False
SQLALCHEMYBACKEND_DROP_ALL_TABLES = False
SQLALCHEMYBACKEND_CLEAR_CONTENT = False
from datetime import timedelta
SQLALCHEMYBACKEND_REVISIT_INTERVAL = timedelta(days=1)

DELAY_ON_EMPTY = 20.0
MAX_NEXT_REQUESTS = 256

# MIDDLEWARES.extend([
#     'frontera.contrib.middlewares.domain.DomainMiddleware',
#     'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
# ])


