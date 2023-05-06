from datetime import datetime
from enum import Enum
casesForCountry= "CasesForCountry"
slugOfCountries="slugOfCountries"
countryWithMostDeaths="CountryWithMostDeaths"
countryWithLeastDeaths="CountryWithLeastDeaths"

listOfCountries="ListOfCountries"
updateList="UpdateList"
Cases=Enum('Case',["Confirmed","Recovered","Death"])

basic_date=datetime(2020, 3, 21, 0, 0, 0)