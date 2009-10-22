import pickle
import twitter.twitter as twitter_real
class twitter:
    class Api:
        def __init__(self, username, password, input_encoding=None):

            pass

        def GetPublicTimeline(self, limit, reload=True):
            if reload:
                real_api = twitter_real.Api('SineX', '')
                o = real_api.GetPublicTimeline( 100)
                f = open('/tmp/publicTimeLine', 'w')
                pickle.dump(o, f)
            f = open('/tmp/publicTimeLine', 'r')
            return pickle.load(f)

        def GetFriendsTimeline(self, user, limit, reload=False):
            if reload:
                real_api = twitter_real.Api('SineX', '')
                o = real_api.GetFriendsTimeline('SineX', 100)
                f = open('/tmp/friendsTimeLine', 'w')
                pickle.dump(o, f)
                print "reloaded"
            f = open('/tmp/friendsTimeLine', 'r')
            return pickle.load(f)

        def GetDirectMessages(user):
            f = open('/tmp/directmessages', 'r')
            return pickle.load(f)

        def SetXTwitterHeaders(a,b,c):
            pass

        def VerifyCredentials():
            return True
