from django.contrib.auth import get_user_model
from django.db import models

import uuid

User = get_user_model(

)


class Brand(models.Model):
    logo = models.ImageField(upload_to='media/brand_logo')
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.ImageField(upload_to='media/image')


class Category(models.Model):
    title = models.CharField(max_length=222)

    def __str__(self):
        return self.title


class Cap(models.Model):
    brands = models.ManyToManyField(Brand)
    title = models.CharField(max_length=123)
    cap_model = models.CharField(max_length=223)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(
        choices=(
            (1, 'S'),
            (2, 'M'),
            (3, 'L'),
            (4, 'XL'),
        )
    )
    actual_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True
    )
    main_cover = models.ImageField(upload_to='media/main_covers')
    images = models.ManyToManyField(Image)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())[:8]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Storage(models.Model):
    cap = models.ForeignKey(Cap, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Нет в наличии'),
            (2, 'Скоро в наличии'),
            (3, 'В наличии')
        )
    )
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cap)


class Banner(models.Model):
    cap = models.ForeignKey(Cap, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    description = models.CharField(max_length=124)
    is_main = models.BooleanField()

    def __str__(self):
        return str(self.cap)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cap = models.ForeignKey(Storage, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> {self.cap}"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cap = models.ForeignKey(Storage, on_delete=models.CASCADE)
    delivery_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=500.00
    )
    quantity = models.PositiveSmallIntegerField()
    unique_code = models.CharField(max_length=8, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    shipping_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=223)
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'В пути'),
            (2, 'Доставлен'),
            (3, 'Отменено'),
            (4, 'В обработке'),
        ),
        default=4
    )
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4())[:8]
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
