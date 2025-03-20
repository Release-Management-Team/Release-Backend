from rest_framework import serializers

from .models import Activity, Event

class get_activity_list_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'leader', 'image', 'info', 'state']


class get_activity_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'content', 'leader', 'image', 'link', 'info', 'state']



class create_activity_serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['title', 'content', 'link', 'state']

class create_activity_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'content', 'leader', 'image', 'link', 'info', 'state']



class update_activity_serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['title', 'content', 'link', 'state']



class update_activity_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'content', 'leader', 'image', 'link', 'info', 'state']


class delete_activity_response_serializer(serializers.Serializer):
    message=serializers.CharField()