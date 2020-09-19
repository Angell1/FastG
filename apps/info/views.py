from django.shortcuts import render
from .models import User
from  django.
# Create your views here.


# 以name和age过滤
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'age')