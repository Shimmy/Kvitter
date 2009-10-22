import gtk, pango
import functions, re

from kvitter_thread import KvitterThread

class MainWindow:
    def __init__(self):
        # Read the gui xml
        self.wMain = gtk.glade.XML('gui/kvitter.glade')

        # Get widgets
        self.mainWindow = self.wMain.get_widget("MainWindow")
        self.updateStatusButton = self.wMain.get_widget("UpdateStatus_Button")
        self.statusEntry = self.wMain.get_widget("Status_Entry")
        self.timelineNoteBook = self.wMain.get_widget("notebook1")
        self.scrolledWindow = self.wMain.get_widget("scrolledwindow1")
        self.statusBar = self.wMain.get_widget("statusbar")

        # Private timeline
        self.privTimeLineTreeView = self.wMain.get_widget("PrivateTimeLine_TreeView")
        self.privTimeLineListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, str)
        self.initTimeLineTreeViewHelper(self.privTimeLineTreeView, self.privTimeLineListStore)

        # Public timeline
        self.pubTimeLineTreeView = self.wMain.get_widget("PublicTimeLine_TreeView")
        self.pubTimeLineListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, str)
        self.initTimeLineTreeViewHelper(self.pubTimeLineTreeView, self.pubTimeLineListStore)

        # Show window
        self.mainWindow.set_property('visible', True)  
        self.connectCallbacks()


    """ All callbacks are connected here 
    """
    def connectCallbacks(self):
        self.mainWindow.connect('destroy', gtk.main_quit)
        self.updateStatusButton.connect('clicked', self.updateStatus_Clicked)
        self.statusEntry.connect('activate', self.updateStatusEntry_Activate)
        self.wMain.get_widget("imagemenuitem_quit").connect('activate', gtk.main_quit)
        self.wMain.get_widget("imagemenuitem_refresh").connect('activate', self.refresh_Activate)


    """ Helper to set timeline treeview properties 
    """
    def initTimeLineTreeViewHelper(self, treeview, liststore):
        textrenderer = gtk.CellRendererText()
        imgrenderer = gtk.CellRendererPixbuf()
        textrenderer.set_fixed_height_from_font(4)
        textrenderer.set_property('yalign', 0.2)
        textrenderer.set_property('width',50)
        imgrenderer.set_property('yalign', 0.2)
        profile_pic_col = gtk.TreeViewColumn('', imgrenderer, pixbuf=0)
        status_col = gtk.TreeViewColumn('', textrenderer, markup=1 )

        treeview.append_column(profile_pic_col)
        treeview.append_column(status_col)
        treeview.set_model(liststore)
        self.scrolledWindow.connect_after('size-allocate', functions.resize_wrap, treeview, status_col, textrenderer)
        treeview.connect('button-release-event', self.timeline_Clicked)

    """ Callbacks """
    def updateStatus_Clicked(self, widget):
        message = self.statusEntry.get_text()
        status = self.api.PostUpdate(message)
        self.statusEntry.set_text("")
        self.refresh_Activate(widget)

    def updateStatusEntry_Activate(self, widget):
        self.updateStatus_Clicked(widget)
    
    def refresh_Activate(self, widget):
        kt = KvitterThread()
        kt.setTwitterUser('SineX')
        if self.timelineNoteBook.get_current_page() == 0:
            kt.setFunction(self.api.GetFriendsTimeline, "GetFriendsTimeline")
            kt.setCallback(functions.updateTimeLineListStore, self.privTimeLineListStore)
        elif self.timelineNoteBook.get_current_page() == 1:
            kt.setFunction(self.api.GetPublicTimeline, "GetPublicTimeline")
            kt.setCallback(functions.updateTimeLineListStore, self.pubTimeLineListStore)
        kt.start()

    def timeline_Clicked(self, widget, event):
        if event.button == 3: #Right click
            liststore, ite = widget.get_selection().get_selected()
            nickname = liststore.get_value(ite,2)
            status_msg = liststore.get_value(ite,1)

            urlpattern = re.compile('(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?')
            urls = urlpattern.findall(status_msg)

            pop = gtk.Menu()
            menuPopupReply = gtk.MenuItem ("Reply")

            pop.add(menuPopupReply)

            for url in urls:
                menuPopupUrl = gtk.MenuItem(url)
                pop.add(menuPopupUrl)
                menuPopupUrl.connect('activate', functions.open_url, url)
            pop.show_all()
            menuPopupReply.connect('activate', self.reply, nickname)
            pop.popup(None, None, None, 1, 0)

    def reply(self, menuitem, who):
        # Workaround for not selecting text when focus on entry
        self.statusEntry.grab_focus()
        self.statusEntry.set_text("@%s: " % who)
        self.statusEntry.set_position(len(who)+3)

    def show(self, api):
        self.api = api


    
