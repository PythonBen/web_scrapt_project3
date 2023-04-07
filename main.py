from utils.extract import extract_full_body_html
from utils.parse import parse_raw_attribute
from config.tools import get_config
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from utils.process import format_and_transform

if __name__ == "__main__":
    config  = get_config()
    html = extract_full_body_html(from_url=config.get("url"), wait_for=config.get("container").get("selector"))
    tree = HTMLParser(html)

    divs = tree.css(config.get("container").get("selector"))

    print(len(divs))

    for d in divs:
        attrs  = parse_raw_attribute(d, config.get('item'))
        attrs = format_and_transform(attrs)
        # postprocessing notes:
        # title -> ok
        # thumbail: <Node img>
        # tags: first 5 from the list
        # relase date: reformat to yyyy-mm-dd
        # review_score: ok
        # review_by: extract digit only
        # price_currency: split by space, get second
        # sale price: split by space, get second


        # title = d.css_first('div[class*="StoreSaleWidgetTitle"]').text()
        # thumbnail = d.css_first('img[class*="CapsuleImage"]').attributes.get("src")
        # tags = [a.text() for a in d.css('div[class*="StoreSaleWidgetTag"] > a')[:5]]
        # release_date = d.css_first('div[class*="WidgetReleaseDateAndPlatformCtn"] > div[class*="StoreSaleWidgetRelease"]').text()
        # review_score = d.css_first('div[class*="ReviewScoreValue"] > div').text()
        # reviewed_by = d.css_first('div[class*="ReviewScoreCount"]').text()
        # sale_price = d.css_first('div[class*="StoreSalePriceBox"]').text()
        # original_price = d.css_first('div[class*="StoreOriginalPrice"]').text()
        # discount = d.css_first('div[class*="StoreSaleDiscountBox"]').text()
        # attrs = {
        #         "title": title,
        #         "review_score": review_score,
        #         "reviewed_by": reviewed_by,
        #         "release_date": release_date,
        #         "tags": tags,
        #         "thumbail": thumbnail,
        #         "original_price": original_price,
        #         "sale_price": sale_price,
        #         "discount": discount
        #
        #     }
        print(attrs)
