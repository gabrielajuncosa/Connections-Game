from os import environ

SESSION_CONFIGS = [
    dict(
        name='Inactives12',
        app_sequence=['inactives_S12'],
        num_demo_participants=6,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['paypal', 'nickname', 'active', 'timeoutCounter', 'connections', 'connections_INIT',
                      'followers', 'followers_INIT', 'i_follow', 'i_follow_INIT', 'i_dont_follow', 'i_dont_follow_INIT',
                      'messages', 'messages_INIT', 'clicks', 'cumm_payoff',
                      ]

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True


ROOMS = [
    dict(
        name='Session10_EXP12Zafiro',
        display_name='Sesión 10 EXP12-Zafiro 29 Noviembre 2023',
    ),
    dict(
        name='Session11_EXP12Zafiro',
        display_name='Sesión 11 EXP12-Zafiro 29 Noviembre 2023',
    ),
    dict(
        name='Session15_EXP12Zafiro',
        display_name='Sesión 15 EXP12-Zafiro 29 Noviembre 2023',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9236122600724'
