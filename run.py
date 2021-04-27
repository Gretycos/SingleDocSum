# -*- coding:utf-8 -*-
"""
Usage:
    run.py [options]

Options:
    -h --help                               show this screen.
    --days=<int>                            load data from days ago [default: 1]
    --all
"""
import json
from docopt import docopt
import time
from datetime import datetime, timedelta
from dao import load_session
from dao.News import News
from dao.NewsInfo import NewsInfo
from dao.NewsSummary import NewsSummary
from util import getAccessToken, getSummary
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def parseDoc(access_token,days):
    logger.info("正在加载数据...")
    target_date = datetime.now().date() + timedelta(days=-days)
    with open("../TopicDiscovery/predict/top/{}.json".format(target_date),'r',encoding='utf-8') as f:
        doc_topic = json.load(f)
    logger.info(doc_topic)
    logger.info("正在处理数据...按照一定比例提取摘要")
    session = load_session()
    for item in doc_topic:
        for row in session.query(News.content,News.title,News.publish_time).filter(News.article_id == item['article_id']):
            content = row[0] if len(row[0])<=3000 else row[0][:3000]
            title = row[1]
            publish_time = row[2]
            if len(content) > 2100:
                summary = getSummary(access_token,title,content,900)
            elif 1500 < len(content) <= 2100:
                summary = getSummary(access_token,title,content,len(content) * 0.25 + 375)
            elif 600 < len(content) <= 1500:
                summary = getSummary(access_token, title, content, len(content) * 0.5)
            else:
                summary = getSummary(access_token, title, content, 300)
            new_news_summary = NewsSummary(item['article_id'],title,summary,item['kw'],publish_time)
            logger.info("[article_id='{}'; title='{}'; summary='{}'; kw='{}'; publish_time='{}']".format(item['article_id'],title,summary,item['kw'],publish_time))
            time.sleep(1)
            try:
                logger.info("提交[article_id={}]到数据库中".format(item['article_id']))
                session.merge(new_news_summary)
                logger.info("提交[article_id={}成功".format(item['article_id']))
            except Exception as e:
                session.rollback()
                logger.error("提交失败，出现异常，回滚。原因:{}".format(e))
    session.commit()
    session.close()
    logger.info("处理数据完成")

def aggregate(days):
    session = load_session()

    # cursor = session.execute("select DATE_FORMAT(publish_time,'%Y-%m-%d') as d, count(article_id) as nums "
    #                          "from news "
    #                          "where publish_time > '2021-01-29' "
    #                          "group by DATE_FORMAT(publish_time,'%Y-%m-%d') "
    #                          "order by d desc ")

    target_date = datetime.now().date() + timedelta(days=-days)
    cursor = session.execute("select DATE_FORMAT(publish_time,'%Y-%m-%d') as d, count(article_id) as nums "
                             "from news "
                             "where DATE_FORMAT(publish_time,'%Y-%m-%d') = '{}' "
                             "group by DATE_FORMAT(publish_time,'%Y-%m-%d') "
                             "order by d desc ".format(target_date))

    items = cursor.fetchall()
    data = {}
    for item in items:
        data['{}'.format(item[0])] = {
            'kw_date': [],
            'nums': item[1]
        }

    cursor = session.execute("select kw "
                             "from news_summary "
                             "where DATE_FORMAT(publish_time,'%Y-%m-%d') = '{}' "
                             "order by publish_time desc".format(target_date))
    kws = cursor.fetchall()
    kw_oneday = []
    for kw in kws:
        kw_oneday.append(json.loads(kw[0]))
    data['{}'.format(target_date)]['kw_date'] = kw_oneday

    # for d in range(1,days):
    #     target_date = datetime.now().date() + timedelta(days=-d)
    #     cursor = session.execute("select kw "
    #                              "from news_summary "
    #                              "where DATE_FORMAT(publish_time,'%Y-%m-%d') = '{}' "
    #                              "order by publish_time desc".format(target_date))
    #     kws = cursor.fetchall()
    #     kw_oneday = []
    #     for kw in kws:
    #         kw_oneday.append(json.loads(kw[0]))
    #     data['{}'.format(target_date)]['kw_date'] = kw_oneday

    for key in data.keys():
        news_info = NewsInfo(key,data[key]['kw_date'],data[key]['nums'])
        try:
            session.merge(news_info)
            logger.info("提交汇总")
        except Exception as e:
            logger.error("回滚汇总: {}".format(e))
            session.rollback()

    session.commit()
    session.close()

def remove_data(days):
    session = load_session()
    target_date = datetime.now().date() + timedelta(days=-days)
    try:
        session.execute("delete from news_summary "
                        "where DATE_FORMAT(publish_time,'%Y-%m-%d') = '{}'".format(target_date))
        session.execute("delete from news_info "
                        "where publish_date = '{}'".format(target_date))
    except Exception as e:
        logger.error("回滚清除: {}".format(e))
        session.rollback()
    session.commit()
    session.close()


def main():
    args = docopt(__doc__)
    # logger.info(args)
    access_token = getAccessToken()
    for day in range(int(args['--days']),0,-1):
        if args['--all']:
            remove_data(day)
        parseDoc(access_token, day)
        aggregate(day)


if __name__ == '__main__':
    main()