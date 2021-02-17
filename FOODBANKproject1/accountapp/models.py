from django.db import models

# Create your models here.
class Users(models.Model):
    useremail = models.EmailField(max_length=30, primary_key=True, verbose_name="이메일(아이디)")
    username = models.CharField(max_length=12, verbose_name="사용자 이름")
    password = models.CharField(max_length=12, verbose_name="비밀 번호")


