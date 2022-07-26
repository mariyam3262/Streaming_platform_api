from warnings import filters
from django.forms import ValidationError

from django.shortcuts import render
from watchlist_app.models import WatchList,StreamPlatform, Review
from watchlist_app.api.serializers import StreamPlatformSerializer, ReviewSerializer,WatchListSerializer


# from rest_framework import pagination
# from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
# from rest_framework import serializers
from rest_framework.views import APIView
# from rest_framework.serializers import Serializer
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination,WatchListCPagination




class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username =self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username =self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)







# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
 

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)


#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        





class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    throttle_class = [ReviewCreateThrottle]

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie !")

        if watchlist.number_rating == 0:
             watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist = watchlist, review_user=review_user)



class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_class = [ReviewListThrottle,AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['review-user__username','active']
    # permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']        
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_class= [ScopedRateThrottle]
    throttle_scope = 'review-detail'









# class ReviewList(mixins.ListModelMixin, 
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request,*args, **kwargs):
#         return self.list(request, *args, **kwargs)
#     def post(self, request, *args, **kwargs):
#         return self.create(self, request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request,*args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)





class StreamPlatformVS(viewsets.ModelViewSet):
    #ReadOnlyModelViewSet ====>  only read the content(ONLY get method)
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer





class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class StreamDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform =StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
       platform= StreamPlatform.objects.get(pk=pk)
       platform.delete()
       return Response(status=status.HTTP_204_NO_CONTENT )



#--------------------------------------------------------------------------------------------------  

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    #(queryset,many=True)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title','platform__name']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['^title','=platform__name']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination

 
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies , many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        print(pk)

        try:
            movie =WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
       movie = WatchList.objects.get(pk=pk)
       movie.delete()
       return Response(status=status.HTTP_204_NO_CONTENT )


   


        




# @api_view(['GET','POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':


#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.#HTTP_204_NO_CONTENT )