from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# 1. .env에서 DATABASE_URL 불러오기
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 3. 테이블 생성 SQL 정의
create_tables_sql = """
CREATE TABLE IF NOT EXISTS movie_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mname_kor VARCHAR(255) NOT NULL,
    mname_eng VARCHAR(255),
    year INT,
    type VARCHAR(100),
    state VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS movie_nation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mid INT NOT NULL,   
    nation VARCHAR(100) NOT NULL,
    FOREIGN KEY (mid) REFERENCES movie_info(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS movie_genre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mid INT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    FOREIGN KEY (mid) REFERENCES movie_info(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS movie_company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mid INT NOT NULL,
    company VARCHAR(255) NOT NULL,
    FOREIGN KEY (mid) REFERENCES movie_info(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS director (
    did INT AUTO_INCREMENT PRIMARY KEY,
    dname VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS director_movie (
    did INT NOT NULL,
    mid INT NOT NULL,
    PRIMARY KEY (did, mid),
    FOREIGN KEY (did) REFERENCES director(did) ON DELETE CASCADE,
    FOREIGN KEY (mid) REFERENCES movie_info(id) ON DELETE CASCADE
);
"""

# 4. 실행
with engine.begin() as conn:
    for stmt in create_tables_sql.strip().split(";"):
        if stmt.strip():
            conn.execute(text(stmt))

print("✅ 모든 테이블이 생성되었습니다.")
