from datetime import datetime
import json
from urllib import request
from urllib.error import URLError

from bs4 import BeautifulSoup

from models import DBSession, County, CountyInitRecord, Street, Community

COMMUNITY_LIST = 'https://{0}.ke.com/xiaoqu/{1}/pg{2}/'

COMMUNITY_DETAIL = 'https://{0}.ke.com/xiaoqu/{1}/'


def get_content(to_url):
    req = request.Request(
        url=to_url
    )
    try:
        response = request.urlopen(req, timeout=15)
        return response.read()
    except URLError as e:
        print('获取html失败：{%s}' % e.reason)
    return None


def open_file():
    with open('house.html', 'r', encoding='utf-8') as f:
        html = f.read()
        return html


def total_page(html):
    bs = BeautifulSoup(html, 'html.parser')
    t = bs.find('div', attrs={'class': 'page-box house-lst-page-box'})
    if t:
        page_info = json.loads(t['page-data'])
        return int(page_info.get('totalPage', 0))
    else:
        return 0


def parse_list(html):
    bs = BeautifulSoup(html, 'html.parser')
    ul = bs.find('ul', attrs={'class': 'listContent'})
    ui_list = ul.find_all('li')
    community_list = []
    for ui in ui_list:
        name = ui.find('div', attrs={'class': 'title'}).find('a')['title']
        a_ = ui.find('div', attrs={'class': 'houseInfo'}).find_all('a')
        recent_sale_count = str2num(a_[0].string.replace('90', ''))
        rent_count = str2num(a_[-1].string)
        recent_sale_price = ui.find('div', attrs={'class': 'xiaoquListItemPrice'}).find('span').string
        if recent_sale_price != '暂无数据':
            recent_sale_price = int(recent_sale_price)
        else:
            recent_sale_price = 0
        sale_count = ui.find('div', attrs={'class': 'xiaoquListItemSellCount'}).find('span').string
        lianjia_id = ui['data-id']
        print('小区名称：%s,90天成交量： %s,在租数量：%s,在售价格：%s,在售数量：%s,；lianjiaId：%s' %
              (name, recent_sale_count, rent_count, recent_sale_price, sale_count, lianjia_id))
        community_list.append(Community(name=name, on_rent_num=rent_count, on_sale_num=recent_sale_count,
                                        ninety_days_deal_num=recent_sale_count, lianjia_id=lianjia_id,
                                        reference_price=recent_sale_price))
    return community_list


def str2num(str_):
    return int(''.join(x for x in str_.strip() if x.isdigit()))


def init_or_update_county_info():
    county_init_list = session.query(CountyInitRecord).all()
    for init_record in county_init_list:
        init_one_county(init_record)


def init_one_street_community(city_code, county_code, street):
    html = get_content(COMMUNITY_LIST.format(city_code, street.code, '1'))
    if not html:
        return
    total = total_page(html)
    print('街道名：%s,总页数：%s' % (street.name, total))
    if total == 0:
        return
    for i in range(0, total):
        i = i + 1
        htm = get_content(COMMUNITY_LIST.format(city_code, street.code, i))
        if not htm:
            return
        community_list = parse_list(htm)
        print('本页解析出%s条小区数据' % len(community_list))
        for c in community_list:
            c.city_code = city_code
            c.county_code = county_code
            c.street_code = street.code
            db_community = session.query(Community).filter(Community.lianjia_id == c.lianjia_id).all()
            if db_community:
                session \
                    .query(Community) \
                    .filter(Community.lianjia_id == c.lianjia_id) \
                    .update({'on_rent_num': c.on_rent_num,
                             'on_sale_num': c.on_sale_num,
                             'ninety_days_deal_num': c.ninety_days_deal_num,
                             'name': c.name,
                             'reference_price': c.reference_price})
            else:
                session.add(c)


def init_one_county(init_record: CountyInitRecord):
    county_code = init_record.county_code
    city_code = init_record.city_code
    street_list = session.query(Street).filter(Street.county_code == county_code, Street.city_code == city_code).all()
    print('city:[%s],county:[%s],查询出[%s]条街道数量' % (init_record.city_name, init_record.county_name, len(street_list)))
    for street in street_list:
        init_one_street_community(city_code, county_code, street)


def parse_detail(lianjia_id, html):
    community = Community(lianjia_id=lianjia_id)
    item_types = {
        '建筑类型': 'building_type',
        '物业费用': 'property_fee',
        '物业公司': 'property_company',
        '开发商': 'develop_company',
        '楼栋总数': 'building_num',
        '房屋总数': 'house_num'
    }
    bs = BeautifulSoup(html, 'html.parser')
    info_items = bs.find_all('div', attrs={'class', 'xiaoquInfoItem'})
    for item in info_items:
        span_list = item.find_all('span')

        if len(span_list) == 2 and span_list[0].string in item_types:
            pro_name = item_types.get(span_list[0].string)
            pro_value = span_list[-1].string.strip()
            if 'building_num' == pro_name or 'house_num' == pro_name:
                pro_value = str2num(pro_value)
            community.__setattr__(pro_name, pro_value)
        else:
            print('解析小区基本信息异常，原始html：[%s]' % span_list)
    return community


def perfect_community_info(city_code, lianjia_id):
    html = get_content(COMMUNITY_DETAIL.format(city_code, lianjia_id))
    if not html:
        return
    community = parse_detail(lianjia_id, html)
    db_community = session.query(Community).filter(Community.lianjia_id == lianjia_id).one()
    if db_community:
        session \
            .query(Community) \
            .filter(Community.lianjia_id == community.lianjia_id) \
            .update({'building_type': community.building_type,
                     'property_fee': community.property_fee,
                     'property_company': community.property_company,
                     'develop_company': community.develop_company,
                     'building_num': community.building_num,
                     'house_num': community.house_num
                     })
    else:
        session.add(community)


if __name__ == '__main__':
    session = DBSession()
    # initRecord = CountyInitRecord(county_id=1852,
    #                               county_code='gaoxin9',
    #                               county_name='高新区',
    #                               city_id=56,
    #                               city_name='郑州',
    #                               city_code='zz',
    #                               province_id=12,
    #                               province_name='河南',
    #                               phase=1,
    #                               deal_history_last_update_time=datetime.now(),
    #                               community_last_update_time=datetime.now()
    #                               )
    # session.add(initRecord)
    # county_init_list = session.query(CountyInitRecord).all()
    # session.commit()
    # init_or_update_county_info()
    c_list = session.query(Community).all()
    for c in c_list:
        perfect_community_info(c.city_code, c.lianjia_id)
    session.commit()
    session.close()
    # print(len(county_init_list))
