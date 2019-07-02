# 定时任务
from bookapp.models import Books,BorrowBook
from user.models import BookUser,BookBeanCredit,MyInformation
from django.contrib.auth.models import User
import datetime


# 定时查询书本状态是否超期
def book_state():
    borrow_books = BorrowBook.objects.filter(is_active=True,is_give_back=False)
    # 定时查询书本状态是否超期
    for borrow_book in borrow_books:
        now_date = str(datetime.date.today())
        end_date = str(borrow_book.end_time)
        now_time = datetime.datetime.strptime(now_date, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # 如果结束时间小于当前日期，那么判定为超期
        if end_time < now_time:
            borrow_book.is_exceed_time = True
            borrow_book.save()
            # 如果未还书
            if not borrow_book.is_give_back:
                book_bean_credit = BookBeanCredit.objects.filter(user=BookUser.objects.get(user=borrow_book.user),
                                                             is_active=True).first()
                # 判断逾期时间，1天扣1分，10天扣10分
                book_bean_credit.number -= 1
                book_bean_credit.save()





# 定期刷新书香豆信用
# 初步设计：0-99信用：1级会员 借书数量：5  最大时长：30
#          100-149信用：2级会员 借书数量：10 最大时长：40
#          150-199信用：3级会员 借书数量：15 最大时长：50
def book_bean_credit_state():
    book_bean_credits = BookBeanCredit.objects.filter(is_active=True)
    for book_bean_credit in book_bean_credits:
        times = book_bean_credit.number // 50
        book_bean_credit.grade = str(times)+ '级会员'
        book_bean_credit.borrow_all = times*5
        book_bean_credit.borrow_max_time = (times-1)*10+30
        book_bean_credit.save()

# 消息生成
def information_create():
    borrow_books = BorrowBook.objects.filter(is_give_back=False,is_active=True)
    # 定时查询书本状态是否超期
    for borrow_book in borrow_books:
        now_date = str(datetime.date.today())
        end_date = str(borrow_book.end_time)
        now_time = datetime.datetime.strptime(now_date, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # 如果结束时间-当前时间小于5天，那么开始生成消息
        if int((end_time-now_time).days) <= 5:
            my_information = MyInformation(user=borrow_book.user,is_dispose=False,is_active=True)
            if int((end_time-now_time).days) < 0:
                my_information.content = '您的《'+str(borrow_book.book.book_name)+\
                                     "》已超期，为影响您的信用，请及时还书！！"
            else:
                my_information.content = '您的《' + str(borrow_book.book.book_name) + \
                                         "》再有" + str((end_time - now_time).days) + \
                                         "天就要到期了，请及时还书！！"
            my_information.save()