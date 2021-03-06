import nltk
from intent.intent_manager import *
from snip.snip_account_balance import SnipAccountBalance

is_noun = lambda pos: pos[:2] == 'NN'

required_fields = ['currency', 'accountNumber']


class AccountBalance:

    def __init__(self, _dict=None):
        self.fields = dict() if _dict is None else _dict
        self.state = None
        self.tag = 'account_balance'

    def has_all_required_fields(self):
        if self.fields is None:
            return False
        if sorted(self.fields.keys()) == sorted(required_fields):
            return True
        else:
            return False

    def get_remaining_fields(self):

        return list((set(required_fields)).difference(set(self.fields.keys())))

    def get_account_balance(self):
        return ['you account balance is 100']

    def account_balance_handler(self, sentence):
        words = nltk.word_tokenize(sentence)

        snip = SnipAccountBalance.get_instance()
        parsed = snip.parse(sentence)
        if self.state is not None:
            self.fields[self.state] = sentence
            self.state = None
        else:
            fields = list(map(lambda x: (x['entity'], x['value']['value']), parsed['slots']))
            for field, value in fields:
                if field in required_fields:
                    self.fields[field] = value

        if self.has_all_required_fields():
            return self.get_account_balance(), None
        else:
            remaining_field = self.get_remaining_fields()[0]
            intent = get_intent('account_balance')
            self.state = remaining_field
            return intent['clarifications'], self

