import os
import pandas as pd

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

def filetypes(tuples):
    typelist=[]
    for t in tuples :
        typelist.append(t[1])
    return list(set(typelist))

def _writetocsv(list) :
       # write to csv
       df = pd.DataFrame(list)
       df.to_csv('filetypes.csv', header=False,index=False)

if __name__ == "__main__":
    # init_path = r"C:\Users\jerryzli\Downloads\DUST_test_data"
    init_path = r"P:\DUST\Fileshare Dataset\GovDocs1\RAW\Harriet"
    dirs = [init_path]
    result= _iterative_scan(dirs)
    typelist = filetypes(result)
    _writetocsv(typelist)
    print(typelist)



