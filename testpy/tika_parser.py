

# run command line : java -jar C:\jars\tika-app-1.22.jar
from tika import parser,config
from tika.tika import parse1,callServer, ServerEndpoint
import time
import json


def _parse(jsonOutput,option):
    '''
    Parses JSON response from Tika REST API server
    :param jsonOutput: JSON output from Tika Server
    :return: a dictionary having 'metadata' and 'content' values
    '''
    parsed = {}
    if not jsonOutput:
        return parsed

    parsed["status"] = jsonOutput[0]
    if jsonOutput[1] == None or jsonOutput[1] == "":
        return parsed
    realJson = json.loads(jsonOutput[1])
    content = ""
    for js in realJson:
        if "X-TIKA:content" in js:
            content += js["X-TIKA:content"]
    if content == "":
        content = None
    parsed["content"] = content
    parsed["metadata"] = {}
    if option == 'all' :
        for js in realJson:
            for n in js:
                if n != "X-TIKA:content":
                    if n in parsed["metadata"]:
                        if not isinstance(parsed["metadata"][n], list):
                            parsed["metadata"][n] = [parsed["metadata"][n]]
                        parsed["metadata"][n].append(js[n])
                    else:
                        parsed["metadata"][n] = js[n]
    elif option == 'meta' :
        for n in realJson:
            if n != "X-TIKA:content":
                if n in parsed["metadata"]:
                    if not isinstance(parsed["metadata"][n], list):
                        parsed["metadata"][n] = [parsed["metadata"][n]]
                    parsed["metadata"][n].append(realJson[n])
                else:
                    parsed["metadata"][n] = realJson[n]
    return parsed




def _parser1_from_file(filename, option, serverEndpoint=ServerEndpoint, xmlContent=False, headers=None, config_path=None):

    if not xmlContent:
        jsonOutput = parse1(option, filename, serverEndpoint, headers=headers, config_path=config_path)
    else:
        jsonOutput = parse1(option, filename, serverEndpoint, services={'meta': '/meta', 'text': '/tika', 'all': '/rmeta/xml'},
                            headers=headers, config_path=config_path)

    return _parse(jsonOutput,option)


def _parser_from_file(fpath):
    # Parse document with tika
    d = parser.from_file(fpath, xmlContent=True)
    return d




if __name__ == "__main__":
   # fpath = r"C:\Users\jerryzli\Downloads\OreillyGraphDatabases.pdf"
   fpath = r"C:\Users\jerryzli\Downloads\DUST_test_data\Tower_Bridge_London_Feb_2006.jpg"
   # fpath = r"C:\Users\jerryzli\Downloads\innovationlabgraphtour-190207131245.pdf"
   # fpath = r"C:\Users\jerryzli\Downloads\DUST_test_data\SampleXLSFile_6800kb.xls"
   # fpath = r"C:\Users\jerryzli\Downloads\DUST_test_data\SamplePPTFile_1000kb.ppt"
   # fpath = r"C:\Users\jerryzli\Downloads\DUST_test_data\SampleDOCFile_5000kb.doc"
   # fpath = r"C:\Users\jerryzli\Downloads\DUST_test_data\657095.doc"

   avg =0
   for i in range(10) :
       start_time = time.time()
       # res = _parser_from_file(fpath)
       res= _parser1_from_file(fpath,'all',xmlContent=True)
       duration = time.time() - start_time
       avg += duration
       print(f'duration:{duration} seconds')
   print ('avg:{} seconds'.format(avg/20))

   avg1 = 0
   for i in range(10):
       start_time = time.time()
       # res = _parser_from_file(fpath)
       res = _parser1_from_file(fpath, 'meta',xmlContent=True)
       duration = time.time() - start_time
       avg1 += duration
       print(f'duration:{duration} seconds')
   print('avg:{} seconds'.format(avg1 / 20))
   # print(res)
   # for k,v in res['metadata'].items():
   #     print({k:v})
   # for k,v in json.loads(config.getDetectors()).items():
   #     print({k:v})

