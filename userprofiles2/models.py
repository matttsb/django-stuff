from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse  # To generate URLS by reversing URL patterns
from django_comments.models import Comment

STATUS = (('U', 'Unread'), ('R', 'Read'), ('D', 'Delivered'))
TYPE = (('T', 'Text'), ('I', 'Image'))


class CommentLikes(models.Model):
    class Meta:
        db_table = "likeuser"
    
    user= models.ForeignKey(User, null=True, related_name="likeuser",
                              verbose_name=_('LikeUser'), on_delete=models.CASCADE)
    comment= models.ForeignKey(Comment, null=True, related_name="likecomment",
                              verbose_name=_('LikeComment'), on_delete=models.CASCADE)

#duplicate for PostLikes and ProfileLikes


class Chat(models.Model):
    owner = models.ForeignKey(User, null=True, related_name="owner",
                              verbose_name=_('User'), on_delete=models.CASCADE)
    otherparty = models.ForeignKey(
        User,
        null=True,
        related_name="otherparty",
        verbose_name=_('User'),
        on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User,
        null=True,
        related_name="sender",
        verbose_name=_('User'),
        on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User,
        null=True,
        related_name="receiver",
        verbose_name=_('User'),
        on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=1, blank=True, verbose_name=_('Status'), choices=STATUS)
    type = models.CharField(
        max_length=1, blank=True, verbose_name=_('Type'), choices=TYPE)
    body = models.CharField(max_length=250)


GENDER = (('Male', 'Male'), ('Female', 'Female'))


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        related_name="profile",
        verbose_name=_('User'),
        on_delete=models.CASCADE)
    last_seen = models.DateTimeField(default=timezone.now)
    phone = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('Phone'))
    gender = models.CharField(
        max_length=40, blank=True, verbose_name=_('Gender'), choices=GENDER)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, verbose_name=_('Avatar'))
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    tagline = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to='logos',
        blank=True,
        verbose_name=_('Logos'))
    completion_level = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('Profile completion percentage'))
    email_is_verified = models.BooleanField(
        default=False, verbose_name=_('Email is verified'))
    notify_new_messages = models.BooleanField(
        default=False, verbose_name=_('Email notification of new messages'))
    website_is_verified = models.BooleanField(
        default=False, verbose_name=_('Website is verified'))
    profile_is_visible = models.BooleanField(
        default=True, verbose_name=_('Email is verified'))
    personal_info_is_completed = models.BooleanField(
        default=False, verbose_name=_('Personal info completed'))

    def age(self):
        import datetime
        dob = self.dob
        tod = datetime.date.today()
        user_age = (tod.year - dob.year) - \
            int((tod.month, tod.day) < (dob.month, dob.day))
        return user_age

    class Meta:
        ordering = ['last_seen']

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')

    def __str__(self):
        return "User profile: %s" % self.user.username

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.pk)])

    def get_completion_level(self):
        completion_level = 0
        if self.email_is_verified:
            completion_level += 50
        if self.personal_info_is_completed:
            completion_level += 50
        return completion_level

    def update_completion_level(self):
        self.completion_level = self.get_completion_level()
        self.save()
