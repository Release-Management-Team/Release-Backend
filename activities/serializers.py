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






class get_event_list_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_time', 'place']



class get_event_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'content', 'start_time', 'place']


class create_event_serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'content', 'place', 'start_time']

class create_event_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'content', 'start_time', 'place']



class update_event_serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'content', 'place', 'start_time']



class update_event_response_serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'content', 'start_time', 'place']


class delete_event_response_serializer(serializers.Serializer):
    message=serializers.CharField()