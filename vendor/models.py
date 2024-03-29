from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendors (models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    class Meta:
         verbose_name_plural = "Vendors"

    def save(self, *args, **kwargs):
        # update
        if self.pk is not None:
            orig = Vendors.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    'user':self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved != True:
                    mail_subject = "Congratulation, your restaurant has been approved"
                    # Send notif email
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject = "You are not eligible for publishing your menu on our marketplace"
                    # Send notif email
                    send_notification(mail_subject,mail_template,context)
        return super(Vendors,self).save(*args,**kwargs)
