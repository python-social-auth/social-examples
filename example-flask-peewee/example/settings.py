from os.path import dirname, abspath, join

SECRET_KEY = 'random-secret-key'
SESSION_COOKIE_NAME = 'psa_session'
DEBUG = True
DATABASE_URI = '%s/db.sqlite3' % dirname(abspath(join(__file__, '..')))
DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'

SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/done/'
SOCIAL_AUTH_USER_MODEL = 'example.models.user.User'
SOCIAL_AUTH_STORAGE = 'social_flask_peewee.models.FlaskStorage'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
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
    'social_core.backends.reddit.RedditOAuth2',
    'social_core.backends.mineid.MineIDOAuth2',
    'social_core.backends.wunderlist.WunderlistOAuth2',
    'social_core.backends.upwork.UpworkOAuth',
)
