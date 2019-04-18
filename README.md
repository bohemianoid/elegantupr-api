# elegantupr-api
API for Elegant Visualisation of ecoinvent Unit Processes

## API
### Parser
Accepts a ecospold2 file upload and parses it into a readable activity object including name, geography shortname and exchanges.

```
POST /parser
```

```
{
  "name": "medium density fibre board production, uncoated",
  "geography_shortname": "RER",
  "exchanges": {
    "reference_product": [
      {
        "amount": 1.0,
        "compartment": null,
        "name": "medium density fibreboard",
        "production_volume_amount": 11114926.0,
        "unit_name": "m3"
      }
    ],
    "by_products": [
      {
        "amount": 2.00503576,
        "compartment": null,
        "name": "wood ash mixture, pure",
        "production_volume_amount": 22285824.0997538,
        "unit_name": "kg"
      }, ...
    ],
    "from_technosphere": [
      {
        "amount": 287.0,
        "compartment": null,
        "name": "tap water",
        "production_volume_amount": null,
        "unit_name": "kg"
      }, ...
    ],
    "from_environment": [
      {
        "amount": 0.323,
        "compartment": "natural resource",
        "name": "Water, river",
        "production_volume_amount": null,
        "unit_name": "m3"
      }, ...
    ],
    "to_environment": [
      {
        "amount": 1.684904e-07,
        "compartment": "air",
        "name": "Chromium VI",
        "production_volume_amount": null,
        "unit_name": "kg"
      }, ...
    ]
  },
}
```

### Filter
Accepts a jsonified activity object and filters it. By-products only include 4 by-products with the highest production volume amount. Other exchanges only include 5 exchanges with the highest amount aggregating similar exchanges to different compartments.

```
POST /filter
```

## Running Locally
```
$ git clone https://github.com/simonroth/elegantupr-api.git
$ cd elegantupr-api

$ virtualenv venv
$ source venv/bin/activate

(venv) $ pip install -r requirements.txt

(venv) $ gunicorn elegantupr.app:app
```

elegantupr-api should now be running on [localhost:8000](http://localhost:8000).

## Deploying to Heroku
```
$ heroku create
$ git push heroku master

$ heroku open
```
