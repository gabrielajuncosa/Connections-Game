from otree.api import *
import random
import numpy as np
import pandas as pd

doc = """
Your app description
"""


def open_CSV(filename):
    # filename = 'statementsPilot.csv'
    temp = pd.read_csv(filename, sep=';')
    # temp = list(temp['statement'])
    # csv = random.sample(temp, len(temp))
    csv = list(temp['statement'])
    return csv


class C(BaseConstants):
    NAME_IN_URL = 'opinions_questionnaire'
    PLAYERS_PER_GROUP = None
    TIMEOUT_Q = 60
    TIMEOUT_S = 600
    CSV = open_CSV('statementsPilotESP.csv')
    NUM_ROUNDS = len(open_CSV('statementsPilotESP.csv'))
    txt_importTU = "¿Qué importancia tiene este tema para ti?"
    CONSENTS_TEMPLATE = 'opinions_questionnaire/introTemplate.html'
    RESULTS_TEMPLATE = 'opinions_questionnaire/resultsTemplate.html'
    SCHEDULE_MONDAY = [
        dict(name='monday0930',
             label="9h30-10h45, hora Madrid"),
        dict(name='monday1000',
             label="10h00-11h15, hora Madrid"),
        dict(name='monday1030',
             label="10h30-11h45, hora Madrid"),
        dict(name='monday1100',
             label="11h00-12h15, hora Madrid"),
        dict(name='monday1130',
             label="11h30-12h45, hora Madrid"),
        dict(name='monday1200',
             label="12h00-13h15, hora Madrid"),
        dict(name='monday1230',
             label="12h30-13h45, hora Madrid"),
        dict(name='monday1300',
             label="13h00-14h15, hora Madrid"),
        dict(name='mondayNone', label="No estoy disponible en ninguno de los horarios anteriores.")
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    paypal = models.StringField(initial="", label="Ingresa el correo electrónico asociado con su cuenta de PayPal.")
    paypal_CONFIRM = models.StringField(initial="",
                                        label="Confirma el correo electrónico asociado con su cuenta de PayPal.")
    agree = models.StringField(
        widget=widgets.RadioSelectHorizontal(),
        choices=[['Agree', 'De acuerdo'],
                 ['Disagree', 'En desacuerdo']],
        label=" "
    )
    # HYPOTHETICAL
    hypothetical = models.IntegerField(
        label="Imagina que estás en una fiesta en la que no conoces a la mayoría de la gente. "
              "Estás hablando con un grupo de personas cuando alguien saca el tema del matrimonio entre personas del mismo sexo. "
              "De la discusión puedes deducir que la mayoría de las personas del grupo no apoyan tu punto de vista. "
              "En este tipo de situación, algunas personas expresarían su opinión y otras no. "
              "¿Qué tan probable es que expreses tu opinión en una situación así?",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy poco probable'],
                 [2, 'Poco probable'],
                 [3, 'Neutral'],
                 [4, 'Probable'],
                 [5, 'Muy probable'],
                 ]
    )
    # SOS COVARIATES
    worryIsolation = models.IntegerField(
        label="Me preocupa que me aíslen si la gente no está de acuerdo conmigo",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    notWorryAvoidance = models.IntegerField(
        label="No me preocupa que otras personas me eviten",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    riskAvoidance = models.IntegerField(
        label="Evito decir a los demás lo que pienso cuando existe el riesgo de que me eviten si conocen mi opinión",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    enjoyAvoidance = models.IntegerField(
        label="Disfruto evitando discusiones",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    intelligentsArgue = models.IntegerField(
        label="Discutir sobre temas controvertidos mejora mi inteligencia",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    enjoysArguments = models.IntegerField(
        label="Disfruto con una buena discusión sobre un tema controvertido",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    avoidsArguments = models.IntegerField(
        label="Intento no entrar en discusiones",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    # NEED TO EVALUATE
    strongOpinions1 = models.IntegerField(
        label="Me gusta tener opiniones firmes incluso cuando no estoy implicada/o personalmente",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    formsOpinions = models.IntegerField(
        label="Creo juicios y opiniones sobre todo",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    strongOpinions2 = models.IntegerField(
        label="Para mí, es muy importante tener opiniones sólidas y firmes",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    notNeutral = models.IntegerField(
        label="Me molesta ser neutral",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    opinionsAverage = models.IntegerField(
        label="Tengo muchas más opiniones que una persona común",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    strongOpinions3 = models.IntegerField(
        label="Prefiero tener una opinión firme a no tener opinión alguna",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    # INTEREST IN POLITICS
    interestPolitics = models.IntegerField(
        label="Me mantengo al día de noticias sobre política, políticas públicas, o asuntos controvertidos "
              "como raza, género o inmigración",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    # SOCIAL MEDIA
    socialMedia = models.IntegerField(
        label="Durante los últimos 12 meses, ¿has publicado contenido público (mensaje, post, comentario) en redes "
              "sociales (Facebook, X, YouTube, Instagram, Snapchat, TikTok, etc.) sobre política, políticas públicas o "
              "temas sociales controvertidos como la raza, el género o la inmigración?",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Sí'],
                 [2, 'No'],
                 ]
    )
    # ATTITUDE CERTAINTY
    attitudeCertainty = models.IntegerField(
        label="Tengo una fuerte convicción respecto a mi postura en este tema",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    # ISSUE IMPORTANCE
    issueImportance = models.IntegerField(
        label="Este tema es muy importante para mí personalmente",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    importantTU = models.IntegerField(
        widget=widgets.RadioSelectHorizontal(),
        choices=[[0, 'Poca importancia'],
                 [1, 'Ligeramente importante'],
                 [2, 'Neutral'],
                 [3, 'Moderadamente importante'],
                 [4, 'Muy importante']],
        label=C.txt_importTU
    )
    # MINORITY CLIMATE
    minorityClimate = models.IntegerField(
        label="Mi opinión sobre el tema es similar a la mayoría de las opiniones que oigo en mi entorno",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[1, 'Muy en desacuerdo'],
                 [2, 'En desacuerdo'],
                 [3, 'Ni de acuerdo ni en desacuerdo'],
                 [4, 'De acuerdo'],
                 [5, 'Muy de acuerdo'],
                 ]
    )
    # SCHEDULE FOR THE SECOND SESSION
    monday0930 = models.BooleanField(blank=True)
    monday1000 = models.BooleanField(blank=True)
    monday1030 = models.BooleanField(blank=True)
    monday1100 = models.BooleanField(blank=True)
    monday1130 = models.BooleanField(blank=True)
    monday1200 = models.BooleanField(blank=True)
    monday1230 = models.BooleanField(blank=True)
    monday1300 = models.BooleanField(blank=True)
    mondayNone = models.BooleanField(blank=True)


# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['paypal']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.paypal = player.paypal


class SoSQuestionnaire(Page):
    # timeout_seconds = C.TIMEOUT_S
    form_model = 'player'
    form_fields = ['worryIsolation', 'notWorryAvoidance', 'riskAvoidance', 'intelligentsArgue',
                   'avoidsArguments', 'enjoysArguments', 'hypothetical', 'strongOpinions1',
                   'formsOpinions', 'strongOpinions2', 'notNeutral', 'opinionsAverage', 'strongOpinions3',
                   'interestPolitics', 'socialMedia', 'socialMedia']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Questionnaire(Page):
    # changeAnswer
    # timeout_seconds = C.TIMEOUT_Q
    # if
    form_model = 'player'
    form_fields = ['agree', 'attitudeCertainty', 'issueImportance', 'minorityClimate']

    @staticmethod
    def vars_for_template(player: Player):
        N = player.round_number - 1
        return {
            'my_label': C.CSV[N]
        }


class Timeslots(Page):
    # timeout_seconds = 300
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def get_form_fields(player: Player):
        return [reason['name'] for reason in C.SCHEDULE_MONDAY]


class Results(Page):
    form_model = 'player'
    form_fields = ['paypal_CONFIRM']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Introduction, SoSQuestionnaire, Questionnaire, Results]
