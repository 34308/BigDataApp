from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class CovidData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.DateField()
    total_cases = models.IntegerField()
    new_cases = models.IntegerField()
    total_deaths = models.IntegerField()
    new_deaths = models.IntegerField()

    class Meta:
        unique_together = ('country', 'date')

    def __str__(self):
        return f"{self.country.name} - {self.date}"
