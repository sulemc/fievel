import os
import json

from az2s3 import AZ2S3
from parser_archive import ParserArchive
from send_to_db import Poster
from state_dict import US_States
from use_model import Model_It
from filter_for_web import filter_class
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row
from mp_builder import mp_scrape
from mp_retry import mp_scrape2



def main_az2s3(azname, azkey, azcontainer, s3buc):
     AZ2S3(azkey, azname, azcontainer, s3buc).az_to_s3()

def main_s32db(strings_of_html_tags, str_bucket_name, prefix_for_files_you_want, table_name, ec2_db_server, db, db_user, db_pass ):
    #convert strings to dict
    dict_of_html_tags = processDict(strings_of_html_tags)
    #intitalize the spark context
    sparkie = SparkContext(appName="s32db")
    sparkie.setLogLevel("FATAL")
    #initialize needed helper classes
    us_dict = US_States()
    insta_model = Model_It()

    #heavy lifiting of parsing the html, returns a RDD of the pieces of the html page you want
    parsed = ParserArchive(dict_of_html_tags, str_bucket_name, prefix_for_files_you_want, sparkie, us_dict.us_state_abbrev).ingest_files()
    #send the RDD to the model function, returns RDD
    modeled = parsed.map(lambda ret_dict: insta_model.predict(ret_dict))

    #convert from RDD to DataFrame and post to DB
    Poster_instance = Poster(ec2_db_server,db,db_user,db_pass)
    spar = SparkSession(sparkie)
    df = spar.createDataFrame(modeled)
    Poster_instance.post(table_name, df)

def main_MP2db(table_name,ec2_db_server,db,db_user,db_pass ):
    #intitalize the spark context
    sparkie = SparkContext(appName="mp2db")
    sparkie.setLogLevel("FATAL")
    #initialize scrape
    insta_mp = mp_scrape2()
    insta_mp.loop()
    paral = sparkie.parallelize(insta_mp.all)
    #convert to dataframe and post to db
    spar = SparkSession(sparkie)
    mpdf = spar.createDataFrame(paral)
    Poster_instance = Poster(ec2_db_server,db,db_user,db_pass)
    Poster_instance.post(table_name, mpdf)
    
    
    # insta_filter = filter_class()
    # df1 = df.dropna(subset=['ad_location_state'])
    # df2 = df1.filter(df.predicted_race == ' ')
    # sqlLite_Poster = CREATEME.post('Flagged_Ad', df2.withColumnRenamed('ad_location_state').select('url', 'location'))
    # df3 = df2.join(mpdf, df1.ad_location_state == mpdf.State).where()

def processDict(string):
    dicT = json.loads(string)
    return dicT

def loop_it(arr):
    try:
        for i in arr:
            print('i',i)
            return i
    except TypeError:
        print('typeerror')

if __name__ == "__main__":
    if os.environ["EX_FLAG"] == "az2s3":
         main_az2s3(os.environ["AZ_Account_Name"], os.environ["AZ_Key"],os.environ["AZ_Container"], os.environ["S3_Bucket_Name"])
    elif os.environ["EX_FLAG"] == "s32db":
        main_s32db(os.environ["DB_HTML_Schema"],os.environ["S3_Bucket_Name"], os.environ["S3_Data_Prefix"],os.environ["DB_TABLE"],os.environ["EC2_DB_Server"], os.environ["DB"], os.environ["DB_User"], os.environ["DB_Pass"])
    elif os.environ["EX_FLAG"] == "mp2db":
        main_MP2db(os.environ["DB_TABLE"],os.environ["EC2_DB_Server"], os.environ["DB"], os.environ["DB_User"], os.environ["DB_Pass"])
