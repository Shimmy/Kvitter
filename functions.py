import os, base64, re, hashlib
import Image, gtk, pango
import StringIO, urllib
import timesince, time, cgi
import webbrowser

def open_url(menuitem, url):
    webbrowser.open(url)

def updateTimeLineListStore(statuses, liststore):
    liststore.clear()
    for status in statuses:
        im, ext = fetchImageFromUrl(status.user.profile_image_url)
        pixbuf = Image_to_GdkPixbuf(im)
        time_ago = timesince.timesince(time.strptime(status.created_at.replace('+0000 ','') ,"%a %b %d %H:%M:%S %Y"))

        row = liststore.append()
        liststore.set_value (row, 0, pixbuf)
        liststore.set_value (row, 1, '<span size="small"><b>%s</b> (%s)\n%s\n</span><span size="x-small">%s ago</span>' % (status.user.screen_name, cgi.escape(status.user.name), cgi.escape(status.text), time_ago))
        liststore.set_value (row, 2, status.user.screen_name)            
        liststore.set_value (row, 3, status.created_at)            
        liststore.set_value (row, 4, status.source)  

def resize_wrap(scroll, allocation, treeview, column, cell):
       cell.set_property('wrap-width', allocation.width-100)
       cell.set_property('wrap-mode', pango.WRAP_WORD)

def get_ext(url):
    urls = os.path.splitext(url)
    ext = urls[-1]
    extnodot = re.findall('\.(\w{3,4})', ext)
    if extnodot[0]:
        return extnodot[0]
    else:
        return 'jpg'


def fetchImageFromUrl(url):
    try:
        #url = "http://api.iglaset.se/resizely/round/5/?url=%s" % url
        ext = get_ext(url)
        source = base64.urlsafe_b64encode(hashlib.sha224(url).hexdigest())
        dest = "%s%s" % ('/tmp/kvitter/', source)
        if not os.path.exists(dest):
            datasource = urllib.urlopen(url)
            im = datasource.read()   
            datasource.close() 

            f = open(dest, 'w')
            f.write(im)
            f.close()     
        im = Image.open(dest)

    except Exception as e:
        print "error %s" % url
        im = Image.open('img/avatar.gif')
        ext = 'gif'
    return (im, ext)

def Image_to_GdkPixbuf (image):
    file = StringIO.StringIO ()
    if image.mode != "RGB":
        image = image.convert("RGBA")
    image.save (file, 'ppm')
    contents = file.getvalue()
    file.close ()
    loader = gtk.gdk.PixbufLoader ()
    loader.write (contents, len (contents))
    pixbuf = loader.get_pixbuf ()
    loader.close ()
    return pixbuf
