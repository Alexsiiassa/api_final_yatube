from django.contrib.auth import get_user_model

from posts.models import Comment, Follow, Group, Post


from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Serialiazer for Groups
    """
    class Meta:
        fields = ('title',)
        model = Group


class PostSerializer(serializers.ModelSerializer):
    """Serialiazer for Posts
    """
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Serialiazer for Comment
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Serialiazer for Follow
    """
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        )

    def validate_following(self, following):
        """Validate for Following
        """
        if self.context.get('request').user == following:
            raise serializers.ValidationError(
                'You can not follow to yourself.')
        return following
