from rest_framework import serializers
# from watchlist_app.api.views import WatchList
from watchlist_app.models import StreamPlatform,Review,WatchList

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"     

class WatchListSerializer(serializers.ModelSerializer):

    # len_name = serializers.SerializerMethodField()
    # def get_len_name(self, object):
    #     return len(object.title)
    platform = serializers.CharField(source='platform.name')

    # review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchList = WatchListSerializer(many=True, read_only=True)
    # watchList = serializers.StringRelatedField(many=True, read_only=True)
    # watchList = serializers.HyperlinkedRelatedField(many = True,
    # read_only=True,
    # view_name='movie-details')
    class Meta:
        model = StreamPlatform
        fields = "__all__"

        

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and Description should be different ! ")
    #     else:
    #         return data




    # def validate_name(self, value):
         
    #     if len(value) < 10:
    #         raise serializers.ValidationError("Name is too short !! ")
    #     else:
    #         return value












# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validation_data):
#         return Movie.objects.create(**validation_data)

#     def update(self, instance, validation_data):
#         instance.name = validation_data.get('name', instance.name)
#         instance.description = validation_data.get('description', instance.description)
#         instance.active = validation_data.get('active', instance.active)
#         instance.save()
#         return instance



#     def validate(self, data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be defferent ! ")
#         else:
#             return data




#     def validate_name(self, value):
         
#         if len(value) < 10:
#             raise serializers.ValidationError("Name is too short !! ")
#         else:
#             return value