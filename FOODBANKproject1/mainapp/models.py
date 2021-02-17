from django.db import models
from accountapp.models import Users

class Board(models.Model):
    writer = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    writedate = models.DateTimeField(auto_now_add=True)
    cnt = models.IntegerField(default=0)
    like = models.IntegerField(default=0)

    @property
    def update_counter(self):
        self.cnt += 1
        self.save()

    @property
    def up_like(self):
        self.like += 1
        self.save()

    @property
    def down_like(self):
        self.like -= 1
        self.save()

class recommend(models.Model):
    useremail=models.ForeignKey(Users,on_delete=models.CASCADE)
    board=models.ForeignKey(Board,on_delete=models.CASCADE)

class preferItem(models.Model):
    Code = models.ForeignKey(Users, on_delete=models.CASCADE)
    Name= models.TextField()
    Prefer_product = models.TextField()
    Prefer_amount = models.TextField()

