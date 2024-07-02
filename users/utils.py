import requests
from lxml import etree
import logging
from decimal import Decimal
import json

logger = logging.getLogger(__name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def send_invoice_peppol(invoice_data):
    headers = {
        'Authorization': 'Bearer TtrvB9jOIvZGrJfg-H4tq9X5u_w9PGK4YEq6i4Gp_B0',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            "https://api.storecove.com/api/v2/document_submissions",
            data=json.dumps(invoice_data, cls=DecimalEncoder),
            headers=headers
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        logger.debug(f"Response content: {response.content}")
        raise
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        raise   