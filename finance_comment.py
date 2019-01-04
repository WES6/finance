# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, String, create_engine, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
from bs4 import BeautifulSoup

page = 22

if __name__ == "__main__":
    # 创建对象的基类:
    Base = declarative_base()

    # 定义对象:
    class Comment(Base):
        # 表的名字:
        __tablename__ = 'comment'

        # 表的结构:
        comment_id = Column(Integer(), primary_key=True, autoincrement=True)
        comment_name = Column(String(255), index=True)
        comment_date = Column(DateTime)
        comment_link = Column(String(255))
        comment_text = Column(Text())

    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:000000@localhost:3306/list')
    Base.metadata.create_all(engine)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    for tt in range(page):
        tt += 1
        print(tt)
        rep1 = requests.get("http://finance.sina.com.cn/roll/index.d.html?cid=56613&page="+str(tt))
        rep1.encoding = "UTF-8"
        soup1 = BeautifulSoup(rep1.text, "lxml")
        for item1 in soup1.find_all(class_="list_009"):
            for subitem1 in item1.find_all("li"):
                a1 = subitem1.find("a").attrs["href"]
                n1 = subitem1.find("a").string
                dt1 = subitem1.find("span").string
                d1 = datetime.strptime("2018"+dt1, '%Y(%m月%d日 %H:%M)')
                str1 = ""
                subrep1 = requests.get(a1)
                subrep1.encoding = "UTF-8"
                subsoup1 = BeautifulSoup(subrep1.text, "lxml")
                for pp in subsoup1.find_all("p"):
                    if pp.string is None or pp.string == "【线索征集令！】你吐槽，我倾听；您爆料，我报道！在这里，" \
                                                         "我们将回应你的诉求，正视你的无奈。新浪财经爆料线索征集启动，" \
                                                         "欢迎广大网友积极“倾诉与吐槽”！爆料联系邮箱：finance_biz@sina.com"\
                            or pp.string == "Copyright © 1996-2018 SINA Corporation" \
                            or pp.string == "新浪财经意见反馈留言板" \
                            or pp.string == "电话：400-690-0000 欢迎批评指正" \
                            or pp.string == "责任编辑：陈悠然 SF104" \
                            or pp.string == "24小时滚动播报最新的财经资讯和视频，更多粉丝福利扫描二维码关注（sinafinance）":
                        pass
                    else:
                        str1 += pp.string
                # try:
                print(str(n1))
                session = DBSession()
                new_comment = Comment(comment_name=str(n1), comment_date=d1, comment_link=a1, comment_text=str1)
                session.add(new_comment)
                session.commit()
                session.close()
                # except BaseException:
                #     print(BaseException)
