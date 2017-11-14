# PostList를 리턴하는 APIView를 만드세요
# 근데 APIView를 상속받도록
# Serializer도 생성 (serializers.py)
# get요청만 응답
from rest_framework import generics, permissions
from rest_framework.response import Response

from member.serializers import UserSerializer
from utils.permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance in user.like_posts.all(pk=instance.pk):
            user.like_posts.remove(instance)
            like_status = False
        else:
            user.like_posts.add(instance)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(instance).data,
            'result': like_status,
        }
        return Response(data)
