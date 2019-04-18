from flask import Blueprint, jsonify, request
from pandas import DataFrame

def filter_by_products(by_products):
    """Filter by-products to only include 4 by-products with the highest
    production volume amount.

    NOTE: Units may not be comparable.

    Arguments:
    by_products -- Array of by_product dictionaries
    """
    if by_products:
        by_products = DataFrame(by_products)

        by_products = by_products.nlargest(4, 'production_volume_amount')

        by_products = by_products.to_dict('records')

    return by_products

def filter_exchanges(exchanges):
    """Filter exchanges to only include 5 exchanges with the highest amount
    aggregating similar exchanges to different compartments.

    NOTE: Units may not be comparable.

    Arguments:
    exchanges -- Array of exchange dictionaries
    """
    if exchanges:
        exchanges = DataFrame(exchanges)

        exchanges = exchanges.groupby(['name', 'unit_name'],
                                      as_index=False)['amount'].sum()
        exchanges = exchanges.nlargest(5, 'amount')

        exchanges = exchanges.to_dict('records')

    return exchanges

filter = Blueprint('filter', __name__)
@filter.route('/filter', methods=['POST'])
def filter_activity():
    """API endpoint accepting a jsonified activity object and filtering it as
    required by specifications.
    """
    activity = request.get_json()

    activity['exchanges']['by_products'] = \
        filter_by_products(activity['exchanges']['by_products'])
    activity['exchanges']['from_technosphere'] = \
        filter_exchanges(activity['exchanges']['from_technosphere'])
    activity['exchanges']['from_environment'] = \
        filter_exchanges(activity['exchanges']['from_environment'])
    activity['exchanges']['to_environment'] = \
        filter_exchanges(activity['exchanges']['to_environment'])

    # return response as json
    return jsonify(activity)
