from datetime import datetime
from enum import Enum

confirmedCasesForCountries="ConfirmedCasesForCountries"
deathCasesForCountries="DeathCasesForCountries"
recoveredCasesForCountries="RecoveredCasesForCountries"
countryWithMostDeaths="CountryWithMostDeaths"
listOfCountries="ListOfCountries"
updateList="updateList"
CaseTable=Enum('CaseTable',[confirmedCasesForCountries,deathCasesForCountries,recoveredCasesForCountries])
Cases=Enum('Case',["Confirmed","Recovered","Death"])

basic_date=datetime(2020, 3, 21, 0, 0, 0)