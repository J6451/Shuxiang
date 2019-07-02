from django.shortcuts import render,redirect,reverse
import random


# 验证是否登录（装饰器）
def login_required(view_func):
    def check(request,*args,**kwargs):
        # 判断session中是否有user
        # try:
        # 判断user是否是匿名用户
        if str(request.user) != 'AnonymousUser':
            return view_func(request,*args,**kwargs)
        else:
            return redirect(reverse('user:login'))
        # except:
        #     return redirect(reverse('user:login'))
    return check


# 出版社对应
def press_shift(press_id):
    press_dict = {
        '1':'清华大学出版社',
        '2':'机械工业出版社',
        '3':'电子工业出版社',
        '4':'人民邮电出版社',
        '5':'安徽大学出版社',
        '6':'安徽教育出版社',
    }
    return press_dict[press_id]

# 随机数函数
def random_str():
    _str = '1234567890'
    return ''.join(random.choice(_str) for i in range(4))



# jieba分词中费词
def jieba_obsoletism_word():
    list = [
        '!',
        '！',
        ',',
        '，',
        '.',
        '\'',
        '\"',
        '。',
        '这',
        '；',
        ';',
        '、',
        '?',
        '*',
        '本',
        '书',
        '本书',
        '%',
        '@']
    return list




