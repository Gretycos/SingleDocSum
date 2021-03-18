from sqlalchemy import Column,JSON,INT,DATE
from dao import Base

class NewsInfo(Base):
    __tablename__ = 'news_info'
    publish_date = Column(DATE,primary_key=True)
    kw_date = Column(JSON)
    nums = Column(INT)

    def __init__(self,publish_date,kw_date,nums):
        self.publish_date = publish_date
        self.kw_date = kw_date
        self.nums = nums
