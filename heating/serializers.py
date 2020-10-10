from rest_framework import serializers
from comment.models import Comment
from comment.api.serializers import CommentSerializer


class ApplianceSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Appliance
        fields = ('id',
                  'appid',
                  'nameandmodel',
                  'model',
                  'slug',
                  'name',
                  'manufacturer',
                  'mpn',
                  'doclink',
                  'visible',
                  'fuel',
                  'parts',
                  'comments')

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_by_object(obj)
        return CommentSerializer(comments_qs, many=True).data


class BlogPostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Appliance
        fields = ('id',
                  'appid')

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_by_object(obj)
        return CommentSerializer(comments_qs, many=True).data
