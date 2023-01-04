import json
import traceback
from bs4 import BeautifulSoup
from util.utils import *
from tg.bot import *
from urllib import parse
from db.base import Session, engine, Base
from models.ad import Ad

QUERY_LIST = json.loads(os.environ['QUERY_LIST'])
URL_HEAD = 'https://www.facebook.com/marketplace/sanjose/search/?query='
CLASS_NAME = "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6"
ALL_ADS_CLASS_NAME = "x1xfsgkm xqmdsaz x1cnzs8 x4v5mdz xjfs22q"


def main():
    try:
        # 2 - generate database schema
        Base.metadata.create_all(engine)

        # 3 - create a new session
        session = Session()

        # open page
        for query in QUERY_LIST:
            url = URL_HEAD + parse.quote(query)
            content = open_page(url)

            soup = BeautifulSoup(content, 'lxml')

            all_ads_div = soup.find_all("div", class_=ALL_ADS_CLASS_NAME)
            area_ads_div = all_ads_div[0].findChild().find_all("div", class_=CLASS_NAME)

            ads_from_fb = []
            for p in area_ads_div:
                if check_if_exist(p):
		    try:
                    	text_div = get_text_div(p)

                    	image_link = get_image_div(p)
                    	link = get_link(text_div[0])
                    	name = text_div[1].get_text()
                    	price = get_price(text_div)
                    	ad = Ad(query, name, price, image_link, link)
                    	ads_from_fb.append(ad)
		    except Exception:
		   	traceback.print_exc()

            print('Ads from FB = {}'.format(len(ads_from_fb)))
            try:
                ads_from_db = session.query(Ad).all()
                ads_new = []
                ads_links = {ad.link for ad in ads_from_db}

                for ad in ads_from_fb:
                    if ad.link not in ads_links:
                        ads_new.append(ad)

                tg_message = "Query= {}, FB ads = {}, new Ads = {}".format(query, len(ads_from_fb), len(ads_new))
                send_message_tg(tg_message)
                for ad in ads_new:
                    text = ad.price + '\n' + ad.name + '\n' + ad.link
                    send_tg(text, ad.image)
                print('Ads to be inserted to db = {}'.format(len(ads_new)))
                session.bulk_save_objects(ads_new)
                session.commit()
            except Exception:
                traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    main()
