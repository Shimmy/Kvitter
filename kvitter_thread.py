import threading
import gtk
import pickle

class KvitterThread(threading.Thread):
    stopthread = threading.Event()
    def setFunction(self, function, fn_str):
        self.function = function
        self.fn_str = fn_str

    def setCallback(self, callback, liststore):
        self.callback = callback
        self.liststore = liststore
    
    def setTwitterUser(self, username):
        self.twitterUser = username

    def run(self):
        gtk.gdk.threads_enter()
        if self.fn_str == "GetFriendsTimeline":
            statuses = self.function(self.twitterUser, 100)
        if self.fn_str == "GetPublicTimeline":
            statuses = self.function(100)
        if self.fn_str == "GetDirectMessages":
            statuses = self.function(self.twitterUser, 100)
        self.callback(statuses, self.liststore)

        gtk.gdk.threads_leave()
