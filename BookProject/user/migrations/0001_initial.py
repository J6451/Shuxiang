# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-16 17:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consignee', models.CharField(max_length=60, verbose_name='收货人')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号')),
                ('province', models.CharField(max_length=50, verbose_name='省')),
                ('city', models.CharField(max_length=50, verbose_name='市')),
                ('country', models.CharField(max_length=50, verbose_name='县')),
                ('street', models.CharField(max_length=50, verbose_name='街道')),
                ('detail_address', models.CharField(max_length=100, verbose_name='详细地址')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '收货地址',
                'verbose_name_plural': '收货地址',
            },
        ),
        migrations.CreateModel(
            name='BookBeanCreditStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_number', models.IntegerField(blank=True, default=0, null=True, verbose_name='加分数量')),
                ('sub_number', models.IntegerField(blank=True, default=0, null=True, verbose_name='减分数量')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('borrow_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics_borrow_book', to='bookapp.BorrowBook')),
            ],
            options={
                'verbose_name': '书香豆信用统计',
                'verbose_name_plural': '书香豆信用统计',
            },
        ),
        migrations.CreateModel(
            name='BookUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sex', models.CharField(blank=True, default='1', max_length=1, null=True, verbose_name='性别')),
                ('age', models.IntegerField(blank=True, default=18, null=True, verbose_name='年龄')),
                ('phone', models.CharField(blank=True, default='12345678901', max_length=20, null=True, verbose_name='手机号')),
                ('is_phone', models.BooleanField(default=False, verbose_name='手机号激活')),
                ('is_email', models.BooleanField(default=False, verbose_name='邮箱激活')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='BrowHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='浏览时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brow_history_book', to='bookapp.Books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brow_history_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '浏览历史',
                'verbose_name_plural': '浏览历史',
            },
        ),
        migrations.CreateModel(
            name='Citys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='城市名')),
                ('level', models.IntegerField(verbose_name='城市等级')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Citys')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='BookBeanCredit',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.BookUser')),
                ('grade', models.CharField(blank=True, default='1级会员', max_length=20, null=True, verbose_name='等级')),
                ('money', models.IntegerField(blank=True, default=0, null=True, verbose_name='书香豆数量')),
                ('number', models.IntegerField(blank=True, default=80, null=True, verbose_name='信用值')),
                ('borrow_all', models.IntegerField(blank=True, default=5, null=True, verbose_name='可借书本总量')),
                ('borrowed', models.IntegerField(blank=True, default=0, null=True, verbose_name='已借书本数量')),
                ('borrow_max_time', models.IntegerField(blank=True, default=30, null=True, verbose_name='可借书本最大时长')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '书香豆信用',
                'verbose_name_plural': '书香豆信用',
            },
        ),
        migrations.AddField(
            model_name='bookbeancreditstatistics',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to=settings.AUTH_USER_MODEL),
        ),
    ]
