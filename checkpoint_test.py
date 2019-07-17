import re
import json
import merry
# key_words=re.match('(?<=<mark>)([a-zA-Z0-9]+)',
#                    str({'content': ['And for <mark>China</mark>, it will be “ICOIT-Asia, <mark>China</mark> Chapter”.']}))
# sentence=str({'content': ['Greenspan was born on March 6, 1926, in <mark>New</mark> <mark>York</mark> <mark>City</mark>.', ',Inc., economic consulting firm in <mark>New</mark> <mark>York</mark> <mark>City</mark>.']})
#
# key_words=re.findall("(?<=<mark>)([a-zA-Z0-9]+)",
#                    sentence
#                    ,re.MULTILINE) #.sort(key=len, reverse=False)
# print (key_words)
# print(json.dumps({'Key Words': key_words.groups()}))

##################################################
# sentence=str({'content': ['Greenspan was born on March 6, 1926, in <mark>New</mark> <mark>York</mark> <mark>City</mark>.', ',Inc., economic consulting firm in <mark>New</mark> <mark>York</mark> <mark>City</mark>.']})
#
# key_words=list(set(re.findall("(?<=<mark>)(.*?)(?=<\/mark>)",
#                    sentence.replace('</mark> <mark>',' ')
#                    ,re.MULTILINE)))
# print (key_words)
#
# # ######################
# sentence=str({'content': ['57:00Z" />\n<meta name="dc:title" content="To:  " />\n<meta name="Application-Name" content="Microsoft <mark>Word</mark>', 'meta name="dc:subject" content="" />\n<meta name="extended-properties:Application" content="Microsoft <mark>Word</mark>', 'content="5831" />\n<meta name="X-TIKA:origResourceName" content="C:\\WINDOWS\\Application Data\\Microsoft\\<mark>Word</mark>', '</p>\n<p class="normal_(Web)">Greg Blair is back in <mark>New</mark> <mark>York</mark> with his wife Rene and his wonderful kids', 'Annat Jain is <mark>now</mark> in <mark>New</mark> Delhi. What began on that balcony is <mark>now</mark> RazorFinish.com.']}
# )
#
# key_words=list(set(re.findall("(?<=<mark>)(.*?)(?=<\/mark>)",
#                    sentence.replace('</mark> <mark>',' ')
#                    ,re.MULTILINE)))
#
# print (key_words)
#
# keys=sorted(key_words, key=len, reverse=True)
# print(keys)


#######################
import os
import datetime
import subprocess

import sys
import configparser


_this_dir = os.path.dirname(os.path.realpath(__file__))
# _static_dir = os.path.join(_this_dir, 'static')
# _config_dir = os.path.join(_static_dir, 'configs')
# print(_this_dir )
_brush_dir = os.path.join(_this_dir, '')
# print(_brush_dir)
_ingest_script = os.path.join(_brush_dir, 'test1.py')  #.replace('\\','/')

now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
fpath = os.path.join(_this_dir,
                     # now
                     #  '_'
                      'AFT-000014'
                     + '.cfg')   #.replace('\\','/')
# cmds = ['sudo','python', _ingest_script, fpath]
cmds = ['python', _ingest_script, fpath]
# print(cmds)
cmds=subprocess.list2cmdline(cmds)
# print(cmds)
output_dir=os.path.join(_this_dir,'output.txt')
# with open(output_dir, "wb") as f:
#     p= subprocess.Popen(cmds, shell=True, stderr=subprocess.PIPE,stdout=f)

proc= subprocess.Popen(cmds, shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)

# stderr_lines = proc.stderr.readlines()
# for line in stderr_lines:
#     print(line.rstrip())

# stderr_lines = iter(proc.stderr.readline, b"")
stderr_lines = proc.stderr.readlines()
with open(output_dir, "wb") as f:
   for line in stderr_lines:
       f.write(line)
       print (str(line,'utf-8'))

# with open(output_dir, "wb") as f1:
#     f1.write(b'test')



    # for o in p.stdout :
    #     print(o)

# while True:
#     out = p.stderr.read(1)
#     if out == '' and p.poll() != None:
#         break
#     if out != '':
#         sys.stdout.flush()



