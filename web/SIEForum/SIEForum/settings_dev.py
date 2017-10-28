from .settings_production import *


DEBUG = True
AUTH_PASSWORD_VALIDATORS = []
SECRET_KEY = 'l7gwqw)_0ek12i*h(i8x8sn^5_2@q0_b*#mfu4h+9r_1345678'

# Email configuration
# https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend

EMAIL_HOST = 'smtp.163.com'
# EMAIL_PORT = 25
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_HOST_USER = 'DUT_SIE@163.com'
EMAIL_HOST_PASSWORD = 'D86hrxEYUc4'
EMAIL_SUBJECT_PREFIX = '[DUT-SIE论坛]'
EMAIL_USE_TLS = True

# Default email address to use for various automated correspondence from the site manager(s).

DEFAULT_FROM_EMAIL = 'Forums <%s>' % EMAIL_HOST_USER
