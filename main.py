import json
from bs4 import BeautifulSoup
from util.utils import *
from tg.bot import *
from db.db_connect import *
import pandas as pd
from urllib import parse
import traceback

QUERY_LIST = json.loads(os.environ['QUERY_LIST'])
URL_HEAD = 'https://www.facebook.com/marketplace/sanjose/search/?query='
CLASS_NAME = "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6"
ALL_ADS_CLASS_NAME = "x1xfsgkm xqmdsaz x1cnzs8 x4v5mdz xjfs22q"


def main():
    # open page
    for query in QUERY_LIST:
        url = URL_HEAD + parse.quote(query)
        content = open_page(url)

        df = pd.DataFrame(columns=['ad_price', 'ad_name', 'ad_image_link', 'ad_link'])

        soup = BeautifulSoup(content, 'lxml')

        all_ads_div = soup.find_all("div", class_=ALL_ADS_CLASS_NAME)
        area_ads_div = all_ads_div[0].findChild().find_all("div", class_=CLASS_NAME)

        for p in area_ads_div:
            if check_if_exist(p):
                text_div = get_text_div(p)

                image_link = get_image_div(p)
                link = get_link(text_div[0])
                name = text_div[1].get_text()
                price = get_price(text_div)
                df.loc[len(df.index)] = [price, name, image_link, link]

        # Start DB connection
        print('df from FB = {}'.format(len(df.index)))
        print(df.head(10))
        table_name = query.replace(" ", "_")
        try:
            db = db_connect(table_name)
            df_from_db = read_from_db(db, table_name)
            df_final = df.merge(df_from_db, indicator='i', how='outer', on='ad_link').query('i == "left_only"').drop(
                ['i', 'ad_price_y', 'ad_name_y', 'ad_image_link_y'], axis=1)
            df_final.rename(
                columns={'ad_price_x': 'ad_price', 'ad_name_x': 'ad_name', 'ad_image_link_x': 'ad_image_link'},
                inplace=True)
            tg_message = "Query= {}, FB ads = {}, new ads = {}".format(query, len(df.index), len(df_final.index))
            send_message_tg(tg_message)
            for index, row in df_final.iterrows():
                text = row['ad_price'] + '\n' + row['ad_name'] + '\n' + row['ad_link']
                send_tg(text, row['ad_image_link'])
            print('df to be inserted to db = {}'.format(len(df_final.index)))
            print(df_final.head(10))
            save_df(df_final, db, table_name)
        except Exception:
            traceback.print_exc()
        finally:
            df_final.to_csv("{}.csv".format(table_name), index=False)
            close_db(db)


if __name__ == "__main__":
    main()
