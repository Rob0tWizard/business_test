from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=155, unique=True)
    email = models.EmailField(validators=[EmailValidator()])
    password = models.CharField(max_length=155)
    role = models.CharField(max_length=25, choices=[('admin', 'Administartor'), ('manager', 'Manager')])
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions',
        blank=True,
        help_text='Специальные разрешения для этого пользователя.'
    )

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role == 'manager'


class Report(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ])

    def __str__(self):
        return self.title

    def get_status_display(self):
        return dict(self._meta.get_field('status').choices)[self.status]

    def can_edit(self, user):
        return user == self.author or user.is_admin()


class Revenue(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'{self.report} - {self.amount} - {self.date}'

# @post_save.connect(sender=Report)
# def send_report_update_email(sender, instance, created, **kwargs):
#     if created:
#         subject = "New Report Created"
#     else:
#         subject = "Report Updated"
#
#     message = f"""
#     A report has been {subject.lower()}.
#
#     Report Title: {instance.title}
#     Author: {instance.author.username}
#     Content: {instance.content}
#     Status: {instance.get_status_display()}
#     """
#
#     mail_list = ['youremail@example.com']
#
#     send_mail(subject, message, None, mail_list)
