from sqlalchemy import create_engine,String,JSON,DateTime,func,Float
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
s_engine = create_engine("postgresql+psycopg2://postgres:Password@localhost:localhost/databasename",echo=False)
Base = declarative_base()
class Numbers(Base):
    __tablename__ = 'Numbers'
    number: Mapped[str] = mapped_column(String)
    last_10_comments: Mapped[dict] = mapped_column(JSON)
    answer_ai: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    created_at: Mapped[str] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    def __repr__(self):
        return f"<Numbers(number={self.number},last_10_comments={self.last_10_comments},answer_ai={self.answer_ai},rating={self.rating},created_at={self.created_at})>"
class AllComments(Base):
    __tablename__ = 'AllComments'
    comment: Mapped[str] = mapped_column(String)
    def __repr__(self):
        return f"<AllComments(comment={self.comment})>"
a_engine = create_async_engine("postgresql+psycopg2://postgres:Password@localhost:localhost/databasename",echo=False)
Session = sessionmaker(a_engine,class_=AsyncSession,expire_on_commit=False)