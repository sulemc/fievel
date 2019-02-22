
from bs4 import BeautifulSoup
import boto3
import json

class ParserArchive:
    def __init__(self, dict_of_html_tags, str_bucket_name,prefix_for_files_you_want, spark_context, states):
        self.html_tags = dict_of_html_tags
        self.bucket_name = str_bucket_name
        self.client = boto3.client('s3')
        self.header = prefix_for_files_you_want
        self.sc = spark_context
        self.states = states
    
    def ingest_files(self):
        #this is how you get the keys from s3 to parallelize
        filtered_bucket = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.header)['Contents']
        print("FILTERED BUCKET IS HERE!", len(filtered_bucket))
         #can't send entire class to worker nodes because of spark context so must create variables to pass
        paral_buc = self.sc.parallelize(filtered_bucket) 
        b_n = self.bucket_name
        h_tags = self.html_tags
        states = self.states
        parsed = paral_buc.map(lambda pointer: process_html(pointer['Key'],b_n, h_tags,states))
        return parsed #returns RDD of processed HTML dictionaries
      
   
def process_html(pointer_key, bucket, tags, states):
    s3_client = boto3.client('s3')
    #get html from s3
    s3_response_object = s3_client.get_object(Bucket=bucket, Key=pointer_key)
    object_content = s3_response_object['Body'].read()
    #soupify
    page_content = BeautifulSoup(object_content, "html.parser")
    results_dict = {}
    results_dict["s3_id"] = str(pointer_key)
    for label, tag in tags.items():
        arg1 = ''
        arg2 = None
        #need to refactor to handle html data from json better
        if label == "location":
            arg1 = "script"
            arg2 = {"type": "application/ld+json"}
            results = page_content.find(arg1, arg2)
            if results is not None:
                try:
                    json_obj = ''
                    for item in results:
                        json_obj = json.loads(item)
                        results_dict['ad_location_city'] = json_obj["address"]["addressLocality"]
                        state = json_obj["address"]["addressRegion"]
                        valid_state = states[state]
                        results_dict['ad_location_state'] = valid_state
                except KeyError:
                    continue
                except TypeError:
                    continue
                except ValueError:
                    continue 
        #this else statement takes each key value pair in the HTML tags dictionary and feeds it to BeautifulSoup's .find()
        # this allows for the code to be resuable for different websites.      
        else:    
            if type(tag) == dict:
                for key, value in tag.items():
                        arg1 = key
                        arg2 = value
            else:
                arg1 = tag
            results = page_content.find(arg1, arg2)
            if results is not None:
                try:
                    json_obj = ''
                    for item in results:
                        json_obj = json.loads(item)
                    results_dict[label] = json_obj[label]
                except ValueError:
                    results_dict[label] = ''
                    for item in results:
                        if item != '\n':
                            results_dict[label] = results_dict[label] + str(item)
                except TypeError:
                    results_dict[label] = ''
                    for item in results:
                        if item != '\n':
                            results_dict[label] = results_dict[label] + str(item)
    
    return results_dict #will be one row in the DataFrame
