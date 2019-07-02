from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin.layout import *
from user.models import BookUser,BookBeanCredit,BookBeanCreditStatistics,BrowHistory,Address,Citys
from bookapp.models import Books,BorrowBook,UserBookComment,BookClasses

from django.utils.translation import ugettext_lazy as _, ugettext

class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True

xadmin.site.register(UserSettings, UserSettingsAdmin)

class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), 
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''
    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'

xadmin.site.register(Log, LogAdmin)

# xadmin增加主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(xadmin.views.BaseAdminView,BaseSetting)


class GlobalSetting(object):
    site_title = '书香盈袖后台管理系统'
    site_footer = 'http://www.jgzhen.com'
    # 菜单伸缩
    menu_style = 'accordion'
xadmin.site.register(xadmin.views.CommAdminView,GlobalSetting)


class BookUserSetting(object):
    list_display = ('user','sex','age')

xadmin.site.register(BookUser,BookUserSetting)

class BookBeanCreditSetting(object):
    list_display = ('user','grade','number')
xadmin.site.register(BookBeanCredit,BookBeanCreditSetting)

class BookBeanCreditStatisticsSetting(object):
    list_display = ('user','borrow_book','add_number','sub_number')
xadmin.site.register(BookBeanCreditStatistics,BookBeanCreditStatisticsSetting)

class BooksSetting(object):
    list_display = ('book_name','all_number_book','surplus_number_book')
xadmin.site.register(Books,BooksSetting)

class BorrowBookSetting(object):
    list_display = ('user','book','start_time','end_time','is_exceed_time')
xadmin.site.register(BorrowBook,BorrowBookSetting)

class UserBookCommentSetting(object):
    list_display = ('user','book')
xadmin.site.register(UserBookComment,UserBookCommentSetting)

class BookClassesSetting(object):
    list_display = ('class_name',)
xadmin.site.register(BookClasses,BookClassesSetting)

class BrowHistorySetting(object):
    list_display = ('user','book','time')
xadmin.site.register(BrowHistory,BrowHistorySetting)

class AddressSetting(object):
    list_display = ('user','consignee','phone')
xadmin.site.register(Address,AddressSetting)

class CitysSetting(object):
    list_display = ('name','level')
xadmin.site.register(Citys,CitysSetting)
