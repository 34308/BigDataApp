"""
URL configuration for BigDataApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from DjangoDB import views

urlpatterns = [
    path('list-of-all-countries', views.getListOfCountriesWichWeHaveDataOn),
    path('covid-allcases-plot/<str:country>', views.getAllCasesForCountry),
    path('covid-<str:case>-cases-db/<str:country>', views.CasesForCountryTillNowFromDatabaseData),
    path('covid-<str:case>-cases-plot-db/<str:country>', views.CasesForCountryTillNowFromDatabasePlot),
    path('covid-country-with-most-deaths',views.getCountryWithMostDeathsData),
    path('covid-country-with-least-deaths', views.getCountryWithLeastDeathsData),
    path('covid-compare-countries-plot/<str:case>/<str:first_country>/<str:second_country>',views.compare_countries_by_case_plot),
    path('covid-compare-countries/<str:case>/<str:first_country>/<str:second_country>', views.compare_countries_by_case)

]
