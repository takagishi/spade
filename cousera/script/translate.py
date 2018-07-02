# -*- coding: utf-8 -*-

import http.client, urllib.parse, uuid, json
import argparse
import sys
import textwrap

parser = argparse.ArgumentParser(description='translate program')
parser.add_argument('-i','--in', action='store', dest='in_file', required=True, help='tanslate input file')
args = parser.parse_args()

if str(args.in_file).endswith('vtt') == False:
    print('invalid in_file. not vtt file. file=' +str(args.in_file))
    sys.exit()

# **********************************************
# *** Update or verify the following values. ***
# **********************************************
# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = ''
host = 'api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
# Translate to Japanese
params = "&to=ja";



text = 'Hello, world!'

def translate (content):

    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", path + params, content, headers)
    response = conn.getresponse ()
    return response

requestBody = [{
    'Text' : text,
}]

out_file = str(args.in_file).replace('vtt','srt')
out_f = open(out_file, 'w')
comment_no = 1
print("start srt file")
with open(args.in_file,'r') as f:
    for row in f:
        line = row.strip()
        if line == str(comment_no):
            out_f.write(str(comment_no) + "\n")
            out_f.write(next(f))

            eng_text = next(f).strip()
            work = next(f).strip()
            while work != '':
                eng_text += " " + str(work.strip())
                if(work.endswith('\n') == False):
                    break
                work = next(f)

            #print(str(comment_no) + ":" + eng_text +"\n")
            requestBody = [{
                'Text' : eng_text,
            }]
            content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
            result = translate (content)
            result_dict = json.load(result)[0]
            #print(result_dict)
            #print('result_dict:{}'.format(type(result_dict)))

            jpn_text = result_dict['translations'][0]['text']
            jpn_text = "\n".join(textwrap.wrap(jpn_text, width=20))
            out_f.write(jpn_text +"\n")

            comment_no = comment_no + 1
            out_f.write('\n')

out_f.close()
print("end srt file")

print("start style file")
with open(out_file+".style",'w') as f:
    f.write("ScriptType: v4.00+\n")
    f.write("\n")
    f.write("[V4+ Styles]\n")
    f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
    f.write("Style: Default,Arial,20,&H00ffffff,&H0000ffff,&H00000000,&H80000000,-1,0,0,0,100,100,0,0.00,1,2,2,1,95,20,20,1\n")
print("end style file")
