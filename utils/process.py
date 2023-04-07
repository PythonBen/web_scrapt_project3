from selectolax.parser import Node
from datetime import datetime
import re
import pandas as pd

def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function expects a selectolax node to be provvided")
    return node.attributes.get(attr)

def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]

#Mar 13 2022 -> 2022-03-13
#%b %d %Y
def reformat_date(date_raw: str, input_format: str = "%b-%d,-%Y", output_format:str = "%Y-%m-%d"):
    dt_obj = datetime.strptime(date_raw, input_format)
    return datetime.strftime(dt_obj, output_format)

def regex(input_str: str, pattern: str, do_what: str = "findall"):
    if do_what == "findall":
        return re.findall(pattern, input_str)
    elif do_what == "split":
        return re.split(pattern, input_str)
    else:
        raise ValueError("The function expects 'findall' or 'split' to be provided")

#def price_curr(input_str: str):
#    return input_str[-1]
def format_and_transform(attrs: dict):

    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),
        "reviewed_by": lambda raw: int(''.join(regex(raw, r'\d+'))),
        #"price_currency": lambda raw: regex(raw, r'\s', "split")[0],
        "price_currency": lambda raw: raw[-1],
        "sale_price": lambda raw: float((regex(raw, r'\d+,\d+', "findall")[0]).replace(',','.')),
        "original_price": lambda raw: float((regex(raw, r'\d+,\d+', "findall")[0]).replace(',', '.'))

    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])

    attrs["discount_pct"] = round(100 * (attrs["original_price"] - attrs["sale_price"])/(attrs["original_price"]), 2)
    return attrs

def save_to_file(filename="extract", data: list[dict] =None):
    if data is None:
        raise ValueError("This function expects data to be provided as a list of dictionnaries")
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
