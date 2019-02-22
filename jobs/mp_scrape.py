#import post_to_db
class mp_scrape:
    def __init__(self):
        self.states = [ 'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY' ]
        self.count = 0
        self.address = 'https://api.missingkids.org/missingkids/servlet/PubCaseSearchServlet?act=usMapSearch&missState='

    def get_MP_state_page(self):
        only_table_tags = SoupStrainer("table")
        page_response = requests.get(self.address+self.states[count], timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser",parse_only=only_table_tags)
        tables = page_content.find_all('table', width="100%")
        stringify_tables = str(tables[0])
        p = re.compile(r"<b>(.+?)</b>")
        s = p.split(stringify_tables)
        images = []
        urls = []
        for img in page_content.find_all('img'):
            im = img.get('src')
            if "photographs" in im:
                images.append(im)
        for a in page_content.find_all('a', href=True):
            url = a['href']
            if "/missingkids/servlet/PubCaseSearchServlet?" in url:
                urls.append(url)
        return s, images

    def package(self, strings, list_of_images):
        people = 0
        i = 1
        j = 0
        while people < len(list_of_images):
            name = s[i]
            number = s[i+2]
            DOB = re.findall(r"\n(.+?)\n",s[i+5])[0].lstrip().rstrip()
            missing_date = re.findall(r"\n(.+?)\n",s[i+9])[0].lstrip().rstrip()
            race = re.findall(r"\n(.+?)\n",s[i+11])[0].lstrip().rstrip()
            location = re.findall(r"\n(.+?)\n",s[i+13])[0].lstrip().rstrip()
            state = self.states[self.count]
            image = 'https://api.missingkids.org' + images[j]
            url = 'https://api.missingkids.org' + urls[j]
            packaged_info = {
                'Name': name,
                'Number': number,
                'DOB': DOB,
                'Missing_Date': missing_date,
                'Race': race,
                'City': location,
                'State': state,
                'Image_URL': image,
                'Post_URL' : url
            }
            poster.post_to_db(packaged_info, 'MEC')
            j = j + 1
            i = i + 14
            people = people + 1
        i = 1
        j = 0