import pprint
from cgi import parse_qs, escape
from mako.template import Template
import os

def application(env, start_response):
    """The main uWSGI application."""
    start_response('200 OK', [('Content-Type', 'text/html')])
    content_length = int(os.getenv('CONTENT_LENGTH', 0))
    post_data = env['wsgi.input'].read(content_length)
    inputList = str(post_data).split("&")
    """number = inputList[0]
    number = number[number.index("=")+1:]
    fromBase = inputList[1]
    fromBase = fromBase[fromBase.index("=")+1:]
    toBase = inputList[2]
    toBase = toBase[toBase.index("=")+1:]"""
    html_template = Template(filename='templates/calc.html')
    pprint.pformat(env)
    html_dict ={
      'title': 'Base Conversion Calculator',
      'postdata': pprint.pformat(post_data)
      
    }
    
    response = html_template.render(**html_dict)
    return response.encode()