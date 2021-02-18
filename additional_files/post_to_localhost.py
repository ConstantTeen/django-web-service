import requests

xml = """
<data project_id='1' task_id='1' operation='request'>    
	<row col0='1' col1='2' col2='3' col3='4' ></row>
	<row col0='5' col1='6' col2='7' col3='8' ></row>
	<row col0='1' col1='2' col2='3' col3='4' ></row>
	<row col0='4' col1='3' col2='2' col3='1' ></row>       
</data>    
"""

response_xml = """
<data project_id='1' task_id='1' operation='request' result_id='20'>    
	<row col0='1' col1='2' col2='3' col3='4' ></row>
	<row col0='5' col1='6' col2='7' col3='8' ></row>
	<row col0='1' col1='2' col2='3' col3='4' ></row>
	<row col0='4' col1='3' col2='2' col3='1' ></row>       
</data>    
"""

# option = 'request'
option = 'response'

url = 'http://127.0.0.1:8000/models/'

data = {
    # 'xml': xml,
    'xml': response_xml,
    'option': option,
}

print('data:', data['xml'])
r = requests.post(url, data=data)
r.encoding = 'utf-8'
print('post:', r.text)
