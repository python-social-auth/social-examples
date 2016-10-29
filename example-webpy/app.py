import sys
import os

import web

from web.contrib.template import render_jinja

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from social_core.utils import setting_name

from common import filters
from common.utils import common_context

import local_settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

web.config.debug = False
web.config[setting_name('USER_MODEL')] = 'models.User'
web.config[setting_name('AUTHENTICATION_BACKENDS')] = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOpenId',
    'social_core.backends.stripe.StripeOAuth2',
    'social_core.backends.persona.PersonaAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.yahoo.YahooOAuth',
    'social_core.backends.angel.AngelOAuth2',
    'social_core.backends.behance.BehanceOAuth2',
    'social_core.backends.bitbucket.BitbucketOAuth',
    'social_core.backends.box.BoxOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.foursquare.FoursquareOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.live.LiveOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.dailymotion.DailymotionOAuth2',
    'social_core.backends.disqus.DisqusOAuth2',
    'social_core.backends.dropbox.DropboxOAuth',
    'social_core.backends.eveonline.EVEOnlineOAuth2',
    'social_core.backends.evernote.EvernoteSandboxOAuth',
    'social_core.backends.fitbit.FitbitOAuth2',
    'social_core.backends.flickr.FlickrOAuth',
    'social_core.backends.livejournal.LiveJournalOpenId',
    'social_core.backends.soundcloud.SoundcloudOAuth2',
    'social_core.backends.thisismyjam.ThisIsMyJamOAuth1',
    'social_core.backends.stocktwits.StocktwitsOAuth2',
    'social_core.backends.tripit.TripItOAuth',
    'social_core.backends.clef.ClefOAuth2',
    'social_core.backends.twilio.TwilioAuth',
    'social_core.backends.xing.XingOAuth',
    'social_core.backends.yandex.YandexOAuth2',
    'social_core.backends.podio.PodioOAuth2',
    'social_core.backends.mineid.MineIDOAuth2',
    'social_core.backends.wunderlist.WunderlistOAuth2',
    'social_core.backends.upwork.UpworkOAuth',
)
web.config[setting_name('LOGIN_REDIRECT_URL')] = '/done/'

from social_webpy.utils import psa, backends
from social_webpy import app as social_app


urls = (
    '^/$', 'main',
    '^/done/$', 'done',
    '', social_app.app_social
)

def url_for(name, **kwargs):
    if name == 'social:begin':
        url = "/login/{backend}/".format(**kwargs)
    elif name == 'social:complete':
        url = "/login/complete/{backend}/".format(**kwargs)
    else:
        url = "/{name}".format(name=name)
    return url

render = render_jinja(os.path.join(BASE_DIR, 'common', 'templates'))
render._lookup.filters.update({
    'backend_name': filters.backend_name,
    'backend_class': filters.backend_class,
    'icon_name': filters.icon_name,
    'social_backends': filters.social_backends,
    'legacy_backends': filters.legacy_backends,
    'oauth_backends': filters.oauth_backends,
    'filter_backends': filters.filter_backends,
    'slice_by': filters.slice_by
})
render._lookup.globals.update({
    'url': url_for
})


class AppBaseView(social_app.BaseViewClass):
    def render_home(self):
        context = common_context(
            web.config[setting_name('AUTHENTICATION_BACKENDS')],
            user=self.get_current_user(),
            plus_id=web.config.get(setting_name('SOCIAL_AUTH_GOOGLE_PLUS_KEY'))
        )
        return render.home(**context)


class main(AppBaseView):
    def GET(self):
        return self.render_home()


class done(AppBaseView):
    def GET(self):
        return self.render_home()


engine = create_engine('sqlite:///db.sqlite3')


def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

app = web.application(urls, locals())
app.add_processor(load_sqla)
session = web.session.Session(
    app,
    web.session.DiskStore(os.path.join(BASE_DIR, 'sessions'))
)

web.db_session = Session()
web.web_session = session
