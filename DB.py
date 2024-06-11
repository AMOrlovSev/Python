import psycopg2
import ETL

def connection_postgres():
    connection = psycopg2.connect(dbname="postgres",
                                    host="localhost",
                                    user="postgres",
                                    password="12345",
                                    port="5432")
    return connection

def connection_DB(DB_name):
    temp_dbname = f"{DB_name}"
    temp_user = f"role_{DB_name}"
    connection = psycopg2.connect(dbname=temp_dbname,
                                    host="localhost",
                                    user=temp_user,
                                    password="Pa$$W0rd",
                                    port="5432")
    return connection

def create_DB_and_Role(DB_name):
    try:
        connection = connection_postgres()
        with connection.cursor() as cursor:
            connection.autocommit = True

            # sql1 = f"""DROP DATABASE IF EXISTS {DB_name}"""
            # cursor.execute(sql1)

            sql2 = f"""CREATE DATABASE {DB_name}"""
            cursor.execute(sql2)

            sql3 = f"""--DROP ROLE IF EXISTS ROLE_{DB_name};
                        CREATE USER ROLE_{DB_name} WITH PASSWORD 'Pa$$W0rd';
                        ALTER ROLE ROLE_{DB_name} SET client_encoding TO 'utf8';
                        ALTER ROLE ROLE_{DB_name} SET default_transaction_isolation TO 'read committed';
                        ALTER ROLE ROLE_{DB_name} SET timezone TO 'UTC';
                        GRANT ALL PRIVILEGES ON DATABASE {DB_name} TO ROLE_{DB_name};
                        GRANT ALL ON ALL TABLES IN SCHEMA public TO ROLE_{DB_name};
                        ALTER DATABASE {DB_name} OWNER TO ROLE_{DB_name};"""
            cursor.execute(sql3)
    except:
        print("create Подключение не удалось")
    finally:
        connection.close()

def create_tables_DB(DB_name):
    connection=connection_DB(DB_name)
    with connection.cursor() as cursor:
        connection.autocommit = True
        sql = """
        DROP TABLE IF EXISTS categories CASCADE;

        CREATE TABLE categories (
            category_id serial4 NOT NULL,
            category varchar NULL,
            CONSTRAINT categories_pk PRIMARY KEY (category_id)
        );
        
        DROP TABLE IF EXISTS states CASCADE;
        
        CREATE TABLE states (
            state_id serial4 NOT NULL,
            state_full varchar NULL,
            state_abbr bpchar(2) NOT NULL,
            CONSTRAINT states_pk PRIMARY KEY (state_id)
        );
 
        DROP TABLE IF EXISTS users CASCADE;
        
        CREATE TABLE users (
            user_id serial4 NOT NULL,
            fname varchar NULL,
            lname varchar NULL,
            username varchar NOT NULL UNIQUE,
            password_hash varchar NOT NULL,
            CONSTRAINT users_pk PRIMARY KEY (user_id)
        );

        DROP TABLE IF EXISTS cities CASCADE;
        
        CREATE TABLE cities (
            city_id serial4 NOT NULL,
            city varchar NOT NULL,
            state_id int4 NOT NULL,
            CONSTRAINT cities_pk PRIMARY KEY (city_id),
            CONSTRAINT cities_states_fk FOREIGN KEY (state_id) REFERENCES states(state_id)
        );
        
        DROP TABLE IF EXISTS markets CASCADE;
        
        CREATE TABLE markets (
            market_id int4 NOT NULL,
            market_name varchar NULL,
            street varchar NULL,
            city int4 NULL,
            state int4 NULL,
            zip int4 NULL,
            lat float4 NULL,
            lon float4 NULL,
            CONSTRAINT markets_pk PRIMARY KEY (market_id),
            CONSTRAINT markets_cities_fk FOREIGN KEY (city) REFERENCES cities(city_id),
            CONSTRAINT markets_states_fk FOREIGN KEY (state) REFERENCES states(state_id)
        );

        DROP TABLE IF EXISTS markets_categories CASCADE;
        
        CREATE TABLE markets_categories (
            market_category_id int4 NOT NULL,
            market_id int4 NOT NULL,
            category_id int4 NOT NULL,
            CONSTRAINT markets_categories_pk PRIMARY KEY (market_category_id),
            CONSTRAINT markets_categories_categories_fk FOREIGN KEY (category_id) REFERENCES categories(category_id),
            CONSTRAINT markets_categories_markets_fk FOREIGN KEY (market_id) REFERENCES markets(market_id)
        );

        DROP TABLE IF EXISTS reviews CASCADE;
        
        CREATE TABLE reviews (
            review_id serial4 NOT NULL,
            user_id int4 NOT NULL,
            market_id int4 NOT NULL,
            date_time date NOT NULL,
            score int2 NOT NULL,
            review text NULL,
            CONSTRAINT reviews_pk PRIMARY KEY (review_id),
            CONSTRAINT reviews_markets_fk FOREIGN KEY (market_id) REFERENCES markets(market_id),
            CONSTRAINT reviews_users_fk FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
        cursor.execute(sql)
    connection.close()


def filling_tables_DB(DB_name):
    connection = connection_DB(DB_name)
    with connection.cursor() as cursor:
        connection.autocommit = True

        sql01 = """INSERT INTO users VALUES(1, 'Orlov', 'Artem', 'AMOrlov', 'Pa$$W0rd');"""
        cursor.execute(sql01)

        csv_file_name = "states.csv"
        sql2 = "COPY states FROM STDIN DELIMITER ',' CSV HEADER;"
        cursor.copy_expert(sql2, open(csv_file_name, "r"))

        csv_file_name = "cities.csv"
        sql2 = "COPY cities FROM STDIN DELIMITER ',' CSV HEADER;"
        cursor.copy_expert(sql2, open(csv_file_name, "r"))

        csv_file_name = "markets.csv"
        sql2 = "COPY markets FROM STDIN DELIMITER ',' CSV HEADER;"
        cursor.copy_expert(sql2, open(csv_file_name, "r"))

        csv_file_name = "categories.csv"
        sql2 = "COPY categories FROM STDIN DELIMITER ',' CSV HEADER;"
        cursor.copy_expert(sql2, open(csv_file_name, "r"))

        csv_file_name = "markets_categories.csv"
        sql2 = "COPY markets_categories FROM STDIN DELIMITER ',' CSV HEADER;"
        cursor.copy_expert(sql2, open(csv_file_name, "r"))

        sql02 = """INSERT INTO reviews VALUES(1, 1,1000021, '2024-06-08', 5, 'отзыв');
                INSERT INTO reviews VALUES(2, 1,1000021, '2024-06-08', 4, 'отзыв2');"""
        cursor.execute(sql02)

    connection.close()

# ETL.create_csv()
# connection_postgres()
# create_DB_and_Role("farmers_markets1")
# connection_DB("farmers_markets1")
# create_tables_DB("farmers_markets1")
# filling_tables_DB("farmers_markets1")