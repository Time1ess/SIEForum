"""
Django settings for SIEForum project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Define placeholder gettext function
# This function will mark strings in settings visible to makemessages
# without need for Django's i18n features be initialized first.
_ = lambda x: x


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l7gwqw)_0ek12i*h(i8x8sn^5_2@q0_b*#mfu4h+9r_#2267cv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# A list of strings representing the host/domain names that this Django site can serve.
# If you are unsure, just enter here your domain name, eg. ['mysite.com', 'www.mysite.com']

ALLOWED_HOSTS = ['192.168.3.95', '192.168.20.100',
                 '202.118.67.200', '127.0.0.1']


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # Misago requires PostgreSQL to run
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Caching
# https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache

CACHES = {
    'default': {
        # Misago doesn't run well with LocMemCache in production environments
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['username', 'email'],
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# User uploads (Avatars, Attachments, files uploaded in other Django apps, ect.)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

MEDIA_URL = '/media/'


# The absolute path to the directory where collectstatic will collect static files for deployment.
# https://docs.djangoproject.com/en/1.11/ref/settings/#static-root

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Absolute filesystem path to the directory that will hold user-uploaded files.
# https://docs.djangoproject.com/en/1.11/ref/settings/#media-root

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder
# is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
# https://docs.djangoproject.com/en/1.10/ref/settings/#staticfiles-dirs

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'theme', 'static'),
]


# Application definition

AUTH_USER_MODEL = 'misago_users.User'

AUTHENTICATION_BACKENDS = [
    'misago.users.authbackends.MisagoBackend',
]

CSRF_FAILURE_VIEW = 'misago.core.errorpages.csrf_failure'

INSTALLED_APPS = [
    # Misago overrides for Django core feature
    'misago',
    'misago.users',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps used by Misago
    'debug_toolbar',
    'crispy_forms',
    'mptt',
    'rest_framework',

    # Misago apps
    'misago.admin',
    'misago.acl',
    'misago.core',
    'misago.conf',
    'misago.markup',
    'misago.legal',
    'misago.categories',
    'misago.threads',
    'misago.readtracker',
    'misago.search',
    'misago.faker',

    # Custom apps
    'student',
    'onlinejudge',
]

INTERNAL_IPS = [
    '127.0.0.1'
]

LOGIN_REDIRECT_URL = 'misago:index'

LOGIN_URL = 'misago:login'

LOGOUT_URL = 'misago:logout'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'misago.users.middleware.RealIPMiddleware',
    'misago.core.middleware.frontendcontext.FrontendContextMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'misago.users.middleware.UserMiddleware',
    'misago.core.middleware.exceptionhandler.ExceptionHandlerMiddleware',
    'misago.users.middleware.OnlineTrackerMiddleware',
    'misago.admin.middleware.AdminAuthMiddleware',
    'misago.threads.middleware.UnreadThreadsCountMiddleware',
    'misago.core.middleware.threadstore.ThreadStoreMiddleware',
]

ROOT_URLCONF = 'SIEForum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'theme', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'misago.core.context_processors.site_address',
                'misago.core.context_processors.momentjs_locale',
                'misago.conf.context_processors.settings',
                'misago.search.context_processors.search_providers',
                'misago.users.context_processors.user_links',
                'misago.legal.context_processors.legal_links',
                'onlinejudge.context_processors.oj_links',

                # Data preloaders
                'misago.conf.context_processors.preload_settings_json',
                'misago.core.context_processors.current_link',
                'misago.markup.context_processors.preload_api_url',
                'misago.threads.context_processors.preload_threads_urls',
                'misago.users.context_processors.preload_user_json',

                # Note: keep frontend_context processor last for previous processors
                # to be able to expose data UI app via request.frontend_context
                'misago.core.context_processors.frontend_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'SIEForum.wsgi.application'

# Django Crispy Forms
# http://django-crispy-forms.readthedocs.io/en/latest/install.html

CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',

    'misago.acl.panels.MisagoACLPanel',

    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
]


# Django Rest Framework
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'misago.core.rest_permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'misago.core.exceptionhandler.handle_api_exception',
    'UNAUTHENTICATED_USER': 'misago.users.models.AnonymousUser',
    'URL_FORMAT_OVERRIDE': None,
}


# Misago specific settings
# https://misago.readthedocs.io/en/latest/developers/settings.html

# PostgreSQL text search configuration to use in searches
# Defaults to "simple", for list of installed configurations run "\dF" in "psql"
# Standard configs as of PostgreSQL 9.5 are: dutch, english, finnish, french,
# german, hungarian, italian, norwegian, portuguese, romanian, russian, simple,
# spanish, swedish and turkish
# Example on adding custom language can be found here: https://github.com/lemonskyjwt/plpstgrssearch

MISAGO_SEARCH_CONFIG = 'simple'


# Path to directory containing avatar galleries
# Those galleries can be loaded by running loadavatargallery command

MISAGO_AVATAR_GALLERY = os.path.join(BASE_DIR, 'avatargallery')


# Profile fields

MISAGO_PROFILE_FIELDS = [
    {
        'name': _("Personal"),
        'fields': [
            'student.profilefields.student.StudentIDField',
            'misago.users.profilefields.default.FullNameField',
            'misago.users.profilefields.default.GenderField',
            'misago.users.profilefields.default.BioField',
            'misago.users.profilefields.default.LocationField',
        ],
    },
    {
        'name': _("Contact"),
        'fields': [
            'misago.users.profilefields.default.WebsiteField',
        ],
    },
    {
        'name': _("IP address"),
        'fields': [
            'misago.users.profilefields.default.JoinIpField',
            'misago.users.profilefields.default.LastIpField',
        ],
    },
]

# Admin
MISAGO_ADMIN_PATH = 'sie-admin'

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

MISAGO_USE_STOP_FORUM_SPAM = True

MISAGO_POSTING_MIDDLEWARES = [
    # Always keep FloodProtectionMiddleware middleware first one
    'misago.threads.api.postingendpoint.floodprotection.FloodProtectionMiddleware',

    'misago.threads.api.postingendpoint.category.CategoryMiddleware',
    'misago.threads.api.postingendpoint.privatethread.PrivateThreadMiddleware',
    'misago.threads.api.postingendpoint.reply.ReplyMiddleware',
    'misago.threads.api.postingendpoint.moderationqueue.ModerationQueueMiddleware',
    'misago.threads.api.postingendpoint.attachments.AttachmentsMiddleware',
    'misago.threads.api.postingendpoint.participants.ParticipantsMiddleware',
    'misago.threads.api.postingendpoint.pin.PinMiddleware',
    'misago.threads.api.postingendpoint.close.CloseMiddleware',
    'misago.threads.api.postingendpoint.hide.HideMiddleware',
    'misago.threads.api.postingendpoint.protect.ProtectMiddleware',
    'misago.threads.api.postingendpoint.recordedit.RecordEditMiddleware',
    'misago.threads.api.postingendpoint.updatestats.UpdateStatsMiddleware',
    'misago.threads.api.postingendpoint.mentions.MentionsMiddleware',
    'misago.threads.api.postingendpoint.subscribe.SubscribeMiddleware',
    'misago.threads.api.postingendpoint.syncprivatethreads.SyncPrivateThreadsMiddleware',

    'onlinejudge.middleware.OJSubmissionMiddleware',
    'onlinejudge.middleware.OJReleaseMiddleware',
    # Always keep SaveChangesMiddleware middleware after all state-changing middlewares
    'misago.threads.api.postingendpoint.savechanges.SaveChangesMiddleware',

    # Those middlewares are last because they don't change app state
    'misago.threads.api.postingendpoint.emailnotification.EmailNotificationMiddleware',

]

# Celery settings
CELERY_BROKER_URL = 'redis://redis:6379/0'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TASK_SERIALIZER = 'json'
