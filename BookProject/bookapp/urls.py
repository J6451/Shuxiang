from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/',views.index.as_view(),name='index'),
    url(r'^$', views.index.as_view(),),
    # 搜索图书
    url(r'^search_book/',views.search_book,name='search_book'),
    # 通过类别查询
    url(r'^class_book_search/(?P<class_id>\d+)/',views.class_book_search,name='class_book_search'),
    # 特价书
    url(r'^special_price/$',views.special_price,name='special_price'),
    # 新上架
    url(r'^new_books/$',views.new_books,name='new_books'),
    # 出版社浏览
    url(r'^press_books/$',views.press_books,name='press_books'),
    # 对应出版社所有书籍
    url(r'^press_detail_books/(?P<press_id>\d+)/$', views.press_detail_books, name='press_detail_books'),
    # 限时免费
    url(r'^free_books/$',views.free_books,name='free_books'),
    # 充值
    url(r'^recharge/$',views.recharge,name='recharge'),
    # 详情
    url(r'^detail/(?P<book_id>\d+)/', views.book_detail, name='detail'),
    # 借阅
    url(r'^book_borrow/(?P<book_id>\d+)/',views.book_borrow,name='book_borrow'),
    # 还书
    url(r'^return_book/(?P<borrow_id>\d+)/', views.return_book, name='return_book'),
    # 评论
    url(r'^book_comment/(?P<book_id>\d+)/',views.book_comment,name='book_comment'),
    # 订单成功页
    url(r'^book_borrow_success/',views.book_borrow_success,name='book_borrow_success'),
    # 会员中心-我的订单
    url(r'^mem_center/',views.member_center,name='member_center'),
    # 我的订单，查询
    url(r'^order_search/',views.order_search,name='order_search'),
    # 会员中心-收货地址
    url(r'^mem_address/$',views.member_address.as_view(),name='member_address'),
    # 收货地址删除
    url(r'^address_drop/(?P<pid>\d+)/$',views.address_drop,name='address_drop'),
    # 会员中心-个人资料
    url(r'^person_data/',views.member_personal_data,name='personal_data'),
    # 会员中心-修改密码
    url(r'^mem_change_password/',views.member_change_password,name='member_change_password'),
    # 发送邮件
    url(r'^send_email/',views.send_email,name='send_email'),
    # 邮件验证码验证
    url(r'^old_password_verify/',views.old_password_verify,name='old_password_verify'),
    # 会员中心-浏览历史
    url(r'^mem_history/',views.member_brow_history,name='member_brow_history'),
    # 会员中心-个性分析
    url(r'^mem_personality_analysis/',views.member_personality_analysis,name='member_personality_analysis'),
    # 会员中心-为我推荐
    url(r'^member_recommend_for_me/',views.member_recommend_for_me,name='member_recommend_for_me'),
    # 会员中心-我的评论
    url(r'^mem_comment/',views.member_comment,name='member_comment'),
    # 会员中心-我的消息
    url(r'^mem_information/',views.member_information,name='member_information'),
    # 会员中心-我的消息-处理
    url(r'^mem_information_dispose/(?P<pid>\d+)/$',views.information_dispose,name='information_dispose'),

]