from django.db.models import F, Count
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


from .filters import StorageListFilter
from .models import Brand, Image, Category, Cap, Banner, Storage, Basket
from .serializers import (
    StorageListSerializer,
    StorageActionListSerializer,
    BannerListSerializer,
    BrandListSerializer,
    StorageDetailListSerializer,
    CapDetailListSerializer,
    LikeCreateSerializer,
    BasketCreateSerializer, CapListSerializer
)


class MainPageView(APIView):

    def get(self, request):
        banners = Banner.objects.all()
        brands = Brand.objects.all()
        bestsellers = Storage.objects.all()
        action_caps = Storage.objects.filter(cap__old_price__gt=F('cap__actual_price'))

        banner_serializers = BannerListSerializer(banners, many=True)
        brands_serializer = BrandListSerializer(brands, many=True)
        bestsellers_serializers = StorageListSerializer(bestsellers, many=True)
        action_caps_serializers = StorageActionListSerializer(action_caps, many=True)

        data = {
            'banners': banner_serializers.data,
            'brands': brands_serializer.data,
            'bestsellers': bestsellers_serializers.data,
            'action_caps': action_caps_serializers.data,
        }

        return Response(data)


class StorageDetailListView(APIView):

    def get(self, request, slug):
        cap_detail = Storage.objects.filter(cap__slug=slug).first()
        similar = Storage.objects.filter(cap__category=cap_detail.cap.category)

        cap_serializer = StorageDetailListSerializer(cap_detail)
        similar_serializer = StorageListSerializer(similar, many=True)

        data = {
            'cap_detail': cap_serializer.data,
            'similar': similar_serializer.data
        }

        return Response(data)

    def post(self, request, slug):
        serializer = LikeCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StorageListPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StorageListView(ListCreateAPIView):
    queryset = Storage.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StorageListFilter
    pagination_class = StorageListPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StorageListSerializer
        elif self.request.method == 'POST':
            return LikeCreateSerializer


class BasketCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=BasketCreateSerializer()
    )
    def post(self, request):
        serializer = BasketCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)




