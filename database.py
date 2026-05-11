from sqlalchemy import create_engine
import cryptography
database_url = "mysql+pymysql://root:Gersolo2009.@localhost:3306/ai_news_bot"
engine = create_engine(database_url)
connection = engine.connect()
print("Контакт есть")