from config import Config
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import os
import argparse
from bento.common.utils import get_logger

parser = argparse.ArgumentParser(description='Extract user data from NCTN')
parser.add_argument("config_file", help="Name of Configuration File to run the File Uploader")
args = parser.parse_args()
config = Config(args.config_file)
log = get_logger('NCTN_USER_DATA_EXTRACT')

user_name_list = []
login_list = []
authority_list = []
project_id_list = []
request_id_list = []
roles = []
email = []
phone = []
status = []
permission_set = []
created = []

r = requests.get(config.api, auth = HTTPBasicAuth(config.username, config.password))
data_set = r.content.decode("utf-8")
data_list = json.loads(data_set)

log.info('Start extracting data files')
for data in data_list:
    user_name_list.append(data[0])
    login_list.append(data[1])
    authority_list.append(data[2])
    project_id_list.append(data[3])
    request_id_list.append(data[4])
    roles.append('')
    email.append('')
    phone.append('')
    status.append('')
    permission_set.append('')
    created.append('')

df = pd.DataFrame()
df['user name'] = user_name_list
df['login'] = login_list
df['authority'] = authority_list
df['roles'] = roles
df['email'] = email
df['phone'] = phone
df['status'] = status
df['project_id'] = project_id_list
df['Permission set'] = permission_set
df['created'] = created
df['request_id'] = request_id_list

subfolder_dirsctory = config.output_folder
if not os.path.exists(subfolder_dirsctory):
    os.mkdir(subfolder_dirsctory)

#df.to_csv('ctdc_user.csv', sep = "\t", index = False)

new_project_id_list = list(set(project_id_list))

for project_id in new_project_id_list:
    new_df = df.loc[df['project_id'] == project_id].loc[:, df.columns != 'request_id']
    file_name = subfolder_dirsctory + 'authentication_file_' + project_id + '.csv'
    new_df.to_csv(file_name, sep = ",", header=True, index=False)
    log.info('Successfully extract data file {}'.format(os.path.basename(file_name)))