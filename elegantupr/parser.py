from flask import Blueprint, jsonify, request
from lxml import etree

def get_activity_name(tree):
    """Get activity name from XML tree.

    Arguments:
    tree -- XML tree
    """
    return tree.findtext('//{*}activityName')

def get_geography_shortname(tree):
    """Get geography shortname from XML tree.

    Arguments:
    tree -- XML tree
    """
    return tree.findtext('//{*}geography/{*}shortname')

def get_exchange(exchange):
    """Get exchange properties as readable dictionary.

    Arguments:
    exchange -- XML element
    """
    production_volume_amount = exchange.get('productionVolumeAmount')

    if production_volume_amount:
        production_volume_amount = float(production_volume_amount)

    return {'amount': float(exchange.get('amount')),
            'production_volume_amount': production_volume_amount,
            'name': exchange.findtext('./{*}name'),
            'unit_name': exchange.findtext('./{*}unitName'),
            'compartment': exchange.findtext('./{*}compartment/{*}compartment')}

def get_exchanges(tree, input_groups=None, output_groups=None):
    """Get exchanges by groups from XML tree.

    Arguments:
    tree -- XML tree
    input_groups -- Array with groups of input flows (default None)
    output_groups -- Array with groups of output flows (default None)
    """
    if input_groups:
        exchanges = [ get_exchange(exchange) for exchange
                          in tree.iterfind('//{*}inputGroup/..')
                          if exchange.findtext('./{*}inputGroup')
                          in input_groups ]

    if output_groups:
        exchanges = [ get_exchange(exchange) for exchange
                          in tree.iterfind('//{*}outputGroup/..')
                          if exchange.findtext('./{*}outputGroup')
                          in output_groups ]

    return exchanges

parser = Blueprint('parser', __name__)
@parser.route('/parser', methods=['POST'])
def parse_ecospold2():
    """API endpoint accepting a ecospold2 file upload and parsing it into a
    readable object including name, geography shortname and exchanges.
    """
    ecospold2 = request.files['ecospold2']

    tree = etree.parse(ecospold2)

    activity = {'name': get_activity_name(tree),
                'geography_shortname': get_geography_shortname(tree),
                'exchanges': {
                    'reference_product':
                        get_exchanges(tree, output_groups=['0']),
                    'by_products': get_exchanges(tree, output_groups=['2']),
                    'from_technosphere':
                        get_exchanges(tree, input_groups=['1','2','3','5']),
                    'from_environment': get_exchanges(tree, input_groups=['4']),
                    'to_environment': get_exchanges(tree, output_groups=['4'])
               }}

    # return response as json
    return jsonify(activity)
