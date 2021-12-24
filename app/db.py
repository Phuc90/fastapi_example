# import psycopg2
# from psycopg2.extras import RealDictCursor


# try:
#     conn = psycopg2.connect(host='localhost',database='dvdrental',user='postgres',password='1234',cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('successful connection')
# except Exception as e:
#     print(e)

# cursor.execute("""with base_table as (
# 	select p.payment_id, p.payment_date, p.amount, p.customer_id,
# 	row_number() over(partition by p.customer_id order by p.payment_date) as row_rank_cust,
# 	lag(p.amount,3) over() as sales_lag_3days
# 	from payment p
# )

# select p.customer_id, p.payment_date, p.amount, p.row_rank_cust, p.sales_lag_3days,
# (select avg(p2.amount) from payment p2 where p2.payment_date between p.payment_date
# and p.payment_date + interval '7 days')fwd_7days,
# (select avg(p2.amount) from payment p2 where  p2.payment_date between p.payment_date
# and p.payment_date + interval '14 days')fwd_14days
# from base_table p 
# where p.row_rank_cust in (1,2,3)""")
# data = cursor.fetchall()


# print(data)



#complete connection 


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    return {"data":posts}



