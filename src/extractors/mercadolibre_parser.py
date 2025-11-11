thonimport json

def parse_product_data(product):
    return {
        'unique_id': product['metadata']['id'],
        'title': product['components'][0]['title']['text'],
        'price': product['components'][1]['price']['current_price']['value'],
        'previous_price': product['components'][1]['price'].get('previous_price', {}).get('value', 'N/A'),
        'shipping': product['components'][2]['shipping']['text'],
        'url': product['metadata']['url'],
        'images': [img['id'] for img in product['pictures']['pictures']]
    }

def parse_json_data(input_json):
    parsed_data = []
    try:
        products = json.loads(input_json)
        for product in products:
            parsed_product = parse_product_data(product)
            parsed_data.append(parsed_product)
    except Exception as e:
        print(f"Error parsing data: {e}")
    return parsed_data