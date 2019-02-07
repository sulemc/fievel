#abstract so it's not tied to one website... make dict of websites!!
#example dict = {'title': 'title', 'text': {'div': 'div', 'itemprop=': "description"} }

class parser_archive:
    def __init__(dict_of_html_tags, str_bucket_name,prefix_for_files_you_want):
        self.html_tags = dict_of_html_tags
        self.bucket_name = str_bucket_name
        self.client = boto3.client('s3')
        self.header = prefix_for_files_you_want

    def ingest_files(self):
        filtered_bucket = self.client.list_objects.v2(Bucket=self.bucket_name, Prefix=self.header)['Contents']
        paral_buc = sc.parallelize(filtered_bucket) #need to make spark context global? it's own module I think...
        paral_buc.map(lambda pointer: self.process_html(pointer.key))
   
   def process_html(self, pointer_key):
        get_it = sc.wholeTextFiles("s3n://"+self.bucket_name+"/" + pointer_key).collect()
        result_file = get_it[0][1]
        page_content = BeautifulSoup(result_file, "html.parser")
        results_dict = {}
        for label, tag in self.html_tags.items:
            results_dict[label] : ''
            arg1 = ''
            arg2 = None
            if type(tag) == dict:
                for key, value in tag:
                    if key == value:
                        arg1 = key
                    else:
                        arg2 = {key: value}
            else:
                arg1 = tag
            results = page_content.find(arg1, arg2)
            if results is not None:
                try:
                    json_obj = json.loads(results)
                    results_dict[label] = json_obj[label]
                except JSONDecodeError:
                    for item in results:
                    if item != '\n':
                        results_dict[label] + str(item)
        return results_dict