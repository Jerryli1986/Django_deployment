from error_handling.error_test import merry
import os
import subprocess
import logging
import sys
import re

@merry._try
def checkpoint():
    _this_dir = os.path.dirname(os.path.realpath(__file__))
    _brush_dir = os.path.join(_this_dir, '')
    _ingest_script = os.path.join(_brush_dir, 'test1.py')  # .replace('\\','/')
    fpath = os.path.join(_this_dir,
                         'AFT-000014'
                         + '.cfg')
    cmds = ['python', _ingest_script, fpath]
    cmds = subprocess.list2cmdline(cmds)
    output_dir = os.path.join(_this_dir, 'output.txt')
    proc = subprocess.Popen(cmds, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stderr_lines = proc.stderr.readlines()
    with open(output_dir, "wb") as f:
        for line in stderr_lines:
            f.write(line)
            print(str(line, 'utf-8'))

        # merry.logger.addHandler(logging.StreamHandler(sys.stderr))

if __name__ == '__main__':
    checkpoint()
    print('continue run until finished')

    # print(re.findall('(?<=_)([0-9]+)$','aft-000017_accent_test_20190114')[0])
    # print(re.findall('aft-[0-9]+','aft-000017_accent_test_20190114')[0].upper())
    # text = open('output.txt', "r").readlines()[0]
    # print(text)
    # print (re.findall('Counts Matched',text))
    # # path =  os.path.dirname(os.path.realpath(__file__))
    # path = r"C:\Users\jerryzli\Desktop\DUST_stuff"
    # arr = [f for f in os.listdir(path) if f.endswith('.txt')]
    # aft_array = list(set(re.findall('AFT-[0-9]+',str(arr))))
    # print(aft_array)

    # file_path = r'C:\Users\jerryzli\Desktop\DUST_stuff\aft-000025_edrm_20190718_QC.txt'
    # text = open(file_path, "r").readlines()
    # print(text)
    # QC = re.findall('Counts Matched', str(text))
    # print(QC)
    # if QC:
    #     QC_check = 'succeed'
    # else:
    #     QC_check = 'failed'

    # a=['a','b','c']
    # b=['e','d','f']
    # a += b
    # print(a)