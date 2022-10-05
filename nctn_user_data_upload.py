import pysftp
import glob
import logging
import argparse
import yaml
import os

parser = argparse.ArgumentParser(description='Upload NCTN user data')
parser.add_argument("config_file", help="Name of Configuration File to run the File Uploader")
args = parser.parse_args()
with open(args.config_file) as f:
    config = yaml.load(f, Loader = yaml.FullLoader)

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
log = logging.getLogger('NCTN_USER_DATA_UPLOAD')
srv = pysftp.Connection(host=config['HOST'], username=config['USERNAME'], private_key=config['PRIVATE_KEY'], cnopts=cnopts)
remote_path = 'dev'
log.warning('Start uploading data files')

try:
    srv.chdir(remote_path)
except IOError:
    srv.mkdir(remote_path)
    srv.chdir(remote_path)
for file in glob.glob(os.path.join(config['AUTHENTICATION_FILE_LOCATION'], '*.enc')):
    srv.put(file)
    log.info('Successfully upload data file {}'.format(os.path.splitext(file)[0]))
# Close the connection
log.info('All data files successfully uploaded')
srv.close()
