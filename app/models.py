from django.db import models 

# Create your models here.


countries = {
    "44": "uk"
}
categories = [
    "News",
    "Entertainment",
    "Politics",
    "Dating"
]

country_choices = tuple([(x,x) for x in list(countries.values())])
category_choices = tuple([(x,x) for x in list(categories)])

class CategoryTable(models.Model):
    country = models.CharField(max_length=100, choices=country_choices)
    category = models.CharField(max_length=100, choices=category_choices)
    def __str__(self) -> str:
        return f'{self.country} -- {self.category}'

class WebListingTable(models.Model):
    country = models.CharField(max_length=100, choices=country_choices,blank=True,null=True)
    category = models.CharField(max_length=100, choices=category_choices,blank=True,null=True)
    title = models.CharField(max_length=100, blank=True,null=True)
    url = models.CharField(max_length=100, blank=True,null=True)
    logo = models.FileField(upload_to="logos") 

    def __str__(self) -> str:
        return f'{self.title} -- {self.url}'



