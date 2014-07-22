from distutils.core import setup
import py2exe

setup(console=['worker.py'],
	options={
                "py2exe":{
                        "skip_archive": 1
                }
        },
      data_files=[('requests', ['requests/cacert.pem'])]
)
