import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    # SECRETS
    SECRET_KEY = os.environ.get('SECRET_KEY', 'You will never guess')
    ADVERT_SECRET_KEY = os.environ.get('ADVERT_SECRET_KY', 'You will newer know')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'SUPER SECRET')

    # DB
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL_ALCHEMY_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.app'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://')

    # PROPS
    HOST = os.environ.get('HOST', '192.168.1.92')
    PORT = os.environ.get('PORT', 5000)
    URL_FOR_REDIRECT_LINK = '{0}:{1}/redirect_link'.format(HOST, int(PORT))
    WTF_CSRF_ENABLED = True
    PROPAGATE_EXCEPTIONS = True

    MESSENGERS = [('None', 'None'),
                  ('skype', 'Skype'),
                  ('tele', 'Telegram'),
                  ('whatsapp', 'WatsApp'),
                  ('viber', 'Viber')]

    ACTION_TYPE = {
        1: 'Click',
        2: 'Add to cart',
        3: 'Order',
        4: 'Purchase',
    }
