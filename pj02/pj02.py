import pprint
from cgi import parse_qs, escape
from mako.template import Template
import os

def application(env, start_response):
    """The main uWSGI application."""
    start_response('200 OK', [('Content-Type', 'text/html')])
    qs = parse_qs(env['QUERY_STRING'])
    """Handling the Query String Interface."""
    if len(qs) > 0:
      try:  
        #If there exist a query string
        qsNumber = qs.get("num")
        qsNumber = qsNumber[0]
        #Save number as a string
        qsFrombase = qs.get("frombase")
        qsFrombase = int(qsFrombase[0])
        #Save frombase int value
        qsTobase = qs.get("tobase")
        qsTobase = int(qsTobase[0])
        #Save tobase int value
        #Converts qsNumber to the right base and saved into converted 
        converted = int(qsNumber,qsFrombase)
        if qsTobase == 2:
          converted = '{:b}'.format(converted) 
        elif qsTobase == 8:
          converted = '{:o}'.format(converted)
        elif qsTobase == 10:
          converted = '{:d}'.format(converted)
        elif qsTobase == 16:
          converted = '{:x}'.format(converted)
        else:
          html_template = Template(filename='./templates/error.html')
          html_dict ={
            'title': 'Base Conversion Calculator'
          }
          response = html_template.render(**html_dict)
          return response.encode() 
        html_template = Template(filename='./templates/correct.html')
        html_dict ={
          'title': 'Base Conversion Calculator',
          'originalValue': pprint.pformat(qsNumber),
          'fromBase': pprint.pformat(qsFrombase),
          'toBase':  pprint.pformat(qsTobase),
          'convertednumber':  pprint.pformat(converted)
        }
      except:
        html_template = Template(filename='./templates/error.html')
        html_dict ={
          'title': 'Base Conversion Calculator'
        }        
      response = html_template.render(**html_dict)
      return response.encode()
    """Handling the POST Interface and General access."""
    if env['REQUEST_METHOD'] == 'POST':
      content_length = int(env.get('CONTENT_LENGTH', 0))
      post_data = env['wsgi.input'].read(content_length)
      post_data = str(post_data)
      qs = parse_qs(post_data)
      qsNumber = qs.get("b'num")
      qsNumber = qsNumber[0]
      qsFrombase = qs.get("frombase")
      #gets frombase value then saves into int
      qsFrombase = int(str(qsFrombase[0]))
      qsTobase = qs.get("tobase")
      qsTobase = str(qsTobase[0])
      #removes the trailing single quote from tobase and saves into int
      qsTobase = int(qsTobase[0:len(qsTobase)-1])
      try:
        converted = int(qsNumber,qsFrombase)
        if qsTobase == 2:
          converted = '{:b}'.format(converted)
        elif qsTobase == 8:
          converted = '{:o}'.format(converted)
        elif qsTobase == 10:
          converted = '{:d}'.format(converted)
        elif qsTobase == 16:
          converted = '{:x}'.format(converted) 
        html_template = Template(filename='./templates/correct.html')
        html_dict ={
          'title': 'Base Conversion Calculator',
          'originalValue': pprint.pformat(qsNumber),
          'fromBase': pprint.pformat(qsFrombase),
          'toBase':  pprint.pformat(qsTobase),
          'convertednumber':  pprint.pformat(converted)
        }
      except:
        html_template = Template(filename='./templates/error.html')
        html_dict ={
          'title': 'Base Conversion Calculator'
        }
        response = html_template.render(**html_dict)
        return response.encode()
    #Handling the GET/ general page access.
    else:
      html_template = Template(filename='./templates/calc.html')
      html_dict ={
        'title': 'Base Conversion Calculator',
      }
    pprint.pformat(env)
    response = html_template.render(**html_dict)
    return response.encode()