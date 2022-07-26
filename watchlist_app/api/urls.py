from django.urls import path,include
# from watchlist_app.api.views import #movie_list,movie_details

from watchlist_app.api.views import WatchListAV,WatchListDetailAV, StreamPlatformAV,WatchListGV
from watchlist_app.api.views import StreamDetailAV, ReviewList, ReviewDetail, UserReview,ReviewCreate
from watchlist_app.api.views import StreamPlatformVS
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')
urlpatterns = [
    path('list/',WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/',WatchListDetailAV.as_view(),name='movie-detail'),
    path('list2/',WatchListGV.as_view(),name='watch-list'),
    # path('stream', StreamPlatformVS.as_view(), name='streamplatform'),

    path('',include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name ='stream'),
    # path('stream/', StreamPlatformVS.as_view(),name='streamplatform'),

    
    # path('stream/<int:pk>/',StreamDetailAV.as_view(),name='stream-details'),

    # path('review/', ReviewList.as_view(), name='review-list'),

    # path('review/<int:pk>', ReviewDetail.as_view(),name='review-details'),

    # path('stream/<int:pk>/review-create',ReviewCreate.as_view(),name='review-creat'),
    
    # path('stream/<int:pk>/review',ReviewList.as_view(),name='review-list'),
    # path('stream/review/<int:pk>',ReviewDetail.as_view(),name='review-list')

    path('<int:pk>/review-create',ReviewCreate.as_view(),name='review-create'),
    
    path('<int:pk>/reviews',ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>',ReviewDetail.as_view(),name='review-details'),

#    path('reviews/<str:username>/',UserReview.as_view(),name='review-detail'),

   path('reviews/',UserReview.as_view(),name='user-review-detail'),

    

    
   
   
]