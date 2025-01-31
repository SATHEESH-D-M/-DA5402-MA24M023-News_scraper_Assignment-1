"""
Summary:
    # This module contains only the helper functions to insert the scrapped data into the PostgreSQL database.
    # The functions are used in the main module to insert the scrapped data into the database.

    # The functions are:
        - insert_data_into_DB (Part answer to Modules 4 & 5)
"""

import psycopg2
from psycopg2 import IntegrityError
import pandas as pd
import configparser


def insert_data_into_DB(config: configparser.ConfigParser, df: pd.DataFrame) -> None:
    """
    Summary:
        # Inserts the scrapped data into the PostgreSQL database.
        # This function creates two tables in the database if not already present.
            - gnews_images
            - gnews_metadata
        # First it inserts the metadata (with unique constraint in headlines) into gnews_metadata table.
        # Then it inserts the image info into gnews_images table.

    Args:
        config (configparser.ConfigParser): The configuration file.
            - config.ini should contain the following:
                 config["POSTGRES"]["dbname"] (str): Database name
                - config["POSTGRES"]["user"] (str): Username for PostgreSQL
                - config["POSTGRES"]["password"] (str): Password for the user
                - config["POSTGRES"]["host"] (str): Host (use 'localhost' or IP address)
                - config["POSTGRES"]["port"] (str): Port (default is 5432)

        df (pd.DataFrame): The dataframe containing the scrapped data.
            - df.columns = ['image_data',
                            'headlines',
                            'image_url',
                            'image_height',
                            'image_width',
                            'article_url',
                            'scrap_timestamp',
                            'published_time']

    Returns: None
    """
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=config["POSTGRES"]["dbname"],  # Database name
            user=config["POSTGRES"]["user"],  # Username for PostgreSQL
            password=config["POSTGRES"]["password"],  # Password for the user
            host=config["POSTGRES"]["host"],  # Host (use 'localhost' or IP address)
            port=config["POSTGRES"]["port"],  # Port (default is 5432)
        )
        # Create a cursor object
        cursor = connection.cursor()
        print("\n\nConnected to the Postgres database successfully. \n")

        # Create a table gnews_images in the DB if one doesn't exist
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS gnews_images (
                        image_id SERIAL PRIMARY KEY,
                        image_data BYTEA NOT NULL,
                        image_url TEXT NOT NULL,
                        image_height INT CHECK (image_height >= 0),
                        image_width INT CHECK (image_width >= 0)
                        )""")

        # Create a table gnews_metadata in the DB if one doesn't exist
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS gnews_metadata (
                        news_id SERIAL PRIMARY KEY,
                        headlines TEXT NOT NULL UNIQUE,
                        article_url TEXT NOT NULL,
                        scrap_timestamp TIMESTAMP NOT NULL,
                        published_time TEXT NOT NULL
                        )""")

        print("\nInserting data into DB. \n")
        # Iterate through each row in the pandas dataframe df
        for _, row in df.iterrows():
            try:
                # check for headline duplicates and insert into gnews_metadata table
                cursor.execute(
                    """
                    INSERT INTO gnews_metadata (headlines, article_url, scrap_timestamp, published_time)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        row["headlines"],
                        row["article_url"],
                        row["scrap_timestamp"],
                        row["published_time"],
                    ),
                )

            except IntegrityError as e:
                # Handle UNIQUE constraint violation
                print(f"Skipping duplicate data: {row['headlines']}")
                connection.rollback()  # Roll back only this failed insert

            else:
                # Once sucessful, then
                # insert corresponding image info into gnews_images table
                try:
                    # Insert row into the table
                    cursor.execute(
                        """
                        INSERT INTO gnews_images (image_data, image_url, image_height, image_width)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            row["image_data"],
                            row["image_url"],
                            row["image_height"],
                            row["image_width"],
                        ),
                    )
                except IntegrityError as e:
                    # Handle error
                    print(f"INSERT ERROR: {e}")
                    # Roll back entire transaction as the second insert failed
                    connection.rollback()
                else:
                    # Committing as both inserts were successful
                    connection.commit()

    # Error handling
    except psycopg2.Error as e:
        # print("Connection failed:", e.pgerror or e.diag.message_primary)
        print("Connection failed:", str(e))

    # Close the connection at the end
    finally:
        if "connection" in locals() and connection:
            cursor.close()
            connection.close()
            print("\n\nInserted data. Database connection closed.\n")

    return None
