from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^get_code/$',views.get_code,name='get_code'),
    url(r'^login/',views.Login.as_view(),name='login'),
    url(r'^register/', views.Register.as_view(), name='register'),
    url(r'^logout/',views.logout,name='logout'),


    # 收货地址 省级
    url(r'^area1/$', views.getArea1, name='area1'),
    # 收货地址 市级/县、区级
    url(r'^area2/(?P<pid>\d+)/$', views.getArea2, name='area2'),

]