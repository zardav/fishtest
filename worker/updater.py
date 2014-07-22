from __future__ import absolute_import
from __builtin__ import file

import os
import requests
import shutil
import sys
import subprocess
from zipfile import ZipFile
from distutils.dir_util import copy_tree

Py2Exe = False

WORKER_URL = 'https://github.com/glinscott/fishtest/archive/master.zip' if not Py2Exe \
else 'https://github.com/glinscott/fishtest/releases/download/v1.0/fishtest-win.zip' # url of compiled executable


def restart(worker_dir):
  """Restarts the worker, using the same arguments"""
  args = sys.argv[:]
  args.insert(0, sys.executable)
  if sys.platform == 'win32':
    args = ['"%s"' % arg for arg in args]

  os.chdir(worker_dir)
  os.execv(sys.executable, args) # This does not return !

def update():
  worker_dir = os.path.dirname(os.path.realpath(__file__))
  update_dir = os.path.join(worker_dir, 'update')
  if not os.path.exists(update_dir):
    os.makedirs(update_dir)

  worker_zip = os.path.join(update_dir, 'wk.zip')
  with open(worker_zip, 'wb+') as f:
    f.write(requests.get(WORKER_URL).content)

  zip_file = ZipFile(worker_zip)
  zip_file.extractall(update_dir)
  zip_file.close()
  prefix = os.path.commonprefix([n.filename for n in zip_file.infolist()])
  fishtest_src = os.path.join(update_dir, prefix)
  fishtest_dir = os.path.dirname(worker_dir) # fishtest_dir is assumed to be parent of worker_dir
  if not Py2Exe:
    copy_tree(fishtest_src, fishtest_dir)
    shutil.rmtree(update_dir)
    restart(worker_dir)
  else:
    finisher = file("finishUpdate.bat", 'w')
    lines = ['ping 127.0.0.1 -n 2 > nul',   # wait 2 seconds
             'xcopy %s\\* %s\\* /E /Y' % (fishtest_src, fishtest_dir), # copy tree
             'rmdir /s /q %s' % update_dir, # delete tree
             'start worker.exe %s' % " ".join(sys.argv[:])] # restart
    finisher.write('\n'.join(lines))
    finisher.close()
    subprocess.Popen("finishUpdate.bat")
    sys.exit(0)
    

