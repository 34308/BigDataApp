from enum import Enum

confirmedCasesForCountries="ConfirmedCasesForCountries"
deathCasesForCountries="DeathCasesForCountries"
recoveredCasesForCountries="RecoveredCasesForCountries"
countryWithMostDeaths="CountryWithMostDeaths"
listOfCountries="ListOfCountries"

CaseTable=Enum('CaseTable',[confirmedCasesForCountries,deathCasesForCountries,recoveredCasesForCountries])
Cases=Enum('Case',["Confirmed","Recovered","Death"])