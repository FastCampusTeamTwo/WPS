# Generated by Django 2.0.3 on 2018-04-17 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0002_itemendorsement_restaurantendorsement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_lat', models.FloatField(default=0, verbose_name='배달위치 위도')),
                ('delivery_lng', models.FloatField(default=0, verbose_name='배달위치 경도')),
                ('delivery_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='배달 주소')),
                ('delivery_address_detail', models.CharField(blank=True, max_length=255, null=True, verbose_name='배달 상세주소')),
                ('delivery_comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='배달요청사항')),
                ('delivery_date_time', models.DateTimeField(default=None, null=True, verbose_name='예약시간')),
                ('payment_method', models.CharField(max_length=10, verbose_name='결제수단')),
                ('payment_num', models.CharField(max_length=19, verbose_name='카드번호')),
                ('order_comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='주문요청사항')),
                ('order_status', models.CharField(choices=[('A', '준비중'), ('B', '조리중'), ('C', '배달중'), ('D', '배달완료'), ('Z', '주문취소')], default='A', max_length=1, verbose_name='주문상태')),
                ('order_create_at', models.DateTimeField(auto_now_add=True)),
                ('price_total', models.PositiveIntegerField(default=0, verbose_name='총 가격 합계')),
                ('order_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='주문유저')),
                ('order_restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='restaurant.Restaurant', verbose_name='식당')),
            ],
            options={
                'verbose_name': '주문정보',
                'verbose_name_plural': '주문정보들',
                'ordering': ['-order_create_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='가격')),
                ('cnt', models.PositiveIntegerField(default=0, verbose_name='수량')),
                ('sub_total', models.PositiveIntegerField(default=0, verbose_name='가격 합계')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='요청사항')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='restaurant.Items', verbose_name='상품')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.Order', verbose_name='주문')),
            ],
            options={
                'verbose_name': '주문 상세',
                'verbose_name_plural': '주문 상세 아이템들',
                'ordering': ['order', 'pk'],
            },
        ),
    ]