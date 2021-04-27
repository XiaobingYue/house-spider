# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, Index, String, TIMESTAMP, Text, text, create_engine
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata


class City(Base):
    __tablename__ = 'city'

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    code = Column(String(32), nullable=False, unique=True)
    geo_code = Column(String(8))
    province_id = Column(INTEGER(11))
    province_name = Column(String(32), nullable=False)
    second_hand = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='是否有二手房')
    longitude = Column(DECIMAL(14, 6), comment='经度')
    latitude = Column(DECIMAL(14, 6), comment='纬度')


class CityHouseDealStat(Base):
    __tablename__ = 'city_house_deal_stat'

    id = Column(INTEGER(10), primary_key=True)
    deal_year = Column(INTEGER(11), comment='成交年')
    deal_month = Column(TINYINT(4), comment='成交月')
    city_name = Column(String(32), nullable=False, comment='城市')
    city_code = Column(String(32), nullable=False, server_default=text("'zz'"), comment='城市码')
    county_name = Column(String(32), comment='区县')
    county_code = Column(String(32), nullable=False, comment='区县码')
    deal_count = Column(INTEGER(11))
    deal_area = Column(DECIMAL(16, 2))
    deal_avg_price = Column(DECIMAL(16, 2))
    second_count = Column(INTEGER(11))
    second_area = Column(DECIMAL(16, 2))
    second_avg_price = Column(DECIMAL(16, 2))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')


class Community(Base):
    __tablename__ = 'community'

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(128), comment='小区名称')
    ninety_days_deal_num = Column(INTEGER(11), comment='90天成交数')
    deal_num = Column(INTEGER(11), comment='成交数,链家只有90成交数，这个是自己统计到的总成交数')
    on_rent_num = Column(INTEGER(11), comment='在租数')
    on_sale_num = Column(INTEGER(11), comment='在售数')
    completion_year = Column(INTEGER(10), comment='建成年份')
    reference_price = Column(DECIMAL(14, 2), comment='参考价')
    lianjia_id = Column(String(32), unique=True, comment='链家小区id')
    page_no = Column(INTEGER(10), comment='页码')
    building_type = Column(String(256), comment='建造类型')
    property_fee = Column(String(64), comment='物业费')
    property_company = Column(String(128), comment='物业公司')
    develop_company = Column(String(128), comment='开发商')
    building_num = Column(INTEGER(11), comment='楼栋总数')
    house_num = Column(INTEGER(11), comment='房屋总数')
    city_name = Column(String(32), comment='城市名')
    city_code = Column(String(32), nullable=False, comment='城市码')
    county_name = Column(String(32), comment='区县名')
    county_code = Column(String(32), nullable=False, comment='区县码')
    street_name = Column(String(64), comment='街区名')
    street_code = Column(String(64), nullable=False, comment='街区码')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')
    update_day = Column(TINYINT(2), comment='更新日')
    update_hour = Column(TINYINT(2), comment='更新时')
    is_watched = Column(TINYINT(1), server_default=text("'0'"), comment='是否被关注')
    longitude = Column(DECIMAL(14, 11), comment='经度')
    latitude = Column(DECIMAL(14, 11), comment='纬度')
    address = Column(String(256), comment='地址')
    longitude2 = Column(DECIMAL(14, 11))
    latitude2 = Column(DECIMAL(14, 11))


class CommunityHistoryDeal(Base):
    __tablename__ = 'community_history_deal'
    __table_args__ = (
        Index('city_code', 'city_code', 'county_code', 'street_code'),
    )

    id = Column(INTEGER(10), primary_key=True)
    community_id = Column(INTEGER(11))
    lianjia_community_id = Column(String(32))
    lianjia_house_id = Column(String(32), unique=True, comment='链家房源编号')
    model = Column(String(32), comment='房屋格局')
    area = Column(DECIMAL(14, 2), comment='房屋面积')
    face_to = Column(String(32), comment='朝向')
    fitment_situation = Column(String(32), comment='装修情况')
    floor_type = Column(String(32), comment='楼层情况')
    total_floor_num = Column(INTEGER(11), comment='总楼层数')
    completion_year = Column(INTEGER(11), comment='建成年份')
    building_type = Column(String(32), comment='建筑类型')
    deal_unit_price = Column(DECIMAL(14, 2), comment='成交均价')
    five_years = Column(String(32), comment='房屋满五年')
    list_date = Column(Date, comment='挂牌日期')
    list_price = Column(DECIMAL(14, 2), comment='挂牌价')
    deal_price = Column(DECIMAL(14, 2), comment='成交价')
    deal_date = Column(Date, comment='成交日期')
    deal_month = Column(TINYINT(4), comment='成交月')
    deal_year = Column(INTEGER(11), comment='成交年')
    deal_cycle = Column(INTEGER(11), comment='成交周期（天）')
    city_code = Column(String(32), nullable=False, comment='城市码')
    county_code = Column(String(32), nullable=False, comment='区县码')
    street_code = Column(String(64), nullable=False, comment='街区码')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')


class County(Base):
    __tablename__ = 'county'
    __table_args__ = (
        Index('code', 'code', 'city_code', unique=True),
        Index('name', 'name', 'city_name', unique=True)
    )

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(32), nullable=False)
    code = Column(String(64), nullable=False)
    geo_code = Column(String(8))
    city_id = Column(INTEGER(11), nullable=False)
    city_name = Column(String(32), nullable=False)
    city_code = Column(String(32), nullable=False)
    province_id = Column(INTEGER(11), nullable=False)
    province_name = Column(String(32), nullable=False)


class CountyInitRecord(Base):
    __tablename__ = 'county_init_record'

    id = Column(INTEGER(10), primary_key=True)
    county_id = Column(INTEGER(11), nullable=False)
    county_code = Column(String(64), nullable=False)
    county_name = Column(String(64), nullable=False)
    city_id = Column(INTEGER(11), nullable=False)
    city_name = Column(String(32), nullable=False)
    city_code = Column(String(32), nullable=False)
    province_id = Column(INTEGER(11), nullable=False)
    province_name = Column(String(32), nullable=False)
    phase = Column(TINYINT(2), nullable=False, comment='初始化阶段')
    is_pressing = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='是否在处理中')
    community_last_update_time = Column(DateTime, comment='小区最后更新时间')
    deal_history_last_update_time = Column(DateTime, comment='成交记录最后更新时间')
    community_num = Column(INTEGER(11), comment='小区数')
    deal_num = Column(INTEGER(11), comment='成交记录数')
    house_num = Column(INTEGER(11), comment='房源数')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')


class House(Base):
    __tablename__ = 'house'

    id = Column(INTEGER(10), primary_key=True)
    community_id = Column(INTEGER(11))
    lianjia_community_id = Column(String(32))
    lianjia_house_id = Column(String(32), unique=True, comment='链家房源编号')
    model = Column(String(32), comment='房屋格局')
    area = Column(DECIMAL(14, 2), comment='房屋面积')
    face_to = Column(String(32), comment='朝向')
    fitment_situation = Column(String(32), comment='装修情况')
    floor_type = Column(String(32), comment='楼层情况')
    total_floor_num = Column(INTEGER(11), comment='总楼层数')
    completion_year = Column(INTEGER(11), comment='建成年份')
    building_type = Column(String(32), comment='建筑类型')
    villa_tag = Column(String(32), comment='别墅标志')
    follower_num = Column(INTEGER(11), server_default=text("'0'"), comment='关注人数')
    five_years = Column(String(32), comment='房屋满五年')
    list_price = Column(DECIMAL(14, 2), comment='挂牌价')
    unit_price = Column(DECIMAL(14, 2), comment='单价')
    city_code = Column(String(32), nullable=False, comment='城市码')
    county_code = Column(String(32), nullable=False, comment='区县码')
    street_code = Column(String(32), nullable=False, comment='街区码')
    good_tag = Column(String(32), comment='必看好房')
    look_tag = Column(String(32), comment='随时看房')
    inner_area = Column(DECIMAL(14, 2), comment='套内面积')
    elevator_ratio = Column(String(32), comment='梯户比例')
    heating_method = Column(String(32), comment='供暖方式')
    structure = Column(String(32), comment='结构：平层、跃层、错层、复式')
    list_date = Column(Date, comment='挂牌日期')
    last_deal_date = Column(Date, comment='上次交易日期')
    trade_type = Column(String(32), comment='交易权属')
    house_use = Column(String(32), comment='房屋用途；别墅、普通住宅')
    property_type = Column(String(32), comment='产权所属')
    property_permit = Column(String(32), comment='产权证信息')
    guaranty_message = Column(String(128), comment='抵押信息')
    is_deal = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='成交标志')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')


class Province(Base):
    __tablename__ = 'province'

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    geo_code = Column(String(8))


class Street(Base):
    __tablename__ = 'street'
    __table_args__ = (
        Index('code', 'city_code', 'county_code', 'code', unique=True),
        Index('name', 'city_name', 'county_name', 'name', unique=True)
    )

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(32), nullable=False)
    code = Column(String(64), nullable=False, unique=True)
    county_id = Column(INTEGER(11), nullable=False)
    county_code = Column(String(64), nullable=False)
    county_name = Column(String(64), nullable=False)
    city_id = Column(INTEGER(11), nullable=False)
    city_name = Column(String(32), nullable=False)
    city_code = Column(String(32), nullable=False)
    province_id = Column(INTEGER(11), nullable=False)
    province_name = Column(String(32), nullable=False)
    update_day = Column(TINYINT(2), comment='每周几更新新上房源')


class Warning(Base):
    __tablename__ = 'warning'

    id = Column(INTEGER(11), primary_key=True)
    warning = Column(Text)
    Bitcoin_Address = Column(Text)
    Email = Column(Text)


class WatchCommunity(Base):
    __tablename__ = 'watch_community'

    id = Column(INTEGER(10), primary_key=True)
    community_id = Column(INTEGER(11))
    lianjia_community_id = Column(String(32), nullable=False)
    user_id = Column(INTEGER(11), nullable=False, comment='用户id')
    city_code = Column(String(32), nullable=False)
    county_code = Column(String(32), nullable=False)
    street_code = Column(String(64), nullable=False)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')


class WatchHouse(Base):
    __tablename__ = 'watch_house'

    id = Column(INTEGER(10), primary_key=True)
    community_id = Column(INTEGER(11))
    lianjia_community_id = Column(String(32), nullable=False)
    lianjia_house_id = Column(String(32), nullable=False, comment='链家房源编号')
    user_id = Column(INTEGER(11), nullable=False, comment='用户id')
    city_code = Column(String(32), nullable=False)
    county_code = Column(String(32), nullable=False)
    street_code = Column(String(64), nullable=False)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='最后更新时间')


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:123456@47.104.254.199:3306/fxgmall')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
