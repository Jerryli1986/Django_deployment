import os
import pandas as pd
from datetime import datetime

# directory_path = r"C:\Users\jerryzli\Downloads\DUST_test_data\656-657"
# directory_path = r"C:\Users\jerryzli\Downloads\DUST_test_data\test"
#

def _iterative_scan(dirs) :
    while len(dirs) >0 :
        current_dir =dirs.pop(0)
        for dir_entry in os.scandir(current_dir) :
            if dir_entry.is_file() :
                filename = dir_entry.name
                filepath = dir_entry.path
                file_extension = os.path.splitext(filename)[1][1:].strip()
                yield filename,file_extension,filepath

            elif  dir_entry.is_dir():
                dirs.append(dir_entry.path)

def fileSummary(tuples):
    res =[]
    for t in tuples :
        # file size
        file_size = round(os.path.getsize(t[2]) / 1024 )   # KB
        t += (file_size,)
        res.append(list(t))
    return res

def _writetocsv(list) :
       # write to csv
       df = pd.DataFrame(list,columns=['filename','type','path','size(KB)'])
       df.to_csv('filesummary.csv', header=['filename','type','path','size(KB)'],index=True)

if __name__ == "__main__":
    #init_path = r"C:\Users\jerryzli\Downloads\DUST_test_data\656"
    init_path = r"P:\DUST\Fileshare Dataset\GovDocs1\RAW\Harriet"
    dirs = [init_path]
    scan_res= _iterative_scan(dirs)
    sum_res = fileSummary(scan_res)
    _writetocsv(sum_res)




