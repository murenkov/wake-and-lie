import re 
from bs4 import BeautifulSoup as BSoup


if __name__ == "__main__":
    TIMESTAMP = re.compile("(\d\d)\.(\d\d)\.(\d{4}) ((\d\d:\d\d):\d\d)")
    WAKING_UP_TIME = re.compile("(Встал) (\d?\d:\d\d)") 
    LYING_DOWN_TIME = re.compile("(Л[ё|е]г) (\d?\d:\d\d)") 
    PARSER = 'html5lib'

    input_file_name = 'messages.html'
    table = {}
    with open(input_file_name, 'r') as doc:
        messages = BSoup(doc.read(), PARSER).find_all(name='div', attrs={'class': 'default'})
        for message in messages:
            body = message.find(name='div', attrs={'class': 'body'})  
            
            timestamp = body.find(attrs={'class':'date'})
            text = body.find(attrs={'class':'text'})
            if not timestamp or not text:
                continue
            
            ts_groups = TIMESTAMP.match(timestamp.get('title')).groups()
            timestamp = '{}-{}-{}T{}'.format(ts_groups[2], ts_groups[1], ts_groups[0], ts_groups[3])
            text = text.text.strip()
            
            print('timestamp: {}\ntext: {}\n'.format(timestamp, text))

            up_time = WAKING_UP_TIME.match(text)
            down_time = LYING_DOWN_TIME.match(text)

            if up_time:
                table.setdefault(timestamp, text)
