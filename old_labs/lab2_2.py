import json

filename = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        "Item": item,
        "Quantity": quantity,
        "Price": price,
        "Buyer": buyer,
        "Date": date
    }
    with open(filename, 'w') as f_n:
        json.dump(dict_to_json, f_n, sort_keys=True, indent=4)


if __name__ == '__main__':
    write_order_to_json('Item1', 3, 150.00, 'Alex', '2019-01-01')
