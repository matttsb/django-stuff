from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
from slugify import slugify
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django_comments.moderation import CommentModerator, moderator
from django.utils import timezone
from tinymce.models import HTMLField
import re

class BlogPost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True,blank=True,max_length=100, unique=True)
    image = models.ImageField(null=True,upload_to='media/img')
    keywords = models.CharField(max_length=200, null=False, blank=False)
    metad = models.CharField(max_length=200, null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    body = HTMLField(null=True, blank=True)
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('BlogCategory', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        null=True,
        related_name="author",
        verbose_name=('author'),
        on_delete=models.CASCADE)
    enable_comments = models.BooleanField()
    publishdate = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    # publish date is start date for events
    enddate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    visible = models.BooleanField(default=False, null=True, blank=True)
    promote = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.intro:
            self.intro = self.body.partition('.')[0]
        if not self.pk:
            self.slug = slugify(self.title+"_"+self.keywords)
        super(BlogPost, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return '/'+self.category.slug+'/'+self.slug

        # def get_absolute_url(self):
        #     return reverse('blog', args=[category.slug+"/"+self.slug])


class BlogPostModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'


moderator.register(BlogPost, BlogPostModerator)


class BlogCategory(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return f'{self.title}'


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100, null=True, blank=True)
    updated = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'


class ParttypesManager(models.Manager):
    def create_part(self, name):
        part = self.create(name=name)
        # do something with the book
        return part


class Parttypes(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=100, unique=True)
    objects = ParttypesManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'


class Part(models.Model):
    mpn = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    man = models.ForeignKey(
        to=Manufacturer,
        on_delete=models.SET_NULL,
        null=True)
    parttype = models.ForeignKey(to=Parttypes, on_delete=models.CASCADE)
    dim = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['mpn']

    def __str__(self):
        return f'{self.mpn}'


TYPE_CHOICES = [
    ('EL', 'ELECTRIC'),
    ('AS', 'AIR SOURCE'),
    ('GE', 'GEOTHERMAL'),
    ('LP', 'LPG'),
    ('LC', 'LPG Combi'),
    ('NG', 'Natural Gas'),
    ('NC', 'Natural Gas Combi'),
    ('CU', 'Combi'),
    ('OI', 'OIL'),
]


class Appliance(models.Model):
    appid = models.CharField(max_length=100, blank=True, null=True)
    nameandmodel = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.ForeignKey(
        to=Manufacturer,
        on_delete=models.SET_NULL,
        null=True)
    mpn = models.CharField(max_length=100, blank=True, null=True)
    doclink = models.CharField(max_length=200, blank=True, null=True)
    visible = models.BooleanField(default=False)
    fuel = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        blank=True, null=True
    )
    parts = models.ManyToManyField(Part, blank=True)
    comments = GenericRelation(Comment)

    def get_absolute_url(self):
        return reverse('appliance-detail', args=[str(self.slug)])

    def save(self, **kwargs):
        if not self.slug:
            slug = slugify(self.nameandmodel)
            while True:
                try:
                    appliance = Appliance.objects.get(slug=slug)
                    if appliance == self:
                        self.slug = slug
                        break
                    else:
                        slug = slug + '-'
                except BaseException:
                    self.slug = slug
                    break

        super(Appliance, self).save()

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.nameandmodel}'
