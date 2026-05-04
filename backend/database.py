from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# اسم ملف قاعدة البيانات اللي هيتكريت
SQLALCHEMY_DATABASE_URL = "sqlite:///./tumor_reports.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# تصميم جدول التقارير
class ReportDB(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, index=True)
    case_name = Column(String)
    date = Column(String)
    data = Column(Text) # هنحفظ تفاصيل التقرير هنا كـ JSON

# إنشاء الجدول في الملف
Base.metadata.create_all(bind=engine)