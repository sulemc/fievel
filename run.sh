#!/bin/bash

#variables
AZ_Account_Name=
AZ_Key=
AZ_Container=
DB_HTML_Schema=
DB=
DB_User=
DB_Pass=
DB_TABLE
S3_Bucket_Name=
S3_Data_Prefix=
EC2_DB_Server=
IP_ADDR="$(hostname)"
DEPS=
EX_FLAG=


# Move data from azure to s3 start script
if [ "$1" = "-az2s3" ]
then
    FLAG="az2s3"
    DEPS="./src/az2s3.py"
    echo "starting azure to s3 job"
    response=$response
    echo -n "Enter Azure Account Name >>"
    read response
    if [ -n "$response" ]; then
    AZ_Account_Name=$response
    echo "Using Azure $AZ_Account_Name"
    echo -n "Enter Azure Account Key >>"
    read response
    if [ -n "$response" ]; then
    AZ_Key=$response
    echo "Key Registered"
    echo -n "Enter Container Name >>"
    read response
    if [ -n "$response" ]; then
    AZ_Container=$response
    echo "Accessing $AZ_Container"
    echo -n "Enter S3 Bucket name >>"
    read response
    if [ -n "$response" ]; then
    S3_Bucket_Name=$response
    echo "Depositing into $S3_Bucket_Name"
    echo "Beginning AZ to S3"
    export AZ_Account_Name
    export AZ_Key
    export AZ_Container
    export EX_FLAG
    export S3_Bucket_Name
    spark-submit --master spark://$IP_ADDR:7077 --num-executors 3 --py-files $DEPS ./src/main.py
    
fi
fi
fi
fi
fi
#s3, parse HTML, store in db
if [ "$1" = "-s32db" ]
then
    FLAG="s32db"
    DEPS="./src/parser_archive.py,./src/send_to_db.py,./src/use_model.py"
    response=
    echo -n "Enter S3 Bucket Name >>"
    read response
    if [ -n "$response" ]; then
    S3_Bucket_Name=$response
    echo "Pulling data from $S3_Bucket_Name"
    echo -n "Enter data prefix (if applicable) >>"
    read response
    if [ -n "$response" ]; then
    S3_Data_Prefix= $response
    echo "Will only pull data starting with $S3_Data_Prefix"
    echo -n "Enter HTML Schema in JSON format>>"
    read response
    if [ -n "$response" ]; then
    DB_HTML_Schema= $response
    echo "Using $DB_HTML_Schema"
    echo -n "Enter DB table name>>"
    read response
    echo -n "Enter EC2 DB Server>>"
    read response
    if [ -n "$response" ]; then
    EC2_DB_Server $response
    echo "Using $EC2_DB_Server"
    echo -n "Enter DB name>>"
    read response
    if [ -n "$response" ]; then
    DB= $response
    echo "Using $DB"
    echo -n "Enter DB username>>"
    read response
    if [ -n "$response" ]; then
    DB_User= $response
    echo "Using $DB_User"
    echo -n "Enter DB password>>"
    read response
    if [ -n "$response" ]; then
    DB_Pass= $response
    echo "Using $DB_pass"
    echo -n "Enter DB table name>>"
    read response
    if [ -n "$response" ]; then
    DB_TABLE= $response
    echo "Using $DB_TABLE"
    export DB
    export DB_Pass
    export DB_User
    export EC2_DB_Server
    export EX_FLAG
    export S3_Bucket_Name
    export S3_Data_Prefix
    export DB_HTML_Schema
    export DB_TABLE
    echo "Starting S3 to DB"
    spark-submit --master spark://$IP_ADDR:7077 --jars mysql-connector-java-8.0.15.jar --num-executors 3 --py-files $DEPS ./src/main.py
fi
fi
fi
fi
fi

if [ "$1" = "-mp2db" ]
then
    FLAG="mp2db"
    DEPS="./src/send_to_db.py,"
    response=
    echo -n "Enter EC2 DB Server>>"
    read response
    if [ -n "$response" ]; then
    EC2_DB_Server $response
    echo "Using $EC2_DB_Server"
    echo -n "Enter DB name>>"
    read response
    if [ -n "$response" ]; then
    DB= $response
    echo "Using $DB"
    echo -n "Enter DB username>>"
    read response
    if [ -n "$response" ]; then
    DB_User= $response
    echo "Using $DB_User"
    echo -n "Enter DB password>>"
    read response
    if [ -n "$response" ]; then
    DB_Pass= $response
    echo "Using $DB_pass"
    echo -n "Enter DB table name>>"
    read response
    if [ -n "$response" ]; then
    DB_TABLE= $response
    echo "Using $DB_TABLE"

    export DB
    export DB_Pass
    export DB_User
    export EC2_DB_Server
    export EX_FLAG
    export S3_Bucket_Name
    export S3_Data_Prefix
    export DB_HTML_Schema
    export DB_TABLE
    echo "Starting MP to DB"
    spark-submit --master spark://$IP_ADDR:7077 --jars mysql-connector-java-8.0.15.jar --num-executors 3 --py-files $DEPS ./src/main.py
