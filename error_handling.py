from error_handling.error_test import merry
import os
import subprocess




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


if __name__ == '__main__':
    checkpoint()
    print('continue run until finished')
