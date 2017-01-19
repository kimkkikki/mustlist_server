from django.db import models
import uuid
from rest_framework import serializers


class User(models.Model):
    class Meta:
        db_table = 'user'
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4)
    key = models.UUIDField(default=uuid.uuid4)
    email = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)
    device_id = models.TextField(null=True)
    point = models.IntegerField(default=0)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Must(models.Model):
    class Meta:
        db_table = 'must'
    index = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(db_index=True)
    deposit = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    default_point = models.IntegerField(default=0)
    success_point = models.IntegerField(default=0)
    success = models.BooleanField(default=False)
    end = models.BooleanField(default=False)


class MustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Must
        fields = '__all__'


class Pay(models.Model):
    class Meta:
        db_table = 'pay'
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User)
    must = models.ForeignKey(Must)
    product_id = models.CharField(max_length=20)
    order_id = models.CharField(max_length=50, db_index=True)
    token = models.TextField()
    date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    refund = models.BooleanField(default=False)


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'


class MustCheck(models.Model):
    class Meta:
        db_table = 'must_check'
    index = models.AutoField(primary_key=True)
    must = models.ForeignKey(Must, db_index=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Notice(models.Model):
    class Meta:
        db_table = 'notice'
    id = models.AutoField(primary_key=True, editable=False)
    type = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class Score(models.Model):
    class Meta:
        db_table = 'score'
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    must = models.ForeignKey(Must, on_delete=models.CASCADE, db_index=True)
    type = models.CharField(max_length=1, default='C')
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
