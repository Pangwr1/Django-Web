from django.db import models

# Create your models here.

class Student(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女"),
    ]

    name    = models.CharField(max_length=50, verbose_name="姓名")
    gender  = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    birthday= models.DateField(verbose_name="生日")
    email   = models.EmailField(verbose_name="邮箱")
    info    = models.CharField(max_length=255, verbose_name="个人简介", help_text="一句话介绍自己")

    grade   = models.CharField(max_length=4, verbose_name="年级")
    number  = models.CharField(max_length=6, verbose_name="学号")
    password= models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['grade', 'number'], name='student_id')
        ]
    
    def get_id(self):
        return "%s%s" % (self.grade, self.number)

    def __str__(self):
        return "%s (%s)" % (self.get_id(), self.name)

class Administrator(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女"),
    ]

    name    = models.CharField(max_length=50, verbose_name="姓名")
    gender  = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    birthday= models.DateField(verbose_name="生日")
    email   = models.EmailField(verbose_name="邮箱")
    info    = models.CharField(max_length=255, verbose_name="个人简介", help_text="一句话介绍自己")

    grade   = models.CharField(max_length=4, verbose_name="年级")
    number  = models.CharField(max_length=6, verbose_name="编号")
    password= models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['grade', 'number'], name='administrator_id')
        ]
    
    def get_id(self):
        return "%s%s" % (self.grade, self.number)

    def __str__(self):
        return "%s (%s)" % (self.get_id(), self.name)
