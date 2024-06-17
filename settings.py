from os import environ

SESSION_CONFIGS = [
    dict(
        name='opinions_questionnaire',
        app_sequence=['opinions_questionnaire'],
        num_demo_participants=100,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

ROOMS = [
    dict(
        name='Session12EXP12Zafiro',
        display_name='Session12_EXP12Zafiro',
    ),
    dict(
        name='Session14EXP12Zafiro',
        display_name='Session14_EXP12Zafiro',
    ),
    dict(
        name='Session13EXP12Zafiro',
        display_name='Session13_EXP12Zafiro',
    ),
]

PARTICIPANT_FIELDS = ['paypal']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3441516710499'
