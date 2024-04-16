from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import pandas_decimal
import json


def extract(file_name:str) -> list[pd.DataFrame]:
    with open(file_name, "r") as access_data_file:
        access_data = json.loads(access_data_file.read())
    try:
        connection = psycopg2.connect(database=access_data["database"], user=access_data["user"],
                                       password=access_data["password"], host=access_data["host"],
                                       port=access_data["port"])
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';''')
        tables = [i[1] for i in cursor.fetchall()]
        #print(tables)
        data_frames = []
        for index,table in enumerate(tables):
            cursor.execute(f'''SELECT * FROM {table};''')
            df = pd.DataFrame(data=cursor.fetchall(),columns=[c[0] for c in cursor.description])
            df.to_csv(f"test_{index}.csv")
            data_frames.append(df)
    except Exception as e:
        print(e)

    return data_frames

def transform(data_frames:list[pd.DataFrame]) -> pd.DataFrame:
    for df in data_frames:
        df.reset_index()
        df.drop("id", axis=1, inplace=True)
        if "salary" in df.columns:
            df.salary = df.salary.apply(lambda x: abs(x)).astype("decimal[2]")
        if "city" in df.columns:
            df.city = df.city.str.capitalize().str[0:8:2]
            df.country = df.country.str.capitalize().str[0:5]

    return pd.concat(data_frames,axis=1)

def load(data:pd.DataFrame, file_name:str):
    with open(file_name, "r") as access_data_file:
        access_data = json.loads(access_data_file.read())

    try:
        engine = create_engine(
            "mysql://{user}:{pw}@{host}/{db}".format(host=access_data["host"], db=access_data["database"],
                                                     user=access_data["user"], pw=access_data["password"]))
        data.to_sql('table', engine, if_exists='replace', index=True)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    data_frames = extract("login_postgres.json")
    df = transform(data_frames)
    load(df,"login_mysql.json")
