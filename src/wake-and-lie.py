import re 
from bs4 import BeautifulSoup as BSoup
from pprint import pprint

if __name__ == "__main__":
    TIMESTAMP = re.compile("(\d\d)\.(\d\d)\.(\d{4}) ((\d\d:\d\d):\d\d)")
    WAKING_UP_TIME = re.compile("(Встал) (\d?\d:\d\d)", re.M) 
    LYING_DOWN_TIME = re.compile("(Л[ё|е]г) (\d?\d:\d\d)", re.M) 
    WL_TIME = re.compile("(Встал|Л[ё|е]г) (\d?\d:\d\d)") 
    PARSER = 'html5lib'

    input_file_name = '../messages1.html'
    table = {}
    with open(input_file_name, 'r') as doc:
        messages = BSoup(
                doc.read().replace('<br>', '\n'),
                PARSER,
                ).find_all(name='div', attrs={'class': 'default'})

        for message in messages:
            body = message.find(name='div', attrs={'class': 'body'})  
            
            timestamp = body.find(attrs={'class':'date'})
            text = body.find(attrs={'class':'text'})
            if not timestamp or not text:
                continue
            
            ts_groups = TIMESTAMP.match(timestamp.get('title')).groups()
            timestamp = '{}-{}-{}T{}'.format(
                    ts_groups[2],
                    ts_groups[1],
                    ts_groups[0],
                    ts_groups[3],
                    )
            text = text.text.strip()
            
            print(f'{text}')
            ivent = [WAKING_UP_TIME.match(text), LYING_DOWN_TIME.match(text)]
            print(f'{ivent}')
            if ivent[0]:
                ivent.append(timestamp)
            if ivent[1]:
                ivent.append(timestamp)

            print(f'timestamp: {ivent[2]}\ntext: {ivent[:1]}\n')
    
    pprint(table)
