from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from .models import BookUser,BookBeanCredit,Citys
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login as user_login,logout as user_logout,authenticate
from django.views import View
from PIL import Image,ImageDraw,ImageFont
import random
from django.utils.six import BytesIO



# 获取验证码
def get_code(request):
    # base64_code,str_code = gvcode.base64()
    # request.session['codes'] = str_code
    # return HttpResponse(base64_code)
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)

    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'ABCDEFGHIJKLMNOPQRST1234567890abcdefghijklmnopqrstuvwxyz'
    # 随机选出4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，
    font = ImageFont.truetype('simsun.ttc', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    # print(HttpResponse(buf.getvalue(),'image/png'))
    return HttpResponse(buf.getvalue(), 'image/png')



class Login(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        # 验证
        error = {}
        static = True
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username,password=password)
        if not user:
            error['username_error'] = '用户不存在或密码错误'
            static = False
        if user and static:
            # 登录前先退出当前登录用户
            user_logout(request)
            # 登录
            user_login(request,user)
            return redirect(reverse('bookapp:index'))
        return render(request,'user/login.html',{'error':error})

class Register(View):
    def get(self,request):
        return render(request,'user/register.html')

    def post(self,request):
        error = {}
        static = True
        username = request.POST.get('username','')
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone')
        code = request.POST.get('code','')
        if username == '':
            error['username_error'] = '用户名不能为空'
            static = False
        if password1 == '' or password2 == '':
            error['password_error'] = '密码不能为空'
            static = False
        if password1 != password2:
            error['password_error'] = '密码不一致'
            static = False
        # 将验证码都转换成大写，然后进行判断
        if code.upper() != request.session.get('verifycode').upper():
            error['code_error'] = '验证码错误'
            static = False
        # 先进行一次判断，优化程序
        if static:
            users = User.objects.all()
            for user in users:
                if username == user.username:
                    error['username_error'] = '用户已存在'
                    static = False
                    break
        if static:
            # 内置用户表保存
            user_info = User(username=username,password=make_password(password1),email=email,is_staff=False)
            user_info.save()
            # 用户表保存
            book_user_info = BookUser(user=user_info,phone=phone)
            book_user_info.save()
            # 书香豆信用表保存
            book_bean_credit_info = BookBeanCredit(user=book_user_info)
            book_bean_credit_info.save()
            return redirect(reverse('user:login'))
        return render(request,'user/register.html',{'error':error})


def logout(request):
    user_logout(request)
    # 退出后重定向到主页
    return redirect(reverse('bookapp:index'))


def getArea1(request):
    list1 = Citys.objects.filter(parent__isnull=True)
    list2 = []
    for i in list1:
        list2.append([i.id,i.name])
    return JsonResponse({"data":list2})

def getArea2(request,pid):
    list1 = Citys.objects.filter(parent_id=pid)
    list2 = []
    for i in list1:
        list2.append({'id':i.id,'name':i.name})
    return JsonResponse({'data':list2})





