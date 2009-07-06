from django.db import models
import re
from google.appengine.ext import db

class PageManager(models.Manager):
    def create_with_auto_version(self, slug, headline, content, change_message, change_ip, minor_edit):
        """
        Creates and returns a Page object with the given attributes.
        Automatically sets version to the next available version number for
        the given slug, in a way that avoids race conditions.
        """
        try:
            latest_page = Page.objects.order_by('-version').filter('slug =', slug)[0]
            version = latest_page.version + 1
        except IndexError:
            version = 1
        s = Page.get_or_insert("page%s%s" % (slug, version), slug=slug, headline=headline, content=content, change_message=change_message,
        	change_ip=change_ip, minor_edit=minor_edit, version=version)
        s.put()        
        return s

    def order_by(self, sort_order):
    	return db.Query(Page).order(sort_order)

class Page(db.Model):
    slug = db.StringProperty()
    headline = db.StringProperty()
    content = db.TextProperty()
    version = db.IntegerProperty()
    change_date = db.DateTimeProperty(auto_now_add=True)
    change_message = db.StringProperty()
    change_user = db.UserProperty(auto_current_user_add=True)
    change_ip = db.StringProperty()
    minor_edit = db.BooleanProperty()
    objects = PageManager()

    def __unicode__(self):
        return self.slug

    def url(self):
        return '/%s/' % self.slug

    def edit_url(self):
        return '/%s/edit/' % self.slug

    def history_url(self):
        return '/%s/history/' % self.slug

    def version_url(self):
        return '/%s/history/%s/' % (self.slug, self.version)

    def diff_url(self):
        return '/%s/history/%s/diff/' % (self.slug, self.version)
