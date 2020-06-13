from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class Serializer(BaseSerializer):
#     @property
#     def data(self):
#         ret = super(Serializer, self).data
#         return ReturnDict(ret, serializer=self)

# class ReturnDict(OrderedDict):
#     def __init__(self, *args, **kwargs):
#         self.serializer = kwargs.pop('serializer')
#         super(ReturnDict, self).__init__(*args, **kwargs)