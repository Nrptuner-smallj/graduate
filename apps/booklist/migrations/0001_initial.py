# Generated by Django 2.0.2 on 2018-06-01 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commoditys', '0007_commodity_sell_nums'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('tag1', models.CharField(max_length=30, verbose_name='标签一')),
                ('tag2', models.CharField(max_length=30, verbose_name='标签二')),
                ('click_nums', models.IntegerField(verbose_name='点击量')),
                ('desc', models.CharField(max_length=500, verbose_name='简介')),
                ('is_pub', models.BooleanField(verbose_name='是否公开')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '书单',
                'verbose_name_plural': '书单',
            },
        ),
        migrations.CreateModel(
            name='BookListDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.BookList', verbose_name='书单')),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commoditys.Commodity', verbose_name='商品')),
            ],
            options={
                'verbose_name': '书单记录',
                'verbose_name_plural': '书单记录',
            },
        ),
    ]
