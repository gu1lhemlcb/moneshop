from io import BytesIO
from django.core.files import File
from django.db import models
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta: 
        verbose_name_plural = "Categories"
        ordering = ('ordering',)

    def __str__(self):
        return self.title

#la fonction ci dessus permets d'afficher dans l'interface django admin le nom de chaque Categorie car sans configuration c'est un nom générique

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) # Si l'on suprime la catégorie on supprime aussi le produit
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to ="media/uploads/images", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="media/uploads/thumbnails", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta: 
        verbose_name_plural = "Products"
        ordering = ('-date_added',)

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)


    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


