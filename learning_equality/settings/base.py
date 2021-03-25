"""
Django settings for learning_equality project.
"""
import os
import sys

import dj_database_url

env = os.environ.copy()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Switch off DEBUG mode explicitly in the base settings.
# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = False


# Secret key is important to be kept secret. Never share it with anyone. Please
# always set it in the environment variable and never check into the
# repository.
# In its default template Django generates a 50-characters long string using
# the following function:
# https://github.com/django/django/blob/fd8a7a5313f5e223212085b2e470e43c0047e066/django/core/management/utils.py#L76-L81
# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
if "SECRET_KEY" in env:
    SECRET_KEY = env["SECRET_KEY"]


# Define what hosts an app can be accessed by.
# It will return HTTP 400 Bad Request error if your host is not set using this
# setting.
# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
if "ALLOWED_HOSTS" in env:
    ALLOWED_HOSTS = env["ALLOWED_HOSTS"].split(",")


# Application definition

INSTALLED_APPS = [
    # This is an app that we use for the performance monitoring.
    # You set configure it by setting the following environment variables:
    #  * SCOUT_MONITOR="True"
    #  * SCOUT_KEY="paste api key here"
    #  * SCOUT_NAME="learning_equality"
    # https://intranet.torchbox.com/delivering-projects/tech/scoutapp/
    # According to the official docs, it's important that Scout is listed
    # first - http://help.apm.scoutapp.com/#django.
    "scout_apm.django",
    "learning_equality.documents",
    "learning_equality.forms",
    "learning_equality.home",
    "learning_equality.images",
    "learning_equality.navigation",
    "learning_equality.news",
    "learning_equality.people",
    "learning_equality.search",
    "learning_equality.standardpages",
    "learning_equality.users",
    "learning_equality.utils",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.postgres_search",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.legacy.richtext",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
    "captcha",
    "wagtailcaptcha",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Must be before `django.contrib.staticfiles`
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "pattern_library",
    "learning_equality.project_styleguide.apps.ProjectStyleguideConfig",
    "wagtailaccessibility",
]


# Middleware classes
# https://docs.djangoproject.com/en/stable/ref/settings/#middleware
# https://docs.djangoproject.com/en/stable/topics/http/middleware/
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise middleware is used to server static files (CSS, JS, etc.).
    # According to the official documentation it should be listed underneath
    # SecurityMiddleware.
    # http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "learning_equality.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                # This is a custom context processor that lets us add custom
                # global variables to all the templates.
                "learning_equality.utils.context_processors.global_vars",
            ],
            "builtins": ["pattern_library.loader_tags"],
        },
    }
]

WSGI_APPLICATION = "learning_equality.wsgi.application"


# Database
# This setting will use DATABASE_URL environment variable.
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# https://github.com/kennethreitz/dj-database-url

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600, default="postgres:///learning_equality"
    )
}


# Server-side cache settings. Do not confuse with front-end cache.
# https://docs.djangoproject.com/en/stable/topics/cache/
# If the server has a Redis instance exposed via a URL string in the REDIS_URL
# environment variable, prefer that. Otherwise use the database backend. We
# usually use Redis in production and database backend on staging and dev. In
# order to use database cache backend you need to run
# "django-admin createcachetable" to create a table for the cache.
#
# On platforms like Heroku which automatically set the REDIS_URL environment
# variable, the value is usually set to not use TLS.
# Setting the `REDIS_FORCE_TLS` environment variable to True will replace redis://
# in the connection string with rediss://, enabling connectionst to redis over TLS.
#
# Do not use the same Redis instance for other things like Celery!
if "REDIS_URL" in env:
    REDIS_FORCE_TLS = env.get("REDIS_FORCE_TLS", "false").lower() == "true"
    REDIS_URL = env["REDIS_URL"]
    if REDIS_FORCE_TLS:
        REDIS_URL = REDIS_URL.replace("redis://", "rediss://")

    CACHES = {
        "default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL}
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "database_cache",
        }
    }

# Search
# https://docs.wagtail.io/en/latest/topics/search/backends.html

WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.contrib.postgres_search.backend"}
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

# We serve static files with Whitenoise (set in MIDDLEWARE). It also comes with
# a custom backend for the static files storage. It makes files cacheable
# (cache-control headers) for a long time and adds hashes to the file names,
# e.g. main.css -> main.1jasdiu12.css.
# The static files with this backend are generated when you run
# "django-admin collectstatic".
# http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps
# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Place static files that need a specific URL (such as robots.txt and favicon.ico) in the "public" folder
WHITENOISE_ROOT = os.path.join(BASE_DIR, "public")


# This is where Django will look for static files outside the directories of
# applications which are used by default.
# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [
    # "static_compiled" is a folder used by the front-end tooling
    # to output compiled static assets.
    os.path.join(PROJECT_DIR, "static_compiled")
]


# This is where Django will put files collected from application directories
# and custom direcotires set in "STATICFILES_DIRS" when
# using "django-admin collectstatic" command.
# https://docs.djangoproject.com/en/stable/ref/settings/#static-root
STATIC_ROOT = env.get("STATIC_DIR", os.path.join(BASE_DIR, "static"))


# This is the URL that will be used when serving static files, e.g.
# https://llamasavers.com/static/
# https://docs.djangoproject.com/en/stable/ref/settings/#static-url
STATIC_URL = env.get("STATIC_URL", "/static/")


# Where in the filesystem the media (user uploaded) content is stored.
# MEDIA_ROOT is not used when S3 backend is set up.
# Probably only relevant to the local development.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-root
MEDIA_ROOT = env.get("MEDIA_DIR", os.path.join(BASE_DIR, "media"))


# The URL path that media files will be accessible at. This setting won't be
# used if S3 backend is set up.
# Probably only relevant to the local development.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-url
MEDIA_URL = env.get("MEDIA_URL", "/media/")

# AWS S3 buckets configuration
# This is media files storage backend configuration. S3 is our preferred file
# storage solution.
# To enable this storage backend we use django-storages package...
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
# ...that uses AWS' boto3 library.
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
#
# Three required environment variables are:
#  * AWS_STORAGE_BUCKET_NAME
#  * AWS_ACCESS_KEY_ID
#  * AWS_SECRET_ACCESS_KEY
# The last two are picked up by boto3:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variables
if "AWS_STORAGE_BUCKET_NAME" in env:
    # Add django-storages to the installed apps
    INSTALLED_APPS = INSTALLED_APPS + ["storages", "wagtail_storages"]

    # https://docs.djangoproject.com/en/stable/ref/settings/#default-file-storage
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_STORAGE_BUCKET_NAME = env["AWS_STORAGE_BUCKET_NAME"]

    # Disables signing of the S3 objects' URLs. When set to True it
    # will append authorization querystring to each URL.
    AWS_QUERYSTRING_AUTH = False

    # Do not allow overriding files on S3 as per Wagtail docs recommendation:
    # https://docs.wagtail.io/en/stable/advanced_topics/deploying.html#cloud-storage
    # Not having this setting may have consequences in losing files.
    AWS_S3_FILE_OVERWRITE = False

    # Default ACL for new files should be "private" - not accessible to the
    # public. Images should be made available to public via the bucket policy,
    # where the documents should use wagtail-storages.
    AWS_DEFAULT_ACL = "private"

    # We generally use this setting in the production to put the S3 bucket
    # behind a CDN using a custom domain, e.g. media.llamasavers.com.
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
    if "AWS_S3_CUSTOM_DOMAIN" in env:
        AWS_S3_CUSTOM_DOMAIN = env["AWS_S3_CUSTOM_DOMAIN"]

    # When signing URLs is facilitated, the region must be set, because the
    # global S3 endpoint does not seem to support that. Set this only if
    # necessary.
    if "AWS_S3_REGION_NAME" in env:
        AWS_S3_REGION_NAME = env["AWS_S3_REGION_NAME"]

    # This settings lets you force using http or https protocol when generating
    # the URLs to the files. Set https as default.
    # https://github.com/jschneier/django-storages/blob/10d1929de5e0318dbd63d715db4bebc9a42257b5/storages/backends/s3boto3.py#L217
    AWS_S3_URL_PROTOCOL = env.get("AWS_S3_URL_PROTOCOL", "https:")


# Logging
# This logging is configured to be used with Sentry and console logs. Console
# logs are widely used by platforms offering Docker deployments, e.g. Heroku.
# We use Sentry to only send error logs so we're notified about errors that are
# not Python exceptions.
# We do not use default mail or file handlers because they are of no use for
# us.
# https://docs.djangoproject.com/en/stable/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Send logs with at least INFO level to the console.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "learning_equality": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}


# Email settings
# We use SMTP to send emails. We typically use transactional email services
# that let us use SMTP.
# https://docs.djangoproject.com/en/2.1/topics/email/

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host
if "EMAIL_HOST" in env:
    EMAIL_HOST = env["EMAIL_HOST"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-port
if "EMAIL_PORT" in env:
    try:
        EMAIL_PORT = int(env["EMAIL_PORT"])
    except ValueError:
        pass

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host-user
if "EMAIL_HOST_USER" in env:
    EMAIL_HOST_USER = env["EMAIL_HOST_USER"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host-password
if "EMAIL_HOST_PASSWORD" in env:
    EMAIL_HOST_PASSWORD = env["EMAIL_HOST_PASSWORD"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-use-tls
if env.get("EMAIL_USE_TLS", "false").lower().strip() == "true":
    EMAIL_USE_TLS = True

# https://docs.djangoproject.com/en/stable/ref/settings/#email-use-ssl
if env.get("EMAIL_USE_SSL", "false").lower().strip() == "true":
    EMAIL_USE_SSL = True

# https://docs.djangoproject.com/en/stable/ref/settings/#email-subject-prefix
if "EMAIL_SUBJECT_PREFIX" in env:
    EMAIL_SUBJECT_PREFIX = env["EMAIL_SUBJECT_PREFIX"]

# SERVER_EMAIL is used to send emails to administrators.
# https://docs.djangoproject.com/en/stable/ref/settings/#server-email
# DEFAULT_FROM_EMAIL is used as a default for any mail send from the website to
# the users.
# https://docs.djangoproject.com/en/stable/ref/settings/#default-from-email
if "SERVER_EMAIL" in env:
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = env["SERVER_EMAIL"]


# Sentry configuration.
# See instructions on the intranet:
# https://intranet.torchbox.com/delivering-projects/tech/starting-new-project/#sentry
is_in_shell = len(sys.argv) > 1 and sys.argv[1] in ["shell", "shell_plus"]

if "SENTRY_DSN" in env and not is_in_shell:

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.utils import get_default_release

    sentry_kwargs = {
        "dsn": env["SENTRY_DSN"],
        "integrations": [DjangoIntegration()],
    }

    # There's a chooser to toggle between environments at the top right corner on sentry.io
    # Values are typically 'staging' or 'production' but can be set to anything else if needed.
    # dokku config:set gosh SENTRY_ENVIRONMENT=staging
    # heroku config:set SENTRY_ENVIRONMENT=production
    if "SENTRY_ENVIRONMENT" in env:
        sentry_kwargs.update({"environment": env["SENTRY_ENVIRONMENT"]})

    release = get_default_release()
    if release is None:
        try:
            # But if it's not, we assume that the commit hash is available in
            # the GIT_REV environment variable. It's a default environment
            # variable used on Dokku:
            # http://dokku.viewdocs.io/dokku/deployment/methods/git/#configuring-the-git_rev-environment-variable
            release = env["GIT_REV"]
        except KeyError:
            try:
                # Assume this is a Heroku-hosted app with the "runtime-dyno-metadata" lab enabled
                release = env["HEROKU_RELEASE_VERSION"]
            except KeyError:
                # If there's no commit hash, we do not set a specific release.
                release = None

    sentry_kwargs.update({"release": release})
    sentry_sdk.init(**sentry_kwargs)


# Front-end cache
# This configuration is used to allow purging pages from cache when they are
# published.
# These settings are usually used only on the production sites.
# This is a configuration of the CDN/front-end cache that is used to cache the
# production websites.
# https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html
# The backend can be configured to use an account-wide API key, or an API token with
# restricted access.

if (
    "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env
    or "FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN" in env
):
    INSTALLED_APPS.append("wagtail.contrib.frontend_cache")
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "ZONEID": env["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }

    if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env:
        # To use an account-wide API key, set the following environment variables:
        #  * FRONTEND_CACHE_CLOUDFLARE_TOKEN
        #  * FRONTEND_CACHE_CLOUDFLARE_EMAIL
        #  * FRONTEND_CACHE_CLOUDFLARE_ZONEID
        # These can be obtained from a sysadmin.
        WAGTAILFRONTENDCACHE["default"].update(
            {
                "EMAIL": env["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
                "TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            }
        )

    else:
        # To use an API token with restricted access, set the following environment variables:
        #  * FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN
        #  * FRONTEND_CACHE_CLOUDFLARE_ZONEID
        WAGTAILFRONTENDCACHE["default"].update(
            {"BEARER_TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN"]}
        )

    # Set up front-end cache if the S3 uses custom domain. This assumes that
    # the same Cloudflare zone is used.
    if env.get("AWS_S3_CUSTOM_DOMAIN"):
        WAGTAIL_STORAGES_DOCUMENTS_FRONTENDCACHE = {
            "default": {
                "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
                "EMAIL": env["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
                "TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
                "ZONEID": env["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
            },
        }


# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py.
try:
    CACHE_CONTROL_S_MAXAGE = int(env.get("CACHE_CONTROL_S_MAXAGE", 600))
except ValueError:
    pass


# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py.
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    env.get("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)
)


# Required to get e.g. wagtail-sharing working on Heroku and probably many other platforms.
# https://docs.djangoproject.com/en/stable/ref/settings/#use-x-forwarded-port
USE_X_FORWARDED_PORT = env.get("USE_X_FORWARDED_PORT", "true").lower().strip() == "true"

# Security configuration
# This configuration is required to achieve good security rating.
# You can test it using https://securityheaders.com/
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security

# Enabling this doesn't have any benefits but will make it harder to make
# requests from javascript because the csrf cookie won't be easily accessible.
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-httponly
# CSRF_COOKIE_HTTPONLY = True

# Force HTTPS redirect (enabled by default!)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
if env.get("SECURE_SSL_REDIRECT", "true").strip().lower() == "true":
    SECURE_SSL_REDIRECT = True


# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# This is a setting setting HSTS header. This will enforce the visitors to use
# HTTPS for an amount of time specified in the header. Please make sure you
# consult with sysadmin before setting this.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
if "SECURE_HSTS_SECONDS" in env:
    SECURE_HSTS_SECONDS = int(env["SECURE_HSTS_SECONDS"])


# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
if env.get("SECURE_BROWSER_XSS_FILTER", "true").lower().strip() == "true":
    SECURE_BROWSER_XSS_FILTER = True


# https://docs.djangoproject.com/en/stable/ref/settings/#secure-content-type-nosniff
if env.get("SECURE_CONTENT_TYPE_NOSNIFF", "true").lower().strip() == "true":
    SECURE_CONTENT_TYPE_NOSNIFF = True


# Content Security policy settings
# http://django-csp.readthedocs.io/en/latest/configuration.html
if "CSP_DEFAULT_SRC" in env:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")

    # The “special” source values of 'self', 'unsafe-inline', 'unsafe-eval', and 'none' must be quoted!
    # e.g.: CSP_DEFAULT_SRC = "'self'" Without quotes they will not work as intended.

    CSP_DEFAULT_SRC = env.get("CSP_DEFAULT_SRC").split(",")
    if "CSP_SCRIPT_SRC" in env:
        CSP_SCRIPT_SRC = env.get("CSP_SCRIPT_SRC").split(",")
    if "CSP_STYLE_SRC" in env:
        CSP_STYLE_SRC = env.get("CSP_STYLE_SRC").split(",")
    if "CSP_IMG_SRC" in env:
        CSP_IMG_SRC = env.get("CSP_IMG_SRC").split(",")
    if "CSP_CONNECT_SRC" in env:
        CSP_CONNECT_SRC = env.get("CSP_CONNECT_SRC").split(",")
    if "CSP_FONT_SRC" in env:
        CSP_FONT_SRC = env.get("CSP_FONT_SRC").split(",")
    if "CSP_BASE_URI" in env:
        CSP_BASE_URI = env.get("CSP_BASE_URI").split(",")
    if "CSP_OBJECT_SRC" in env:
        CSP_OBJECT_SRC = env.get("CSP_OBJECT_SRC").split(",")


# Referrer-policy header settings.
# https://django-referrer-policy.readthedocs.io/en/1.0/

REFERRER_POLICY = env.get(
    "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
).strip()

# Recaptcha
# These settings are required for the captcha challange to work.
# https://github.com/springload/wagtail-django-recaptcha

if "RECAPTCHA_PUBLIC_KEY" in env and "RECAPTCHA_PRIVATE_KEY" in env:
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = env["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = env["RECAPTCHA_PRIVATE_KEY"]


# Basic authentication settings
# These are settings to configure the third-party library:
# https://gitlab.com/tmkn/django-basic-auth-ip-whitelist
if env.get("BASIC_AUTH_ENABLED", "false").lower().strip() == "true":
    # Insert basic auth as a first middleware to be checked first, before
    # anything else.
    MIDDLEWARE.insert(0, "baipw.middleware.BasicAuthIPWhitelistMiddleware")

    # This is the credentials users will have to use to access the site.
    BASIC_AUTH_LOGIN = env.get("BASIC_AUTH_LOGIN", "tbx")
    BASIC_AUTH_PASSWORD = env.get("BASIC_AUTH_PASSWORD", "tbx")

    # Wagtail requires Authorization header to be present for the previews
    BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER = True

    # This is the list of network IP addresses that are allowed in without
    # basic authentication check.
    BASIC_AUTH_WHITELISTED_IP_NETWORKS = [
        # Torchbox networks.
        # https://projects.torchbox.com/projects/sysadmin/notebook/IP%20addresses%20to%20whitelist
        "78.32.251.192/28",
        "89.197.53.244/30",
        "193.227.244.0/23",
        "2001:41c8:103::/48",
    ]

    # This is the list of hosts that website can be accessed without basic auth
    # check. This may be useful to e.g. white-list "llamasavers.com" but not
    # "llamasavers.production.torchbox.com".
    if "BASIC_AUTH_WHITELISTED_HTTP_HOSTS" in env:
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS = env[
            "BASIC_AUTH_WHITELISTED_HTTP_HOSTS"
        ].split(",")


# Django REST framework settings
# Change default settings that enable basic auth.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    )
}


AUTH_USER_MODEL = "users.User"

# Wagtail settings


# This name is displayed in the Wagtail admin.
WAGTAIL_SITE_NAME = "Learning Equality Website"


# This is used by Wagtail's email notifications for constructing absolute
# URLs. Please set to the domain that users will access the admin site.
if "PRIMARY_HOST" in env:
    BASE_URL = "https://{}".format(env["PRIMARY_HOST"])

# Custom image model
# https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html
WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

# Rich text settings to remove unneeded features
# We normally don't want editors to use the images
# in the rich text editor, for example.
# They should use the image stream block instead
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "h3",
                "h4",
                "ol",
                "ul",
                "link",
                "document-link",
            ]
        },
    }
}

# Custom document model
# https://docs.wagtail.io/en/stable/advanced_topics/documents/custom_document_model.html
WAGTAILDOCS_DOCUMENT_MODEL = "documents.CustomDocument"


# Document serve method - avoid serving files directly from the storage.
# https://docs.wagtail.io/en/stable/advanced_topics/settings.html#documents
WAGTAILDOCS_SERVE_METHOD = "serve_view"


PASSWORD_REQUIRED_TEMPLATE = "patterns/pages/wagtail/password_required.html"


# Default size of the pagination used on the front-end.
DEFAULT_PER_PAGE = 20


# Styleguide
PATTERN_LIBRARY_ENABLED = env.get("PATTERN_LIBRARY_ENABLED", "false").lower() == "true"
PATTERN_LIBRARY = {
    "SECTIONS": (
        ("atoms", ["patterns/atoms"]),
        ("molecules", ["patterns/molecules"]),
        ("pages", ["patterns/pages"]),
    ),
    "TEMPLATE_SUFFIX": ".html",
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
    "BASE_TEMPLATE_NAMES": ["patterns/base_page.html"],
}


# Google Tag Manager ID from env
GOOGLE_TAG_MANAGER_ID = env.get("GOOGLE_TAG_MANAGER_ID")


# Allows us to toggle search indexing via an environment variable.
SEO_NOINDEX = env.get("SEO_NOINDEX", "false").lower() == "true"

TESTING = "test" in sys.argv

# By default, Django uses a computationally difficult algorithm for passwords hashing.
# We don't need such a strong algorithm in tests, so use MD5
if TESTING:
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]
