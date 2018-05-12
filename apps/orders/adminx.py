import xadmin

from xadmin import views

from .models import Order, DeliveryOrder


class OrderAdmin(object):
    list_display = ['id', 'user', 'status', 'add_time']  # 展示的内容
    search_fields = ['user', 'status']  # 搜索时按以上字段搜索
    list_filter = ['status', 'add_time', 'total_price']  # 筛选器内容
    readonly_fields = ['id', 'user', 'status', 'total_price', 'add_time']


class DeliveryOrderAdmin(object):
    list_display = ['id', 'order', 'status', 'commodity', 'tracking']  # 展示的内容
    search_fields = ['status', 'commodity__name']  # 搜索时按以上字段搜索
    list_filter = ['status', 'add_time','order__status']  # 筛选器内容
    readonly_fields = ['id', 'order', 'commodity', 'address', 'nums', 'add_time']  # 只读
    ordering = ['add_time']  # 排序
    list_editable = ['status', 'tracking']  # 列表页编辑


xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(DeliveryOrder, DeliveryOrderAdmin)


class GlobalSettings(object):
    # 修改title
    site_title = '烟海书店后台管理'
    # 修改footer
    site_footer = 'YanHaiBookStore'
    # 收起菜单
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSettings)
