import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "pennapps_f15.settings.development")

from django.core.wsgi import get_wsgi_application
from pennapps_f15.settings.production import HEROKU

if HEROKU:
  from dj_static import Cling
  application = Cling(get_wsgi_application())
else:
  application = get_wsgi_application()

