from sqlalchemy import Column,String,DateTime,JSON
from dao import Base

class NewsSummary(Base):
    __tablename__ = 'news_summary'
    article_id = Column(String(20),primary_key=True)
    title = Column(String(50))
    summary = Column(String(3000))
    kw = Column(JSON)
    publish_time = Column(DateTime)
    kw_virtual = Column(String(255),primary_key=True)

    def __init__(self,article_id,title,summary,kw,publish_time):
        self.article_id = article_id
        self.title = title
        self.summary = summary
        self.kw = kw
        self.publish_time = publish_time