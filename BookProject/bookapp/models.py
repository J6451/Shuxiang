from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.

# 书籍信息
class Books(models.Model):
    # 图书名字
    book_name = models.CharField('图书名字',max_length=500)
    # 作者
    author = models.CharField('作者',blank=True,null=True,max_length=500)
    # 出版社
    press = models.CharField('出版社',blank=True,null=True,max_length=100)
    #出版日期
    press_time = models.CharField('出版日期',blank=True,null=True,max_length=100)
    # 价格（书香豆）
    price = models.IntegerField('价格（书香豆）',default=20,blank=True,null=True)
    # 书本总数量
    all_number_book = models.IntegerField('书本总数量',default=30,blank=True,null=True)
    # 剩余数量
    surplus_number_book = models.IntegerField('剩余数量',default=30,blank=True,null=True)
    # 查看次数
    check_number = models.IntegerField('查看次数',default=0,blank=True,null=True)
    # 借阅次数
    borrow_number = models.IntegerField('借阅次数',default=0,blank=True,null=True)
    # 在线阅读次数
    booking_number = models.IntegerField('在线阅读次数',default=0,blank=True,null=True)
    # 所需信用值
    credit_value = models.IntegerField('所需信用值',default=100,blank=True,null=True)
    # 简介
    intro = models.TextField('简介',blank=True,null=True)
    # 图书图片
    image = models.ImageField('图片',upload_to='photo',blank=True,null=True,default='photo/default.jpg')
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = '书籍'

    def __str__(self):
        return self.book_name

# 图书类别表
class BookClasses(models.Model):
    """
    思路：通过class_two_id 来查询分类，
    如果是一级类别，那么class_two_id 写0
    如果是二级类别，那么class_two_id 写父id
    """
    class_name = models.CharField('类别',max_length=20)
    # 二级分类id
    class_two_id = models.IntegerField('二级id')
    book = models.ManyToManyField(Books,related_name='book_class')
    # 状态
    is_active = models.BooleanField('状态', default=True)

    class Meta:
        verbose_name = '图书类别'
        verbose_name_plural = '图书类别'

    def __str__(self):
        return self.class_name

# 借阅书籍信息
class BorrowBook(models.Model):
    # 用户
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='borrow_user')
    # 图书
    book = models.ForeignKey(Books,on_delete=models.CASCADE,related_name='borrow_book')
    # 收货地址
    address = models.CharField('收货地址id',max_length=20,default=1)
    # 借书起始时间
    start_time = models.DateField('起始时间',default=datetime.date.today)
    # 借书结束时间
    end_time = models.DateField('结束时间')
    # 时长
    borrow_time = models.IntegerField('时长',blank=True,null=True)
    # 是否归还 True：归还 False：未归还
    is_give_back = models.BooleanField('是否归还',default=False)
    # 是否超期
    is_exceed_time = models.BooleanField('是否超期',default=False)
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '借阅书籍信息'
        verbose_name_plural = '借阅书籍信息'

    def __str__(self):
        return self.book.book_name


# 评论
class UserBookComment(models.Model):
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_user')
    # 图书
    book = models.ForeignKey(Books, on_delete=models.CASCADE,related_name='comment_book')
    # 时间
    comment_time = models.DateTimeField('评论时间',default=timezone.now)
    # 评论
    comment = models.TextField('评论')
    # 状态
    is_active = models.BooleanField('状态',default=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.user.username
