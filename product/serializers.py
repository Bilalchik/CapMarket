from rest_framework import serializers
from .models import Brand, Image, Category, Cap, Banner, Storage, Like, Basket


class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'title', 'logo')


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')


class CapListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Cap
        fields = ('id', 'title', 'main_cover', 'cap_model', 'category', 'actual_price')


class CapActionListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Cap
        fields = ('id', 'title', 'main_cover', 'cap_model', 'category', 'price', 'old_price')


class StorageListSerializer(serializers.ModelSerializer):
    cap = CapListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'cap', 'status', 'created_date')


class StorageActionListSerializer(serializers.ModelSerializer):
    cap = CapActionListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'cap', 'status', 'created_date')


class ImageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class BannerListSerializer(serializers.ModelSerializer):
    cap = CapListSerializer()
    image = ImageListSerializer()

    class Meta:
        model = Banner
        fields = ('id', 'cap', 'image', 'description', 'is_main')


class CapDetailListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    brands = BrandListSerializer(many=True)
    images = ImageListSerializer(many=True)

    class Meta:
        model = Cap
        fields = '__all__'


class StorageDetailListSerializer(serializers.ModelSerializer):

    cap = CapDetailListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'cap', 'quantity', 'get_status_display', 'created_date')


class LikeCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('user', 'cap')


class BasketCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Basket
        fields = ('user', 'cap', 'quantity', 'address')

    def validate(self, attrs):
        cap_id = attrs['cap'].id

        object = Storage.objects.filter(cap__id=cap_id).exists()

        if not object:
            raise serializers.ValidationError('Такого товара не существует!')

        return attrs

