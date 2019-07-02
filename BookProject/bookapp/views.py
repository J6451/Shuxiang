from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import View
from user.help import login_required,press_shift,jieba_obsoletism_word,random_str
import pymysql
from bookapp.models import Books,BorrowBook,UserBookComment,BookClasses
from user.models import Citys,Address,BrowHistory,BookBeanCredit,BookUser,MyInformation
from django.utils.decorators import method_decorator
import time,datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout as user_logout
import jieba
from collections import Counter
from BookProject import settings
from django.core.mail import send_mail
# 将图书加入到数据库，
# try:
#     Books.objects.get(id=1)
# except:
#     db = pymysql.connect('localhost','root','123456','book',charset='utf8')
#     cursor = db.cursor()
#     cursor.execute("select book_title,book_author,book_press,book_publication_date,book_img,book_intro_text from books_all ")
#     for i in cursor.fetchall():
#         book = Books(book_name=i[0],author=i[1],press=i[2],press_time=i[3],image=i[4],intro=i[5])
#         book.save()


# 主页
class index(View):
    # @login_required
    def get(self,request):
        if str(request.user) != 'AnonymousUser':
            information_len = information_amount(request)
        else:
            information_len = 0
        # 特价书
        sale_books = Books.objects.filter()[0:5]
        # 男士推荐
        man_books = Books.objects.filter()[10:15]
        # 女士推荐
        lady_books = Books.objects.filter()[20:25]

        return render(request,'bookapp/index.html',locals())


# 分类查询
def class_book_search(request,class_id):
    # book_class = BookClasses.objects.get(id=class_id)
    # print(book_class[0])
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    class_info = BookClasses.objects.get(id=class_id)
    class_name = class_info.class_name
    class_books = class_info.book.all()
    # print(11111,special_books.book.all())
    paginator = Paginator(class_books, 9)
    page = request.GET.get('page', 1)
    class_books = paginator.page(page)

    return render(request,'bookapp/class_books_search.html',{'class_name':class_name,'class_books':class_books,'information_len':information_len})


# 特价书
def special_price(request):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0


    # 查找价格小于等于20书豆的书
    special_books = Books.objects.filter(price__lt=20,price__gt=0)

    paginator = Paginator(special_books,9)
    page = request.GET.get('page',1)
    special_books = paginator.page(page)
    return render(request,'bookapp/tejia.html',{'special_books':special_books,'information_len':information_len})

# 新上架
def new_books(request):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    new_books = Books.objects.filter(press_time__contains='2019')
    paginator = Paginator(new_books, 9)
    page = request.GET.get('page', 1)
    new_books = paginator.page(page)
    return render(request,'bookapp/new_books.html',{'new_books':new_books,'information_len':information_len})

# 出版社浏览
def press_books(request):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    return render(request,'bookapp/press_books.html',{'information_len':information_len})

# 查询对应id的出版社所有书籍
def press_detail_books(request,press_id):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    press_name = press_shift(press_id)
    # print(11111,press_name)
    press_books = Books.objects.filter(press__contains=press_name)
    paginator = Paginator(press_books, 9)
    page = request.GET.get('page', 1)
    press_books = paginator.page(page)
    return render(request,'bookapp/press_detail_books.html',{'press_books':press_books,'information_len':information_len})

# 限时免费
def free_books(request):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    free_books = Books.objects.filter(price=0)
    paginator = Paginator(free_books, 9)
    page = request.GET.get('page', 1)
    free_books = paginator.page(page)
    return render(request,'bookapp/free_books.html',{'free_books':free_books,'information_len':information_len})

# 充值
def recharge(request):
    success = ''
    if request.method == 'POST':
        money = request.POST.get('money',0)
        book_bean_credit = BookBeanCredit.objects.filter(user=BookUser.objects.get(user=request.user),is_active=True).first()
        # 增加余额
        book_bean_credit.money += int(money)*10
        # 增加信用值
        book_bean_credit.number += int(money)
        book_bean_credit.save()
        success = '充值成功'
    return render(request,'bookapp/recharge.html',{"success":success})




# 搜索
def search_book(request):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    content = request.GET.get('content')
    # print(content)
    search_books = Books.objects.filter(Q(book_name__icontains=content)|Q(author__icontains=content))
    # print(search_books)
    paginator = Paginator(search_books, 9)
    page = request.GET.get('page', 1)
    search_books = paginator.page(page)
    return render(request,'bookapp/search_book.html',{'search_books':search_books,'information_len':information_len,'content':content})


# 书籍详细页
def book_detail(request,book_id):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    book = Books.objects.get(id=book_id)
    # 查看一次，将书籍的查看次数加1
    book.check_number += 1
    book.save()
    # 查看一次，如果当前用户存在，则添加到浏览历史中去
    try:
        if request.user.id:
            brow_history = BrowHistory(user=request.user,book=book)
            brow_history.save()
        else:
            pass
    except:
        pass

    return render(request,'bookapp/xiangxi_xiu.html',{"book":book,'information_len':information_len})

# 书籍借阅页
@login_required
def book_borrow(request,book_id):
    book = Books.objects.get(id=book_id)
    error = ''
    if request.method == 'POST':
        # 地址id
        address_id = request.POST.get('address_id')
        # 开始日期
        start_date = request.POST.get('start_date')
        # 结束日期
        end_date = request.POST.get('end_date')

        start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # 时长
        diff_days = int((end_time - start_time).days)
        book_bean_credit = BookBeanCredit.objects.filter(user=BookUser.objects.get(user=request.user),is_active=True).first()
        # 判断可借书本总量与已借书本数量的差
        if book_bean_credit.borrow_all - book_bean_credit.borrowed >= 1:
            # 判断该用户剩余书香豆-该书需要的书香豆 是否大于0
            if book_bean_credit.money - book.price >= 0:
                # 判断书籍剩余书本数量
                if book.surplus_number_book > 0:
                    # 判断信用值
                    if book_bean_credit.number >= 50:
                        borrow_book = BorrowBook(user=request.user,book=book,
                                             address=address_id,start_time=start_date,
                                             end_time=end_date,borrow_time=diff_days)

                        borrow_book.save()
                        # 将已借书本数量+1
                        book_bean_credit.borrowed += 1
                        # 当前余额减去商品价格
                        book_bean_credit.money -= book.price
                        book_bean_credit.save()
                        # 将书本剩余数量-1
                        book.surplus_number_book -= 1
                        # 将书本借阅次数+1
                        book.borrow_number += 1
                        book.save()
                        return redirect(reverse('bookapp:book_borrow_success'))
                    else:
                        error = '抱歉，信用不足！！'
                else:
                    error = '抱歉，库存不足！！'
            else:
                error = '抱歉，书香豆金额不足！！<a href="/bookapp/recharge/" id="recharge">前往充值</a>'
        else:
            error = '抱歉，您所借的书数量超过您当前所能借的最大数量！！'

    user_addresses = Address.objects.filter(user=request.user, is_active=True)
    borrow_max_time = BookBeanCredit.objects.filter(user=BookUser.objects.get(user=request.user),is_active=True).first().borrow_max_time
    return render(request,'bookapp/tijiao.html',{'book':book,'user_addresses':user_addresses,'borrow_max_time':borrow_max_time,'error':error})


# 订单成功页
@login_required
def book_borrow_success(request):
    return render(request,'bookapp/chenggong.html')


# 评论
def book_comment(request,book_id):
    if str(request.user) != 'AnonymousUser':
        information_len = information_amount(request)
    else:
        information_len = 0

    book = Books.objects.get(id=book_id)
    user = str(request.user)
    user_book_comments = UserBookComment.objects.filter(book=book,is_active=True).order_by('-comment_time')
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user_book_comment = UserBookComment(user=request.user,book=book,comment=comment)
        user_book_comment.save()
        return redirect(reverse('bookapp:book_comment',kwargs={"book_id":book_id}))
    return render(request, 'bookapp/comment.html',{'user':user,"book":book,'user_book_comments':user_book_comments,'information_len':information_len})



# 查询所有订单详情
def all_borrow_books(aa):
    borrow_books = BorrowBook.objects.filter(user=aa.user, is_active=True).order_by('-start_time')
    borrow_book_list = []
    for i in borrow_books:
        borrow_book = {}
        borrow_book['id'] = i.id
        borrow_book['book_id'] = i.book.id
        borrow_book['book_image'] = i.book.image
        borrow_book['consignee'] = Address.objects.get(id=i.address).consignee
        borrow_book['book_price'] = i.book.price
        borrow_book['start_time'] = i.start_time
        borrow_book['end_time'] = i.end_time
        # 是否归还
        borrow_book['is_give_back'] = i.is_give_back
        # 是否超期
        borrow_book['is_exceed_time'] = i.is_exceed_time
        # borrow_book[''] = ''
        borrow_book_list.append(borrow_book)
    # 订单数量
    book_amount = len(borrow_book_list)
    return borrow_book_list,book_amount

# 查询满足条件订单详情
def condition_borrow_books(borrow_books):
    borrow_book_list = []
    for i in borrow_books:
        borrow_book = {}
        borrow_book['id'] = i.id
        borrow_book['book_id'] = i.book.id
        borrow_book['book_image'] = i.book.image
        borrow_book['consignee'] = Address.objects.get(id=i.address).consignee
        borrow_book['book_price'] = i.book.price
        borrow_book['start_time'] = i.start_time
        borrow_book['end_time'] = i.end_time
        # 是否归还
        borrow_book['is_give_back'] = i.is_give_back
        # 是否超期
        borrow_book['is_exceed_time'] = i.is_exceed_time
        # borrow_book[''] = ''
        borrow_book_list.append(borrow_book)
    # 订单数量
    book_amount = len(borrow_book_list)
    return borrow_book_list,book_amount


# 会员中心（主页）我的订单
@login_required
def member_center(request):
    borrow_book_list,book_amount = all_borrow_books(request)
    information_len = information_amount(request)

    paginator = Paginator(borrow_book_list, 5)
    page = request.GET.get('page', 1)
    borrow_book_list = paginator.page(page)
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'huiyuan/huiyuan.html',{'borrow_book_list':borrow_book_list,'book_amount':book_amount,'addresses':addresses,'information_len':information_len})

# 订单查询
@login_required
def order_search(request):
    days = request.GET.get('datetime')
    address = request.GET.get('address')
    order_status = request.GET.get('order_status')
    order_status_list = []
    for i in order_status:
        if i == '0':
            order_status_list.append(False)
        else:
            order_status_list.append(True)
    # print(order_status_list)
    date_time = datetime.date.today() - datetime.timedelta(days=int(days))
    if days != '0':
        if order_status != '0':
            if address != '0':
                borrow_books = BorrowBook.objects.filter(start_time__gte=date_time,user=request.user,address=address,is_give_back=order_status_list[0],is_exceed_time=order_status_list[1], is_active=True)
            else:
                borrow_books = BorrowBook.objects.filter(start_time__gte=date_time,user=request.user,is_give_back=order_status_list[0],is_exceed_time=order_status_list[1], is_active=True)
        else:
            if address != '0':
                borrow_books = BorrowBook.objects.filter(start_time__gte=date_time,user=request.user,address=address, is_active=True)
            else:
                borrow_books = BorrowBook.objects.filter(start_time__gte=date_time,user=request.user, is_active=True)
    else:
        if order_status != '0':
            if address != '0':
                borrow_books = BorrowBook.objects.filter(user=request.user, address=address,
                                                         is_give_back=order_status_list[0],
                                                         is_exceed_time=order_status_list[1], is_active=True)
            else:
                borrow_books = BorrowBook.objects.filter(user=request.user, is_give_back=order_status_list[0],
                                                         is_exceed_time=order_status_list[1], is_active=True)
        else:
            if address != '0':
                borrow_books = BorrowBook.objects.filter(user=request.user, address=address, is_active=True)
            else:
                borrow_books = BorrowBook.objects.filter(user=request.user, is_active=True)

    borrow_book_list,book_amount = condition_borrow_books(borrow_books)

    paginator = Paginator(borrow_book_list, 5)
    page = request.GET.get('page', 1)
    borrow_book_list = paginator.page(page)
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'huiyuan/huiyuan_order_search.html',{'borrow_book_list':borrow_book_list,'book_amount':book_amount,'addresses':addresses})



# 还书
def return_book(request,borrow_id):

    borrow_book = BorrowBook.objects.get(id=borrow_id)
    book = Books.objects.get(id=borrow_book.book.id)
    # 将剩余数量+1
    book.surplus_number_book += 1
    book.save()
    # 是否归还改为True
    borrow_book.is_give_back = True

    book_bean_credit = BookBeanCredit.objects.filter(user=BookUser.objects.get(user=request.user),
                                                     is_active=True).first()
    # 信用表中已借书本数量-1
    book_bean_credit.borrowed -= 1

    # 注意：这段超期保存应写在定期任务中，此处先在还书中进行判断。
    # 如果结束时间小于当前日期，那么判定为超期，超期还书不返还部分书香豆
    now_date = str(datetime.date.today())
    end_date = str(borrow_book.end_time)
    now_time = datetime.datetime.strptime(now_date, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if end_time < now_time:
        # 注意：保存应写在定期任务中
        borrow_book.is_exceed_time = True
        # 注意：下面这行代码不需要写在定期任务中
    else:
        # 未超期还书，即为正常还书，返还部分书香豆
        book_bean_credit.money += 10
        # 未超期还书，即为正常还书，提升信用值
        book_bean_credit.number += 1

    borrow_book.save()
    book_bean_credit.save()

    return redirect(reverse('bookapp:member_center'))

# 会员中心-收货地址
@method_decorator(login_required,name='dispatch')
class member_address(View):
    def get(self,request):
        user_addresses = Address.objects.filter(user=request.user,is_active=True)
        borrow_book_list, book_amount = all_borrow_books(request)
        information_len = information_amount(request)

        return render(request, 'huiyuan/huiyuan_address.html', {"user_addresses": user_addresses,'book_amount':book_amount,'information_len':information_len})

    def post(self,request):
        # print('测试222')
        recipient = request.POST.get('recipient')
        cell_phone = request.POST.get('cell_phone')
        province = Citys.objects.get(id=request.POST.get('province'))
        city = Citys.objects.get(id=request.POST.get('city'))
        country = Citys.objects.get(id=request.POST.get('country'))
        street = Citys.objects.get(id=request.POST.get('street'))
        detail_address = request.POST.get('detail_address')
        address = Address(user=request.user,consignee=recipient,phone=cell_phone,
                          province=province,city=city,country=country,street=street,detail_address=detail_address)
        address.save()
        return redirect(reverse('bookapp:member_address'))

# 收货地址编辑
def address_edit(request,pid):
    pass

# 收货地址删除
def address_drop(request,pid):
    address = Address.objects.get(id=pid)
    address.is_active = False
    address.save()
    return redirect(reverse('bookapp:member_address'))


# 会员中心-个人资料
@login_required
def member_personal_data(request):

    borrow_book_list, book_amount = all_borrow_books(request)
    information_len = information_amount(request)

    user = User.objects.get(id=request.user.id)
    book_user = BookUser.objects.filter(user=request.user,is_active=True).first()
    book_bean_credit = BookBeanCredit.objects.filter(user=book_user).first()
    # print(book_user)
    return render(request,'huiyuan/huiyuan_gerenziliao.html',{'book_amount':book_amount,'user':user,'book_user':book_user,'book_bean_credit':book_bean_credit,'information_len':information_len})


# 会员中心-修改密码
@login_required
def member_change_password(request):
    borrow_book_list, book_amount = all_borrow_books(request)
    information_len = information_amount(request)

    error = ''
    if request.method == 'POST':
        new_password_1 = request.POST.get('new_password_1')
        new_password_2 = request.POST.get('new_password_2')
        email_code = request.POST.get('email_code','')
        if email_code != '':
            if new_password_1 == new_password_2 and email_code==request.session.get('email_code',''):
                user = request.user
                user.set_password(new_password_1)
                user.save()
                user_logout(request)
                return redirect(reverse('user:login'))
            error = '两次密码不一致！'
        else:
            error = '验证码错误！！'
    return render(request,'huiyuan/huiyuan_change_password.html',{'book_amount':book_amount,'error':error,'information_len':information_len})


def send_email(request):
    """
    邮件发送函数，ajax发送get请求，调用随机字符串函数，生成思维随机数，保存到session中，
    并发送邮件到验证邮箱。
    post请求中判断得到的随机字符串是否与session中所保存的字符串相同，若相同则返回
    :param request:
    :return:
    """
    email = request.GET.get('email','')
    if email == '':
        return HttpResponse('发送失败')
    email_code = random_str()
    msg = '验证码：' + email_code
    send_mail('邮箱验证',msg,settings.EMAIL_FROM,[email],fail_silently=False)
    request.session['email_code'] = email_code
    return HttpResponse('发送成功')



# 邮箱验证码验证
@login_required
def old_password_verify(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password','')
        # if authenticate(username=request.user.username,password=old_password):
        if old_password == '':
            return HttpResponse('验证失败')
        elif request.session.get('email_code') == old_password:
            return HttpResponse('验证成功')
        else:
            return HttpResponse('验证失败')




# 会员中心-浏览历史
@login_required
def member_brow_history(request):
    borrow_book_list, book_amount = all_borrow_books(request)
    information_len = information_amount(request)

    brow_historys = BrowHistory.objects.filter(user=request.user,is_active=True).order_by('-time')
    paginator = Paginator(brow_historys, 6)
    page = request.GET.get('page', 1)
    brow_historys = paginator.page(page)
    return render(request,'huiyuan/huiyuan_history.html',{'brow_historys':brow_historys,'book_amount':book_amount,'information_len':information_len})


# 会员中心-个性分析
@login_required
def member_personality_analysis(request):
    borrow_book_list, book_amount = all_borrow_books(request)
    information_len = information_amount(request)

    brow_historys = BrowHistory.objects.filter(user=request.user,is_active=True)
    dates = {
        'today':0,'date_1':0,'date_2':0,'date_3':0,'date_4':0,'date_5':0,'date_6':0,'date_7':0
    }
    classify = {'Python':0,'Java':0,'Linux':0,'MySQL':0,'math':0,'physics':0,'chemistry':0,'natural_science':0,'foreign_language':0,'philosophy':0,'psychology':0}
    today = datetime.date.today()
    for brow_history in brow_historys:
        # 判断天
        if str(brow_history.time)[0:10] == str(today):
            dates['today'] += 1
        elif str(brow_history.time)[0:10] == str(today-datetime.timedelta(days=1)):
            dates['date_1'] += 1
        elif str(brow_history.time)[0:10] == str(today-datetime.timedelta(days=2)):
            dates['date_2'] += 1
        elif str(brow_history.time)[0:10] == str(today-datetime.timedelta(days=3)):
            dates['date_3'] += 1
        elif str(brow_history.time)[0:10] == str(today-datetime.timedelta(days=4)):
            dates['date_4'] += 1
        elif str(brow_history.time)[0:10] == str(today-datetime.timedelta(days=5)):
            dates['date_5'] += 1
        elif str(brow_history.time)[0:10] == str(today-datetime.timedelta(days=6)):
            dates['date_6'] += 1
        elif str(brow_history.time)[0:10] == str(today - datetime.timedelta(days=7)):
            dates['date_7'] += 1
        else:
            pass

        # 判断分类
        class_name = BookClasses.objects.filter(book=brow_history.book).last().class_name
        if class_name == 'Python类':
            classify['Python'] += 1
        elif class_name == 'JAVA类':
            classify['Java'] += 1
        elif class_name == 'Linux类':
            classify['Linux'] += 1
        elif class_name == 'MySQL类':
            classify['MySQL'] += 1
        elif class_name == '数学类':
            classify['math'] += 1
        elif class_name == '化学类':
            classify['chemistry'] += 1
        elif class_name == '物理类':
            classify['physics'] += 1
        elif class_name == '自然科普类':
            classify['natural_science'] += 1
        elif class_name == '外语':
            classify['foreign_language'] += 1
        elif class_name == '哲学类':
            classify['philosophy'] += 1
        elif class_name == '心理类':
            classify['psychology'] += 1
        else:
            pass

    # jieba分词,将当前用户的所有评论使用jieba分词
    comments = UserBookComment.objects.filter(user=request.user,is_active=True)
    comment_keywords = []
    all_text_list = []
    # 废词
    obsoletism_word = jieba_obsoletism_word()
    # 根据jieba分词，将当前用户的所有评论分词后存入一个列表中
    for comment in comments:
        text_list = list(jieba.cut(comment.comment,cut_all=False))
        all_text_list.extend(text_list)
    # print(all_text_list)
    # 统计列表中不同字符的个数，如果是废词，则不存
    for i in Counter(all_text_list).most_common():
        if i[0] in obsoletism_word:
            continue
        comment_dict = {"name":'',"value":0}
        comment_dict["name"] = i[0]
        comment_dict["value"] = i[1]
        comment_keywords.append(comment_dict)
    # print(comment_keywords)
    return render(request,'huiyuan/huiyuan_personality_analysis.html',{'book_amount':book_amount,'dates':dates,'classify':classify,'comment_keywords':comment_keywords,'information_len':information_len})




# 会员中心-为我推荐
def member_recommend_for_me(request):
    classify = {'Python类':0,'JAVA类':0,'Linux类':0,'MySQL类':0,'数学类':0,'化学类':0,'物理类':0,'自然科普类':0,'外语':0,'哲学类':0,'心理类':0}
    brow_historys = BrowHistory.objects.filter(user=request.user,is_active=True)

    for brow_history in brow_historys:
        # 判断分类
        class_name = BookClasses.objects.filter(book=brow_history.book).last().class_name
        if class_name == 'Python类':
            classify['Python类'] += 1
        elif class_name == 'JAVA类':
            classify['JAVA类'] += 1
        elif class_name == 'Linux类':
            classify['Linux类'] += 1
        elif class_name == 'MySQL类':
            classify['MySQL类'] += 1
        elif class_name == '数学类':
            classify['数学类'] += 1
        elif class_name == '化学类':
            classify['化学类'] += 1
        elif class_name == '物理类':
            classify['物理类'] += 1
        elif class_name == '自然科普类':
            classify['自然科普类'] += 1
        elif class_name == '外语':
            classify['外语'] += 1
        elif class_name == '哲学类':
            classify['哲学类'] += 1
        elif class_name == '心理类':
            classify['心理类'] += 1
        else:
            pass
    # for i,j in classify:
    list1 = sorted(classify.items(),key=lambda i:i[1],reverse=True)
    # print(1111,list1[0][0])
    class_info = BookClasses.objects.filter(class_name=list1[0][0]).first()
    search_books = class_info.book.filter().order_by('-check_number')[0:5]
    # print(content)
    # print(search_books)
    paginator = Paginator(search_books, 9)
    page = request.GET.get('page', 1)
    search_books = paginator.page(page)
    return render(request, 'huiyuan/huiyuan_recommend.html', {'search_books': search_books})


# 会员中心-我的评论
@login_required
def member_comment(request):

    borrow_book_list, book_amount = all_borrow_books(request)
    information_len = information_amount(request)

    user_book_comments = UserBookComment.objects.filter(user=request.user,is_active=True).order_by('-comment_time')
    paginator = Paginator(user_book_comments, 6)
    page = request.GET.get('page', 1)
    user_book_comments = paginator.page(page)
    return render(request,'huiyuan/huiyuan_comment.html',{'book_amount':book_amount,'user_book_comments':user_book_comments,'information_len':information_len})


# 会员中心-我的消息
@login_required
def member_information(request):
    borrow_book_list, book_amount = all_borrow_books(request)
    my_informations = MyInformation.objects.filter(user=request.user,is_dispose=False,is_active=True).order_by('-time')
    information_len = information_amount(request)
    paginator = Paginator(my_informations, 6)
    page = request.GET.get('page', 1)
    my_informations = paginator.page(page)
    return render(request,'huiyuan/huiyuan_information.html',{'book_amount':book_amount,'my_informations':my_informations,'information_len':information_len})

# 消息处理
@login_required
def information_dispose(request,pid):
    my_information = MyInformation.objects.get(id=pid)
    my_information.is_dispose = True
    my_information.save()
    return redirect(reverse('bookapp:member_information'))

# 我的消息个数
def information_amount(aa):
    informations = MyInformation.objects.filter(user=aa.user,is_dispose=False,is_active=True)
    return len(informations)
