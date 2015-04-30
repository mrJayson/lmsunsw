from swampdragon.serializers.model_serializer import ModelSerializer

class NotificationSerializer(ModelSerializer):
    class Meta:
    	# need to specify explicitly or cause circular import
        model = 'app.Notification'
        publish_fields = ['message']