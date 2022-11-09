import sys
import os

import web

from web.contrib.template import render_jinja

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from social_core.utils import setting_name
from social_webpy.utils import load_strategy

from common import filters
from common.utils import common_context, url_for

import local_settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

web.config.debug = False
web.config[setting_name("USER_MODEL")] = "models.User"
web.config[setting_name("AUTHENTICATION_BACKENDS")] = (
    "social_core.backends.amazon.AmazonOAuth2",
    "social_core.backends.angel.AngelOAuth2",
    "social_core.backends.aol.AOLOpenId",
    "social_core.backends.appsfuel.AppsfuelOAuth2",
    "social_core.backends.beats.BeatsOAuth2",
    "social_core.backends.behance.BehanceOAuth2",
    "social_core.backends.belgiumeid.BelgiumEIDOpenId",
    "social_core.backends.bitbucket.BitbucketOAuth",
    "social_core.backends.box.BoxOAuth2",
    "social_core.backends.clef.ClefOAuth2",
    "social_core.backends.coinbase.CoinbaseOAuth2",
    "social_core.backends.coursera.CourseraOAuth2",
    "social_core.backends.dailymotion.DailymotionOAuth2",
    "social_core.backends.deezer.DeezerOAuth2",
    "social_core.backends.disqus.DisqusOAuth2",
    "social_core.backends.douban.DoubanOAuth2",
    "social_core.backends.dropbox.DropboxOAuth",
    "social_core.backends.dropbox.DropboxOAuth2",
    "social_core.backends.eveonline.EVEOnlineOAuth2",
    "social_core.backends.evernote.EvernoteSandboxOAuth",
    "social_core.backends.facebook.FacebookAppOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.fedora.FedoraOpenId",
    "social_core.backends.fitbit.FitbitOAuth2",
    "social_core.backends.flickr.FlickrOAuth",
    "social_core.backends.foursquare.FoursquareOAuth2",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.google.GoogleOAuth",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.google.GoogleOpenId",
    "social_core.backends.google.GooglePlusAuth",
    "social_core.backends.google_openidconnect.GoogleOpenIdConnect",
    "social_core.backends.instagram.InstagramOAuth2",
    "social_core.backends.jawbone.JawboneOAuth2",
    "social_core.backends.kakao.KakaoOAuth2",
    "social_core.backends.linkedin.LinkedinOAuth",
    "social_core.backends.linkedin.LinkedinOAuth2",
    "social_core.backends.live.LiveOAuth2",
    "social_core.backends.livejournal.LiveJournalOpenId",
    "social_core.backends.mailru.MailruOAuth2",
    "social_core.backends.mendeley.MendeleyOAuth",
    "social_core.backends.mendeley.MendeleyOAuth2",
    "social_core.backends.mineid.MineIDOAuth2",
    "social_core.backends.mixcloud.MixcloudOAuth2",
    "social_core.backends.nationbuilder.NationBuilderOAuth2",
    "social_core.backends.odnoklassniki.OdnoklassnikiOAuth2",
    "social_core.backends.open_id.OpenIdAuth",
    "social_core.backends.openstreetmap.OpenStreetMapOAuth",
    "social_core.backends.persona.PersonaAuth",
    "social_core.backends.podio.PodioOAuth2",
    "social_core.backends.rdio.RdioOAuth1",
    "social_core.backends.rdio.RdioOAuth2",
    "social_core.backends.readability.ReadabilityOAuth",
    "social_core.backends.reddit.RedditOAuth2",
    "social_core.backends.runkeeper.RunKeeperOAuth2",
    "social_core.backends.sketchfab.SketchfabOAuth2",
    "social_core.backends.skyrock.SkyrockOAuth",
    "social_core.backends.soundcloud.SoundcloudOAuth2",
    "social_core.backends.spotify.SpotifyOAuth2",
    "social_core.backends.stackoverflow.StackoverflowOAuth2",
    "social_core.backends.steam.SteamOpenId",
    "social_core.backends.stocktwits.StocktwitsOAuth2",
    "social_core.backends.stripe.StripeOAuth2",
    "social_core.backends.suse.OpenSUSEOpenId",
    "social_core.backends.thisismyjam.ThisIsMyJamOAuth1",
    "social_core.backends.trello.TrelloOAuth",
    "social_core.backends.tripit.TripItOAuth",
    "social_core.backends.tumblr.TumblrOAuth",
    "social_core.backends.twilio.TwilioAuth",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.weibo.WeiboOAuth2",
    "social_core.backends.wunderlist.WunderlistOAuth2",
    "social_core.backends.xing.XingOAuth",
    "social_core.backends.yahoo.YahooOAuth",
    "social_core.backends.yahoo.YahooOpenId",
    "social_core.backends.yammer.YammerOAuth2",
    "social_core.backends.yandex.YandexOAuth2",
    "social_core.backends.vimeo.VimeoOAuth1",
    "social_core.backends.lastfm.LastFmAuth",
    "social_core.backends.moves.MovesOAuth2",
    "social_core.backends.vend.VendOAuth2",
    "social_core.backends.email.EmailAuth",
    "social_core.backends.username.UsernameAuth",
    "social_core.backends.upwork.UpworkOAuth",
)
web.config[setting_name("PIPELINE")] = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "common.pipeline.require_email",
    "social_core.pipeline.mail.mail_validation",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.debug.debug",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "social_core.pipeline.debug.debug",
)

for name, value in local_settings.__dict__.items():
    if name.startswith("SOCIAL_AUTH"):
        web.config[name] = value

web.config[setting_name("LOGIN_REDIRECT_URL")] = "/done/"

from social_webpy.utils import psa, backends
from social_webpy import app as social_app


urls = (
    "^/$",
    "main",
    "^/done/?$",
    "done",
    "^/email/?$",
    "email",
    "",
    social_app.app_social,
)

render = render_jinja(os.path.join(BASE_DIR, "common", "templates"))
render._lookup.filters.update(
    {
        "backend_name": filters.backend_name,
        "backend_class": filters.backend_class,
        "icon_name": filters.icon_name,
        "social_backends": filters.social_backends,
        "legacy_backends": filters.legacy_backends,
        "oauth_backends": filters.oauth_backends,
        "filter_backends": filters.filter_backends,
        "slice_by": filters.slice_by,
    }
)
render._lookup.globals.update({"url": url_for})


class AppBaseView(social_app.BaseViewClass):
    def render_home(self, **extra):
        context = common_context(
            web.config[setting_name("AUTHENTICATION_BACKENDS")],
            load_strategy(),
            user=self.get_current_user(),
            plus_id=web.config.get(setting_name("SOCIAL_AUTH_GOOGLE_PLUS_KEY")),
            **extra
        )
        return render.home(**context)


class main(AppBaseView):
    def GET(self):
        return self.render_home()


class done(AppBaseView):
    def GET(self):
        return self.render_home()


class email(AppBaseView):
    def GET(self):
        strategy = load_strategy()
        partial_token = web.input(_method="get").get("partial_token")
        partial = strategy.partial_load(partial_token)
        return self.render_home(
            email_required=True,
            partial_backend_name=partial.backend,
            partial_token=partial_token,
        )


engine = create_engine("sqlite:///db.sqlite3")


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
    app, web.session.DiskStore(os.path.join(BASE_DIR, "sessions"))
)

web.db_session = Session()
web.web_session = session
