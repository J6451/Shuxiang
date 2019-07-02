from django.db import models
from django.contrib.auth.models import User
from bookapp.models import BorrowBook,Books
from django.utils import timezone
# Create your models here.

# 用户表
class BookUser(models.Model):
    # django内置用户表
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    # 1:男 0:女
    sex = models.CharField('性别',default='1',blank=True,null=True,max_length=1)
    # 年龄
    age = models.IntegerField('年龄',default=18,blank=True,null=True)
    # 手机号
    phone = models.CharField('手机号',default='12345678901',blank=True,null=True,max_length=20)
    # 手机号是否激活
    is_phone = models.BooleanField('手机号激活',default=False)
    # 邮箱是否激活
    is_email = models.BooleanField('邮箱激活',default=False)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.user.username

# 收货地址表
class Address(models.Model):
    # 关联用户
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_address')
    # 收货人
    consignee = models.CharField('收货人',max_length=60)
    # 手机号
    phone = models.CharField('手机号',max_length=20)
    # 省
    province = models.CharField('省',max_length=50)
    # 市
    city = models.CharField('市',max_length=50)
    # 县或区
    country = models.CharField('县',max_length=50)
    # 街道
    street = models.CharField('街道',max_length=50)
    # 补充
    detail_address = models.CharField('详细地址',max_length=100)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'

    def __str__(self):
        return self.user.username


#暂定加总书豆字段，通过充值增加书豆数量


# 书香豆信用表
class BookBeanCredit(models.Model):
    user = models.OneToOneField(BookUser,on_delete=models.CASCADE,primary_key=True)
    # 等级
    grade = models.CharField('等级',default='1级会员',blank=True,null=True,max_length=20)
    # 金额（书香豆）
    money = models.IntegerField('书香豆数量',default=0,blank=True,null=True)
    # 信用值
    number = models.IntegerField('信用值',default=80,blank=True,null=True)
    # 可借书本总量
    borrow_all = models.IntegerField('可借书本总量',default=5,blank=True,null=True)
    # 已借书本数量
    borrowed = models.IntegerField('已借书本数量',default=0,blank=True,null=True)
    # 可借书本最大时长(天)
    borrow_max_time = models.IntegerField('可借书本最大时长',default=30,blank=True,null=True)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '书香豆信用'
        verbose_name_plural = '书香豆信用'

    def __str__(self):
        return self.user.user.username

# 书香豆信用统计表
class BookBeanCreditStatistics(models.Model):
    # 用户
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='statistics_user')
    # 借书表外键
    borrow_book = models.ForeignKey(BorrowBook,on_delete=models.CASCADE,related_name='statistics_borrow_book')
    # 加分数量
    add_number = models.IntegerField('加分数量',default=0,blank=True,null=True)
    # 减分数量
    sub_number = models.IntegerField('减分数量',default=0,blank=True,null=True)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '书香豆信用统计'
        verbose_name_plural = '书香豆信用统计'

    def __str__(self):
        return self.user.username


# 浏览历史
class BrowHistory(models.Model):
    # 用户
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='brow_history_user')
    # 图书
    book = models.ForeignKey(Books,on_delete=models.CASCADE,related_name='brow_history_book')
    # 时间
    time = models.DateTimeField('浏览时间',default=timezone.now)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '浏览历史'
        verbose_name_plural = '浏览历史'

    def __str__(self):
        return self.user.username


# 城市
class Citys(models.Model):
    # 城市名
    name = models.CharField('城市名',max_length=100)
    # 城市等级
    level = models.IntegerField('城市等级')
    # 父级城市
    parent = models.ForeignKey('Citys',on_delete=models.CASCADE,null=True)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = '城市'

    def __str__(self):
        return self.name


# 我的消息
class MyInformation(models.Model):
    # 备用字段
    standby = models.CharField('备用字段',max_length=200,null=True,blank=True)
    # 消息内容
    content = models.TextField('消息内容')
    # 时间
    time = models.DateTimeField('通知时间',default=timezone.now)
    # 用户id
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='information_user',default=1)
    # 是否处理
    is_dispose = models.BooleanField('是否处理',default=False)
    # 状态
    is_active = models.BooleanField('状态',default=True)


