import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# 1. 환경변수 로드 + DB 연결
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# 2. Excel 병합
df1 = pd.read_excel('movie_data.xls', sheet_name='영화정보 리스트', header=4)
df2 = pd.read_excel('movie_data.xls', sheet_name='영화정보 리스트_2', header=None)
df2.columns = df1.columns
df = pd.concat([df1, df2], ignore_index=True)
df = df.fillna('').applymap(lambda x: x.strip() if isinstance(x, str) else x)

# 3. INSERT
director_cache = {}
batch_size = 1000
total = len(df)

try:
    with engine.begin() as conn:
        for i in range(0, total, batch_size):
            print(f"▶ Processing rows {i+1} to {min(i+batch_size, total)}")
            batch = df.iloc[i:i + batch_size]

            for _, row in batch.iterrows():
                mname_kor = row['영화명']
                mname_eng = row['영화명(영문)']
                year = int(float(row['제작연도'])) if not pd.isna(row['제작연도']) and row['제작연도'] != '' else None
                mtype = row['유형']
                state = row['제작상태']
                nations = [x.strip() for x in row['제작국가'].split(',') if x.strip()]
                genres = [x.strip() for x in row['장르'].split(',') if x.strip()]
                companies = [x.strip() for x in row['제작사'].split(',') if x.strip()]
                directors = [x.strip() for x in row['감독'].split(',') if x.strip()]

                # 1. movie_info 삽입
                result = conn.execute(text("""
                    INSERT INTO movie_info (mname_kor, mname_eng, year, type, state)
                    VALUES (:kor, :eng, :year, :type, :state)
                """), {
                    "kor": mname_kor,
                    "eng": mname_eng,
                    "year": year,
                    "type": mtype,
                    "state": state
                })
                mid = result.lastrowid

                # 2. movie_nation
                for nation in nations:
                    conn.execute(text("INSERT INTO movie_nation (mid, nation) VALUES (:mid, :nation)"), {"mid": mid, "nation": nation})

                # 3. movie_genre
                for genre in genres:
                    conn.execute(text("INSERT INTO movie_genre (mid, genre) VALUES (:mid, :genre)"), {"mid": mid, "genre": genre})

                # 4. movie_company
                for company in companies:
                    conn.execute(text("INSERT INTO movie_company (mid, company) VALUES (:mid, :company)"), {"mid": mid, "company": company})

                # 5. director + 관계
                for dname in directors:
                    if dname in director_cache:
                        did = director_cache[dname]
                    else:
                        result = conn.execute(text("SELECT did FROM director WHERE dname = :dname"), {"dname": dname})
                        row_result = result.fetchone()
                        if row_result:
                            did = row_result.did
                        else:
                            result = conn.execute(text("INSERT INTO director (dname) VALUES (:dname)"), {"dname": dname})
                            did = result.lastrowid
                        director_cache[dname] = did

                    conn.execute(text("INSERT IGNORE INTO director_movie (did, mid) VALUES (:did, :mid)"), {"did": did, "mid": mid})

    print("✅ 모든 데이터 삽입 완료.")

except Exception as e:
    print(f"❌ 에러 발생: {e}")
