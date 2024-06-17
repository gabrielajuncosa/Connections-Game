from otree.api import *
import pandas as pd
import numpy as np

import random
import time
import json

doc = """
Your app description
"""


# FUNCTIONS FOR BaseConstants
def open_CSV(filename):
    """
    :param filename: opinions.csv
    :return: a list of statements for the session
    """
    temp = pd.read_csv(filename, sep=',')
    csv = list(temp['statements'])
    return csv


def open_CLAVES(filename):
    """
    :param filename: checkCLAVE.csv
    :return: should return a list of passwords, NEEDS TO CHANGE
    """
    temp = pd.read_csv(filename, sep=',')
    csv = list(temp['clave'])
    return csv


class C(BaseConstants):
    NAME_IN_URL = 'inactives_S12'
    PLAYERS_PER_GROUP = None
    # HTML TEMPLATES
    CONSENTS_TEMPLATE = 'inactives_S12/introTemplate.html'  # UPDATE!

    # CSV FILES
    CSV_ANSWERS = pd.read_csv('D1S12_opinions.csv', sep=',')  # UPDATE!
    CSV = open_CSV('D1S12_opinions.csv')  # UPDATE!
    NUM_ROUNDS = len(open_CSV('D1S12_opinions.csv'))  # UPDATE!
    # NUM_ROUNDS = 4  # UPDATE!
    CLAVES = open_CLAVES('D1S12_claves.csv')  # UPDATE!

    # TIMEOUTS
    NoTIMEOUTS = 11  # max allowed timeouts
    TIMEOUT_YA = 20  # timeout yesterday answers
    TIMEOUT_IN = 1  # timeout inactives
    TIMEOUT_G = 75

    # PARAMETERS
    LANGUAGE = 'SPA'  # SPANISH = 'SPA' ENGLISH= 'EN"
    LINKS = 4
    ATTENTION_CHECKS = [5, 9, 13, 17, 20]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # INIT Introduction(Page)
    pagoEuros = models.FloatField()
    pagoEurosAll = models.FloatField()
    paypal = models.StringField(initial="", label="Ingresa la contraseña de ingreso que hemos enviado a tu correo.")
    typed1 = models.StringField(initial="")
    typed2 = models.StringField(initial="")
    claveOK = models.BooleanField(initial=False)
    # INIT EnterClaveAgain(Page)
    active = models.BooleanField(initial=True)
    # INIT YesterdaysAnswer(Page)
    changeAnswer = models.BooleanField(  # UPDATE!!
        label="¿Te gustaría cambiar tu respuesta?",
        choices=[[True, 'Sí'],
                 [False, 'No']],
    )
    agree = models.StringField(  # UPDATE!!
        widget=widgets.RadioSelectHorizontal(),
        choices=[['Agree', 'De acuerdo'],
                 ['Disagree', 'En desacuerdo'],
                 ],
    )
    timeoutCounter = models.IntegerField(initial=0)
    shareAnswer = models.BooleanField(  # UPDATE!!
        label="¿Te gustaría compartir esta opinión con tus contactos?",
        choices=[[True, 'Sí'],
                 [False, 'No']],
    )
    opinion_preview = models.LongStringField(initial="NO OPINION TO PREVIEW")
    opinion_prev_ID = models.IntegerField(initial=0)
    opinion_prev_COLOR = models.LongStringField(initial='Black')

    opinion_def = models.LongStringField(initial="UNDEFINED OPINION")
    opinion_def_ID = models.IntegerField(initial=0)
    opinion_def_COLOR = models.LongStringField(initial='Black')

    opinion_post = models.LongStringField(initial="NO OPINION TO POST")
    opinion_post_ID = models.IntegerField(initial=0)
    opinion_post_COLOR = models.LongStringField(initial='Black')

    # INIT WillingnessShareR1(Page)
    importantTO_R1 = models.IntegerField(
        label="¿Qué importancia crees tiene este tema para la SOCIEDAD ESPAÑOLA?",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[0, 'Poca importancia'],
                 [1, 'Ligeramente importante'],
                 [2, 'Neutral'],
                 [3, 'Moderadamente importante'],
                 [4, 'Muy importante']],
    )
    # INIT WillingnessShareR1plus(Page)
    importantTO_R1plus = models.IntegerField(
        label="¿Qué importancia crees que tiene este tema para tus CONEXIONES?",
        widget=widgets.RadioSelectHorizontal(),
        choices=[[0, 'Poca importancia'],
                 [1, 'Ligeramente importante'],
                 [2, 'Neutral'],
                 [3, 'Moderadamente importante'],
                 [4, 'Muy importante']],
    )
    # INIT WaitPages
    connections = models.LongStringField()
    i_follow = models.LongStringField()
    followers = models.LongStringField()
    i_dont_follow = models.LongStringField()
    messages = models.LongStringField()
    # INIT MyPage
    my_disconnects = models.IntegerField(initial=0)
    my_requests = models.IntegerField(initial=0)
    store_clicks = models.LongStringField(initial="")

    numAgree = models.IntegerField(initial=0)
    numDisagree = models.IntegerField(initial=0)
    numNeutral = models.IntegerField(initial=0)
    numDontKnow = models.IntegerField(initial=0)
    majority = models.StringField()
    payment = models.IntegerField(initial=0)
    # INIT GuessEstimate
    majorityGUESS = models.StringField(
        choices=[["Agree", 'La mayoría está de acuerdo'],
                 ["Disagree", 'La mayoría está de en desacuerdo'],
                 ["DontKnow", 'La mayoría prefiere no compartir opinión'],
                 ["No clear majority", 'No hay mayoría']],
        label="En la última ronda, ¿qué opinión crees que comparte la mayoría de tus conexiones?"
    )
    bonus = models.IntegerField(initial=0)


# FUNCTIONS FOR PAGES
def answer_yesterday(player: Player):
    """
    :param player: N, C.CSV, C.CSV_ANSWERS
    :return: agree-->opinion previos day
             answer-->message based on previous day answer
    """
    options = {'Agree': 'De acuerdo',
               'Disagree': 'En desacuerdo',
               }
    N = player.round_number - 1
    statement = C.CSV[N]
    index = list(C.CSV_ANSWERS['statements']).index(statement)
    agree = C.CSV_ANSWERS[player.participant.paypal][index]
    answer = options[agree]
    return agree, answer


def text_timestamp(statement):
    """
    :param statement: statement from file
    :return: text to post
    """
    post = "{0}.".format(statement.upper())
    return post


def return_color_prev_opinion(player: Player, opinion_ID):
    post_def_COLOR = player.opinion_def_COLOR
    if opinion_ID == 1:
        post_def_COLOR = 'color009'  # GREEN2
    elif opinion_ID == 2:
        post_def_COLOR = 'color010'  # RED2
    elif opinion_ID == 3:
        post_def_COLOR = 'color011'  # BLUE2
    return post_def_COLOR


def player_opinion_preview(player: Player, language):
    """
        NOTE: If running Spanish version, set language='SPA', else language='EN'
    """
    post_def_COLOR = player.opinion_def_COLOR
    post_list_EN = ["agrees.",
                    "disagrees.",
                    "neither agrees, nor disagrees."]

    post_list_SPA = ["está de acuerdo.",
                     "está en desacuerdo.",
                     "no está de acuerdo, ni en desacuerdo."]

    if language == 'SPA':
        post_list = post_list_SPA
    else:
        post_list = post_list_EN

    opinion_prev_ID = player.opinion_prev_ID
    post_prev_COLOR = player.opinion_prev_COLOR

    """ 
    if player.participant.active:
        if player.agree == 'Agree':
            post = post_list[0]
            opinion_prev_ID = 1
        elif player.agree == 'Disagree':
            post = post_list[1]
            opinion_prev_ID = 2
        else:
            post = post_list[2]
            opinion_prev_ID = 3
    else:
        rand_idx = random.randrange(len(post_list))
        post = post_list[rand_idx]
        opinion_prev_ID = rand_idx + 1
    """

    if player.agree == 'Agree':
        post = post_list[0]
        opinion_prev_ID = 1
    elif player.agree == 'Disagree':
        post = post_list[1]
        opinion_prev_ID = 2
    else:
        post = post_list[2]
        opinion_prev_ID = 3

    post_prev_COLOR = return_color_prev_opinion(player, opinion_prev_ID)
    return post, opinion_prev_ID, post_prev_COLOR


def player_opinion_def(player: Player, language):
    """
        NOTE: If running Spanish version, set language='SPA', for English language='EN'
    """
    post_SPA = "preferiría no compartir una opinión."
    post_EN = "would rather not share an opinion."

    post_def_COLOR = player.opinion_prev_COLOR
    opinion_def_ID = player.opinion_prev_ID

    """ 
    if player.participant.active:
        shareRandom_list = [True, False]
        rand_idx = random.randrange(len(shareRandom_list))
        player.shareAnswer = shareRandom_list[rand_idx]
    """
    if player.shareAnswer:
        post = player.opinion_preview
        opinion_def_ID = 1
    else:
        if language == 'SPA':
            post = post_SPA
        else:
            post = post_EN
        opinion_def_ID = 2
        post_def_COLOR = 'color008'
    return post, opinion_def_ID, post_def_COLOR


def player_opinion_post(player: Player, target, language):
    opinion_post_ME = player.opinion_def
    post_post_COLOR = player.opinion_def_COLOR
    message_by_color = {'color001': {'SPA': target.opinion_def, 'EN': target.opinion_def},  # BLACK
                        'color002': {'SPA': 'está de acuerdo contigo.', 'EN': 'you both agree.'},  # GREEN
                        'color003': {'SPA': 'está en desacuerdo contigo.', 'EN': 'you two disagree.'},  # RED
                        'color004': {'SPA': 'dijo que no sabe.', 'EN': 'they don\'t know.'},  # BLUE
                        'color005': {'SPA': 'dijo sí.', 'EN': 'they agree.'},  # YELLOW
                        'color006': {'SPA': 'dijo que no.', 'EN': 'they disagree.'},  # BROWN
                        'color007': {'SPA': 'ninguno sabeís.', 'EN': 'neither of you know.'}}  # FUCHSIA

    if target.opinion_def_ID == 1:  # They want to share
        if player.opinion_prev_ID == 1:
            if target.opinion_prev_ID == 1:
                post_post_COLOR = 'color002'  # GREEN: I agree, they agree
            elif target.opinion_prev_ID == 2:
                post_post_COLOR = 'color003'  # RED: I agree, they disagree
            else:
                post_post_COLOR = 'color004'  # BLUE: I agree, they don't know
            opinion_post_ME = message_by_color[post_post_COLOR][language]

        elif player.opinion_prev_ID == 2:
            if target.opinion_prev_ID == 1:
                post_post_COLOR = 'color003'  # RED: I disagree, they agree
            elif target.opinion_prev_ID == 2:
                post_post_COLOR = 'color002'  # GREEN: I disagree, they disagree
            else:
                post_post_COLOR = 'color004'  # BLUE: I disagree, they don't know
            opinion_post_ME = message_by_color[post_post_COLOR][language]

        elif player.opinion_prev_ID == 3:
            if target.opinion_prev_ID == 1:
                post_post_COLOR = 'color005'  # YELLOW: I don't know, they agree
            elif target.opinion_prev_ID == 2:
                post_post_COLOR = 'color006'  # BROWN: I don't know, they disagree
            else:
                post_post_COLOR = 'color007'  # FUCHSIA: I don't know, they don't know
            opinion_post_ME = message_by_color[post_post_COLOR][language]

    else:  # They'd rather not share
        post_post_COLOR = 'color001'  # BLACK
        opinion_post_ME = message_by_color[post_post_COLOR][language]

    return opinion_post_ME, post_post_COLOR


def player_opinion_post_ID(player: Player):
    opinion_post_ID = player.opinion_post_ID

    if player.opinion_def_ID == 1:
        opinion_post_ID = player.opinion_prev_ID
    else:
        opinion_post_ID = 4
    return opinion_post_ID


def random_regular_graph(n, k):
    ''' Returns an edge list corresponding to a random k-regular graph
        with n nodes.

        This is a simple algorithm for which n*k must be even.
    '''
    if n * k % 2 != 0:
        print('n*k must be even')
    else:
        success = False
        i = 0
        while True:
            if success:
                break

            pn = range(n * k)
            candidates = list(pn)
            matchings = []
            while True:
                if len(candidates) == 0:
                    break
                x, y = np.random.choice(candidates, 2, replace=False)
                matchings.append((x, y))
                candidates.pop(candidates.index(x))
                candidates.pop(candidates.index(y))

            el = [sorted([(x // k), (y // k)]) for x, y in matchings]
            dictio = {}

            self_loops = np.any([x == y for x, y in el])
            multi_edges = np.unique(['%s,%s' % (x, y) for x, y in el], return_counts=True)
            multi_edges = np.any(multi_edges[1] > 1)

            if not self_loops and not multi_edges:
                success = True

            i += 1
            # print('success: %s' % success, el)
        print('Success in %s attempt(s)...' % i)
        el = [[x + 1, y + 1] for x, y in el]
        return el


def random_connections(group: Group, k):
    all_players = [p.id_in_group for p in group.get_players()]
    n = len(all_players)
    el = random_regular_graph(n, k)
    degs = [sum([x in v for v in el]) for x in range(1, n + 1)]
    print('Correct degrees: ', np.all([d == k for d in degs]))
    dict_connections = dict([(x, []) for x in range(1, n + 1)])
    for i in el:
        dict_connections[int(i[0])].append(int(i[1]))
    return dict_connections


def get_connections_init(group: Group, dictio):
    dict_followers = {}
    players = [p.id_in_group for p in group.get_players()]
    for p in players:
        temp_list = [k for k, v in dictio.items() if p in v] + dictio[p]
        dict_followers[p] = random.sample(temp_list, len(temp_list))
    return dict_followers


def save_click_timestamp(player: Player, leader, leader_id, msg_type):
    temp = dict(
        source=player.id_in_group,
        target=leader_id,
        action=msg_type,
        timestamp=time.time(),
    )
    return temp


def remove_Participant(target_id, temp_list):
    res = temp_list
    if target_id in res:
        res.remove(target_id)
    return res


def append_Participant(target_id, temp_list):
    res = temp_list
    if target_id not in res:
        res.append(target_id)
        aux = random.sample(res, len(res))
        res = aux
    return res


def update_feed(player: Player, target_id, target):
    temp = [p['round'] for p in player.participant.messages[target_id]]
    feed = player.participant.messages
    opinion_post, opinion_color = player_opinion_post(player, target, C.LANGUAGE)
    if np.logical_or(not temp, player.round_number not in temp):
        feed[target_id].append({
            # 'statement': C.CSV['statement'][player.round_number - 1],
            'statement': C.CSV[player.round_number - 1],
            'text': opinion_post,
            'color': opinion_color,
            'nickname': target.participant.nickname,
            'round': target.round_number, })
    return feed


def all_activos(group: Group):
    activos = {}
    for player in group.get_players():
        activos[player.id_in_group] = {}
        activos[player.id_in_group]['nickname'] = player.participant.nickname
        activos[player.id_in_group]['active'] = player.participant.active
    return activos


def live_method(player: Player, data):
    group = player.group
    my_id = player.id_in_group

    msg_type = data['type']

    broadcast = {}
    if msg_type == 'toggle_connect':
        leader_id = data['id_in_group']
        leader = group.get_player_by_id(leader_id)
        player.my_requests += 10
        # save click action with timestamp
        temp = save_click_timestamp(player, leader, leader_id, msg_type)
        player.store_clicks += json.dumps(temp) + ';'
        # action for ME
        player.participant.i_dont_follow = remove_Participant(leader_id,
                                                              player.participant.i_dont_follow)
        player.participant.i_follow = append_Participant(leader_id,
                                                         player.participant.i_follow)
        # action for OTHER
        leader.participant.i_dont_follow = remove_Participant(my_id,
                                                              leader.participant.i_dont_follow)
        leader.participant.followers = append_Participant(my_id,
                                                          leader.participant.followers)

        broadcast[leader_id] = dict(followers=leader.participant.followers,
                                    i_dont_follow=leader.participant.i_dont_follow)

    if msg_type == 'toggle_undo':
        leader_id = data['id_in_group']
        leader = group.get_player_by_id(leader_id)
        # save click action with timestamp
        temp = save_click_timestamp(player, leader, leader_id, msg_type)
        player.store_clicks += json.dumps(temp) + ';'
        # action for ME
        player.participant.i_follow = remove_Participant(leader_id,
                                                         player.participant.i_follow)
        player.participant.i_dont_follow = append_Participant(leader_id,
                                                              player.participant.i_dont_follow)
        # action for OTHER
        leader.participant.followers = remove_Participant(my_id,
                                                          leader.participant.followers)
        leader.participant.i_dont_follow = append_Participant(my_id,
                                                              leader.participant.i_dont_follow)
        broadcast[leader_id] = dict(followers=leader.participant.followers,
                                    i_dont_follow=leader.participant.i_dont_follow)

    if msg_type == 'toggle_accept':
        leader_id = data['id_in_group']
        leader = group.get_player_by_id(leader_id)
        # save click action with timestamp
        temp = save_click_timestamp(player, leader, leader_id, msg_type)
        player.store_clicks += json.dumps(temp) + ';'
        # action for ME
        player.participant.followers = remove_Participant(leader_id,
                                                          player.participant.followers)
        player.participant.connections = append_Participant(leader_id,
                                                            player.participant.connections)

        player.participant.messages = update_feed(player, leader_id, leader)

        # action for OTHER
        leader.participant.i_follow = remove_Participant(my_id,
                                                         leader.participant.i_follow)
        leader.participant.connections = append_Participant(my_id,
                                                            leader.participant.connections)

        leader.participant.messages = update_feed(leader, my_id, player)

        broadcast[leader_id] = dict(i_follow=leader.participant.i_follow,
                                    connections=leader.participant.connections,
                                    messages=leader.participant.messages)

    if msg_type == 'toggle_reject':
        leader_id = data['id_in_group']
        leader = group.get_player_by_id(leader_id)
        print(leader, leader.my_disconnects)
        # save click action with timestamp
        temp = save_click_timestamp(player, leader, leader_id, msg_type)
        player.store_clicks += json.dumps(temp) + ';'
        # action for ME
        player.participant.followers = remove_Participant(leader_id,
                                                          player.participant.followers)
        player.participant.i_dont_follow = append_Participant(leader_id,
                                                              player.participant.i_dont_follow)
        # action for OTHER
        leader.participant.i_follow = remove_Participant(my_id,
                                                         leader.participant.i_follow)
        leader.participant.i_dont_follow = append_Participant(my_id,
                                                              leader.participant.i_dont_follow)

        broadcast[leader_id] = dict(i_follow=leader.participant.i_follow,
                                    i_dont_follow=leader.participant.i_dont_follow)

    if msg_type == 'toggle_disconnect':
        leader_id = data['id_in_group']
        leader = group.get_player_by_id(leader_id)
        leader.my_disconnects += 10
        # save click action with timestamp
        temp = save_click_timestamp(player, leader, leader_id, msg_type)
        player.store_clicks += json.dumps(temp) + ';'
        # action for ME
        player.participant.connections = remove_Participant(leader_id,
                                                            player.participant.connections)
        player.participant.i_dont_follow = append_Participant(leader_id,
                                                              player.participant.i_dont_follow)
        # action for OTHER
        leader.participant.connections = remove_Participant(my_id,
                                                            leader.participant.connections)
        leader.participant.i_dont_follow = append_Participant(my_id,
                                                              leader.participant.i_dont_follow)
        broadcast[leader_id] = dict(connections=leader.participant.connections,
                                    i_dont_follow=leader.participant.i_dont_follow)

    broadcast.update(
        {
            my_id: dict(
                full_load=True,
                connections=player.participant.connections,
                followers=player.participant.followers,
                i_follow=player.participant.i_follow,
                i_dont_follow=player.participant.i_dont_follow,
                messages=player.participant.messages,
                active=player.participant.active,
            )
        }
    )
    return broadcast


def all_nicknames(group: Group):
    nicknames = {}
    P = len(list(group.get_players()))
    position = list(range(1, P + 1))
    random.shuffle(position)
    for player in group.get_players():
        nicknames[player.id_in_group] = {}
        nicknames[player.id_in_group]['nickname'] = player.participant.nickname
        nicknames[player.id_in_group]['position'] = position[player.id_in_group - 1]
    return nicknames


def Majorities(player: Player):
    temp = [("Agree", player.numAgree),
            ("Disagree", player.numDisagree),
            ("Neutral", player.numNeutral),
            ("DontKnow", player.numDontKnow)]
    temp = Sort_Tuple(temp)
    if temp[1][1] == temp[0][1]:
        return "No clear majority"
    else:
        return temp[0][0]


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[1], reverse=True)
    return tup


# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['paypal']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        messages = 'images/' + 'tabla.png'
        popUp = 'images/' + 'popUp.png'
        panel = 'images/' + 'panelview.png'
        return dict(messages=messages,
                    popUp=popUp,
                    panel=panel)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # INIT for all
        player.participant.nickname = "Usuario {0}".format(player.id_in_group + 19)
        player.participant.timeoutCounter = 0
        # check if password provided is in list, else try again
        player.typed1 = player.paypal
        if player.paypal in C.CLAVES:
            player.claveOK = True
            # INIT only if password is correct
            player.participant.paypal = player.paypal[1:5]
            player.participant.active = player.active
        else:
            player.paypal = ""


class EnterClaveAgain(Page):
    form_model = 'player'
    form_fields = ['paypal']

    @staticmethod
    def is_displayed(player: Player):
        return np.logical_and(not player.claveOK, player.round_number == 1)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.typed2 = player.paypal
        if player.paypal in C.CLAVES:
            player.claveOK = True
        else:
            player.claveOK = False
            player.active = False  # player must be considered inactive
            player.paypal = C.CLAVES[random.randint(1, len(C.CLAVES))]  # but answers must be assigned. UPDATE!!
        # INIT for those who did not put password correctly at first
        player.participant.paypal = player.paypal[1:5]
        player.participant.active = player.active


class CannotContinue(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player: Player):
        return np.logical_and(not player.claveOK, player.round_number == 1)


class practiceGuessEstimate(Page):
    form_model = 'player'
    form_fields = ['majorityGUESS']

    @staticmethod
    def vars_for_template(player: Player):
        messages = 'images/' + 'tabla.png'
        popUp = 'images/' + 'popUp.png'
        panel = 'images/' + 'panelview.png'
        return dict(messages=messages,
                    popUp=popUp,
                    panel=panel)

    @staticmethod
    def is_displayed(player: Player):
        return np.logical_and(player.claveOK, player.round_number == 1)


class YesterdaysAnswer(Page):
    form_model = 'player'
    form_fields = ['changeAnswer']

    @staticmethod
    def get_timeout_seconds(player):
        """
        print("Round: ", player.round_number)
        print("   Active: ", player.participant.active)
        print("   Timeouts here: ",  player.timeoutCounter)
        print("   Timeouts universal: ", player.participant.timeoutCounter)
        """
        if player.participant.timeoutCounter > C.NoTIMEOUTS:
            player.active = False
            player.participant.active = player.active
        if player.participant.active:
            return C.TIMEOUT_YA
        else:
            return C.TIMEOUT_IN

    @staticmethod
    def vars_for_template(player: Player):
        N = player.round_number - 1
        player.agree, answer = answer_yesterday(player)
        return {
            'my_label': C.CSV[N],
            'yesterday': answer
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.participant.active:
            player.active = False
        if timeout_happened:
            if player.participant.active:
                player.timeoutCounter += 1  # counts timeouts in this rounds
                player.participant.timeoutCounter += 1  # counts timeouts for all rounds
            player.changeAnswer = random.choice([True, False])

        if player.changeAnswer:
            if player.agree == 'Agree':
                player.agree = 'Disagree'
            else:
                player.agree = 'Agree'
        player.opinion_preview, player.opinion_prev_ID, player.opinion_prev_COLOR = player_opinion_preview(player,
                                                                                                           language=C.LANGUAGE)


class WillingnessShareR1(Page):
    form_model = 'player'
    form_fields = ['shareAnswer', 'importantTO_R1']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def get_timeout_seconds(player):
        """
        print("Round: ", player.round_number)
        print("   Active: ", player.participant.active)
        print("   Timeouts here: ",  player.timeoutCounter)
        print("   Timeouts universal: ", player.participant.timeoutCounter)
        """
        if player.participant.timeoutCounter > C.NoTIMEOUTS:
            player.active = False
            player.participant.active = player.active
        if player.participant.active:
            return C.TIMEOUT_YA
        else:
            return C.TIMEOUT_IN

    @staticmethod
    def vars_for_template(player: Player):
        my_id = player.id_in_group
        N = player.round_number - 1
        statement = text_timestamp(C.CSV[N])
        return {'my_label': C.CSV[N],
                'statement': statement,
                'opinion': player.opinion_preview,
                'my_id': my_id,
                'nickname': player.participant.nickname, }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.participant.active:
            player.active = False
        if timeout_happened:
            if player.participant.active:
                player.timeoutCounter += 1  # counts timeouts in this rounds
                player.participant.timeoutCounter += 1  # counts timeouts for all rounds
            player.shareAnswer = random.choice([True, False])
        player.opinion_def, player.opinion_def_ID, player.opinion_def_COLOR = player_opinion_def(player,
                                                                                                 language=C.LANGUAGE)
        player.opinion_post_ID = player_opinion_post_ID(player)


class WillingnessShareR1plus(Page):
    form_model = 'player'
    form_fields = ['shareAnswer', 'importantTO_R1plus']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1

    @staticmethod
    def get_timeout_seconds(player):
        """
        print("Round: ", player.round_number)
        print("   Active: ", player.participant.active)
        print("   Timeouts here: ",  player.timeoutCounter)
        print("   Timeouts universal: ", player.participant.timeoutCounter)
        """
        if player.participant.timeoutCounter > C.NoTIMEOUTS:
            player.active = False
            player.participant.active = player.active
        if player.participant.active:
            return C.TIMEOUT_YA
        else:
            return C.TIMEOUT_IN

    @staticmethod
    def vars_for_template(player: Player):
        my_id = player.id_in_group
        N = player.round_number - 1
        statement = text_timestamp(C.CSV[N])
        return {'my_label': C.CSV[N],
                'statement': statement,
                'opinion': player.opinion_preview,
                'my_id': my_id,
                'nickname': player.participant.nickname, }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.participant.active:
            player.active = False
        if timeout_happened:
            if player.participant.active:
                player.timeoutCounter += 1  # counts timeouts in this rounds
                player.participant.timeoutCounter += 1  # counts timeouts for all rounds
            player.shareAnswer = random.choice([True, False])
        player.opinion_def, player.opinion_def_ID, player.opinion_def_COLOR = player_opinion_def(player,
                                                                                                 language=C.LANGUAGE)
        player.opinion_post_ID = player_opinion_post_ID(player)


class MyWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        random_connections_dict = random_connections(group, C.LINKS)
        connections_dict = get_connections_init(group, random_connections_dict)

        for player in group.get_players():
            # print("PLAYER: ", player.id_in_group, "CONNECTIONS: ", connections_dict[player.id_in_group])
            player.participant.cumm_payoff = 0
            # player.nickname = player.participant.nickname
            player.participant.clicks = []

            player.participant.connections = connections_dict[player.id_in_group] + [player.id_in_group]
            player.participant.connections_INIT = player.participant.connections
            # people I sent request to
            player.participant.i_follow = []
            player.participant.i_follow_INIT = player.participant.i_follow
            # requests received
            player.participant.followers = []
            player.participant.followers_INIT = player.participant.followers
            notInList = player.participant.i_follow + player.participant.followers + player.participant.connections
            player.participant.i_dont_follow = [p.id_in_group for p in group.get_players()
                                                if p.id_in_group not in notInList]
            player.participant.i_dont_follow_INIT = player.participant.i_dont_follow

            player.participant.messages = {}
            for p in group.get_players():
                player.participant.messages[p.id_in_group] = []

            player.participant.messages[player.id_in_group].append(
                {  # 'statement': C.CSV['statement'][player.round_number - 1],
                    'statement': C.CSV[player.round_number - 1],
                    # 'text': player.opinion_def,
                    'text': player.opinion_preview,
                    # 'color': player.opinion_def_COLOR,
                    'color': player.opinion_prev_COLOR,
                    'nickname': player.participant.nickname,
                    'round': player.round_number})

            for leader_id in player.participant.connections:
                if leader_id != player.id_in_group:
                    leader = group.get_player_by_id(leader_id)
                    opinion_post, opinion_color = player_opinion_post(player, leader, C.LANGUAGE)
                    player.participant.messages[leader_id].append({
                        'statement': C.CSV[player.round_number - 1],
                        # 'statement': C.CSV['statement'][player.round_number - 1],
                        'text': opinion_post,
                        'color': opinion_color,
                        'nickname': leader.participant.nickname,
                        'round': leader.round_number})
            # print("PLAYER ", player.id_in_group, ": ", player.participant.messages)
            player.participant.messages_INIT = player.participant.messages

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class MyWaitPageTwo(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            # add my opinion and then the rest
            player.participant.messages[player.id_in_group].append(
                {  # 'statement': C.CSV['statement'][player.round_number - 1],
                    'statement': C.CSV[player.round_number - 1],
                    # 'text': player.opinion_def,
                    'text': player.opinion_preview,
                    # 'color': player.opinion_def_COLOR,
                    'color': player.opinion_prev_COLOR,
                    'nickname': player.participant.nickname,
                    'round': player.round_number})

            for leader_id in player.participant.connections:
                if leader_id != player.id_in_group:
                    leader = group.get_player_by_id(leader_id)
                    opinion_post, opinion_color = player_opinion_post(player, leader, C.LANGUAGE)
                    player.participant.messages[leader_id].append({
                        # 'statement': C.CSV['statement'][player.round_number - 1],
                        'statement': C.CSV[player.round_number - 1],
                        'text': opinion_post,
                        'color': opinion_color,
                        'nickname': leader.participant.nickname,
                        'round': leader.round_number})
            # print("PLAYER ", player.id_in_group, ": ", player.participant.messages)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1


class MyPage(Page):
    timeout_seconds = C.TIMEOUT_G
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group,
                    nickname=player.participant.nickname,
                    cumm_payoff=player.participant.cumm_payoff)

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        nicknames = all_nicknames(group)
        activos = all_activos(group)
        return {
            # 'statement': C.CSV['statement'][player.round_number - 1],
            'statement': C.CSV[player.round_number - 1],
            'nicknames': nicknames,
            'actives': activos,
            # COLORS IN HEX
            'color001': '#636363',  # BLACK
            'color002': '#31a354',  # GREEN
            'color003': '#de2d26',  # RED
            'color004': '#7fcdbb',  # BLUE
            'color005': '#fec44f',  # YELLOW
            'color006': '#d95f0e',  # BROWN
            'color007': '#dd1c77',  # FUCHSIA
            'color008': '#7570b3',  # PURPLE
            'color009': '#1b9e77',  # GREEN2
            'color010': '#d95f02',  # RED2
            'color011': '#1f78b4',  # BLUE2
            'color012': '#bdbdbd',  # GREY
            'color013': '#f7fcb9',  # box_1
            'color014': '#f0f0f0',  # box_2
            'color015': '#9ebcda',  # button_1
            'color016': '#91bfdb',  # button_2
            'color017': '#a1d76a',  # button_3
            'color018': '#d73027',  # button_4
            'color019': '#e7d4e8',  # box_3
            'color020': '#d9f0d3',  # box_4
            'color021': '#ffffbf',  # box_5
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payment = ((len(player.participant.connections) - 1) * 100) - (
                player.my_requests + player.my_disconnects)
        player.participant.cumm_payoff += player.payment

        group = player.group
        # print("BEFORE: ", player.numAgree, player.numDisagree, player.numNeutral, player.numDontKnow)
        for leader_id in player.participant.connections:
            if leader_id != player.id_in_group:
                leader = group.get_player_by_id(leader_id)
                if leader.opinion_post_ID == 1:
                    player.numAgree += 1
                elif leader.opinion_post_ID == 2:
                    player.numDisagree += 1
                elif leader.opinion_post_ID == 3:
                    player.numNeutral += 1
                elif leader.opinion_post_ID == 4:
                    player.numDontKnow += 1

        player.majority = Majorities(player)
        # print("AFTER: ", player.numAgree, player.numDisagree, player.numNeutral, player.numDontKnow)
        # print("MAJORITY: ", player.majority)

        # SAVE NETWORK DATA
        player.connections = str(player.participant.connections)
        player.i_follow = str(player.participant.i_follow)
        player.followers = str(player.participant.followers)
        player.i_dont_follow = str(player.participant.i_dont_follow)
        player.messages = str(player.participant.messages)


class GuessEstimate(Page):
    form_model = 'player'
    form_fields = ['majorityGUESS']

    @staticmethod
    def get_timeout_seconds(player):
        """
        print("Round: ", player.round_number)
        print("   Active: ", player.participant.active)
        print("   Timeouts here: ",  player.timeoutCounter)
        print("   Timeouts universal: ", player.participant.timeoutCounter)
        """
        if player.participant.timeoutCounter > C.NoTIMEOUTS:
            player.active = False
            player.participant.active = player.active
        if player.participant.active:
            return C.TIMEOUT_YA
        else:
            return C.TIMEOUT_IN

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        print("GUESS: ", player.majorityGUESS)
        print("REAL: ", player.majority)

        if timeout_happened:
            player.bonus = 0
        else:
            if player.majorityGUESS == player.majority:
                player.bonus += 100
            else:
                player.bonus = 0

        player.participant.cumm_payoff = player.participant.cumm_payoff + player.bonus

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in C.ATTENTION_CHECKS


class Results(Page):
    @staticmethod
    def get_timeout_seconds(player):
        """
        print("Round: ", player.round_number)
        print("   Active: ", player.participant.active)
        print("   Timeouts here: ",  player.timeoutCounter)
        print("   Timeouts universal: ", player.participant.timeoutCounter)
        """
        if player.participant.timeoutCounter > C.NoTIMEOUTS:
            player.active = False
            player.participant.active = player.active
        if player.participant.active:
            return C.TIMEOUT_YA
        else:
            return C.TIMEOUT_IN

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'my_connection_points': (len(player.participant.connections) - 1) * 100,
            'my_connections': (len(player.participant.connections) - 1),
            'my_requests': int(player.my_requests / 10),
            'my_requests_deductions': player.my_requests,
            'my_disconnects': int(player.my_disconnects / 10),
            'my_disconnects_deductions': player.my_disconnects,
            'my_lost_points': player.my_requests + player.my_disconnects,
            'my_bonus_points': player.bonus,
            'my_earn_points': ((len(player.participant.connections) - 1) * 100) + player.bonus,
            'total_points': player.payment + player.bonus,
            'cumm_payment': player.participant.cumm_payoff,
        }

    @staticmethod
    def is_displayed(player: Player):
        # return np.logical_and(player.round_number < C.NUM_ROUNDS, player.participant.active)
        return player.participant.active


class MyWaitPageThree(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        all_points = [player.participant.cumm_payoff for player in group.get_players() if player.participant.active]
        mean_points = np.mean(all_points)
        rate = 15 / mean_points
        for player in group.get_players():
            player.pagoEuros = round(player.participant.cumm_payoff * rate, 2)
            player.pagoEurosAll = player.pagoEuros + 2.00

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class ResultsFinal(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'my_connection_points': (len(player.participant.connections) - 1) * 100,
            'my_connections': (len(player.participant.connections) - 1),
            'my_requests': int(player.my_requests / 10),
            'my_requests_deductions': player.my_requests,
            'my_disconnects': int(player.my_disconnects/10),
            'my_disconnects_deductions': player.my_disconnects,
            'my_lost_points': player.my_requests + player.my_disconnects,
            'my_bonus_points': player.bonus,
            'my_earn_points': ((len(player.participant.connections) - 1) * 100) + player.bonus,
            'total_points': player.payment + player.bonus,
            'cumm_payment': player.participant.cumm_payoff,
            'payoff': player.pagoEuros,
            'payoffAll': player.pagoEurosAll,
        }

    @staticmethod
    def is_displayed(player: Player):
        return np.logical_and(player.round_number == C.NUM_ROUNDS, player.participant.active)


page_sequence = [Introduction, EnterClaveAgain, CannotContinue, practiceGuessEstimate, YesterdaysAnswer,
                 WillingnessShareR1,
                 WillingnessShareR1plus, MyWaitPage, MyWaitPageTwo, MyPage, GuessEstimate, Results,
                 MyWaitPageThree, ResultsFinal]
