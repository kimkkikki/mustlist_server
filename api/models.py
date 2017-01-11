from django.db import models
import uuid
from rest_framework import serializers


class User(models.Model):
    class Meta:
        db_table = 'user'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(null=True, max_length=100)
    point = models.IntegerField(default=0)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Purchase(models.Model):
    class Meta:
        db_table = 'purchase'
    developer_payload = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    itemType = models.CharField(null=True, max_length=10)
    purchase_time = models.DateTimeField(null=True)
    order_id = models.CharField(null=True, max_length=100)
    original_json = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class Must(models.Model):
    class Meta:
        db_table = 'must'
    index = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    purchase = models.ForeignKey(Purchase, null=True)
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(db_index=True)
    deposit = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    default_point = models.IntegerField(default=0)
    success_point = models.IntegerField(default=0)
    success_yn = models.BooleanField(default=False)


class MustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Must
        fields = '__all__'


class MustCheck(models.Model):
    class Meta:
        db_table = 'must_check'
    index = models.AutoField(primary_key=True)
    must = models.ForeignKey(Must)
    date = models.DateField()
    check_yn = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class Notice(models.Model):
    class Meta:
        db_table = 'notice'
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
