from django.db import models
import uuid


class User(models.Model):
    class Meta:
        db_table = 'user'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    key = models.UUIDField(default=uuid.uuid4())
    reg_date = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(null=True)
    point = models.IntegerField(default=0)


class Must(models.Model):
    class Meta:
        db_table = 'must'
    index = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    amount = models.IntegerField()
    reg_date = models.DateTimeField(auto_now_add=True)
    default_point = models.IntegerField()
    success_point = models.IntegerField()
    success_yn = models.BooleanField(default=False)


class MustCheck(models.Model):
    class Meta:
        db_table = 'must_check'
    index = models.AutoField(primary_key=True)
    must_index = models.ForeignKey(Must)
    date = models.DateTimeField(auto_now_add=True)
    check_yn = models.BooleanField(default=False)


class Purchase(models.Model):
    class Meta:
        db_table = 'purchase'
    developer_payload = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user_id = models.ForeignKey(User)
    itemType = models.CharField(null=True)
    purchase_time = models.DateTimeField(null=True)
    order_id = models.CharField(null=True)
    original_json = models.TextField(null=True)
