from django.db.models.signals import post_save
from django.dispatch import receiver
from .models  import User, UserProfile

@receiver(post_save,sender=User)   
def created_user_profile_receiver (sender, instance, created, **kwargs):
    print("kk",created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:
            user_profile = UserProfile.objects.get(user=instance)
            print(user_profile)
            
            user_profile.save()
        except:
            print('jsdkfj')
            UserProfile.objects.create(user=instance)

