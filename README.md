# BigDataApp

Application stores **Covid** data, and enable us to display it in way that we want.

## Starting app

Go to the app folder, and run:
```
python manage.py runserver --noreaload
```
Application should be hosted on `http://127.0.0.1:8000/`

## Using app

App have following endpoints:

  1) `/ListOfAllCountries` - returns list of all countries, that we can use
        
      example output:
        ```json
        {
          "countries": [
              "Afghanistan",
              "Albania",
              "Algeria",
              "Andorra",
              "Angola",
              "Antarctica",
              "Antigua and Barbuda",
              ...
              "Yemen",
              "Zambia",
              "Zimbabwe"
              ]
          }
  
  3) `/covid-allcases-plot/*country*` - saves covid data from country do database
      
      path variables:
        - `country` - name of country eg. `poland`
        
      example output: 
      ```json
      {
        "data": [
            "Confirmed, Deaths, Recovered cases for poland, correctly saved to database"
          ]
      }
      ```
        
  4) `/covid-*case*-cases-plot-db/*country*`
      
      path variables:
      - `case` - `confirmed`, `death`, or `recovered`
      - `country` - name of country eg. `poland`
      
      example output:
      
      <img width="321" alt="image" src="https://user-images.githubusercontent.com/86781217/236620727-182a7b12-8ba1-4cce-a69f-5115097c3d7e.png">

      
  5) `/most-deaths` - return country with the most amount of deaths
  
      example output:
      ```json
      {
        "Country": "United States of America",
        "death_Cases": 1123836
      }
      ```
