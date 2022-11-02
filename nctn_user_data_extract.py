from config import Config
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import os
import argparse
from bento.common.utils import get_logger
import numpy as np
import re

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

df = pd.DataFrame()
df['user name'] = user_name_list
df['login'] = login_list
df['authority'] = authority_list
df['roles'] = roles
df['email'] = email
df['project_id'] = project_id_list
df['request_id'] = request_id_list

subfolder_dirsctory = config.output_folder
if not os.path.exists(subfolder_dirsctory):
    os.mkdir(subfolder_dirsctory)

#df.to_csv('ctdc_user.csv', sep = "\t", index = False)

new_project_id_list = list(set(project_id_list))
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

for project_id in new_project_id_list:
    new_df = df.loc[df['project_id'] == project_id].loc[:, df.columns != 'request_id']
    new_df = new_df.drop_duplicates()
    new_df = new_df.replace(r'^\s*$', np.nan, regex=True)
    new_df = new_df.dropna(subset=['login', 'authority'])
    new_df = new_df.reset_index()
    login_index_list = []
    login_index = 0
    for login in new_df['login']:
        if not re.fullmatch(regex, login):
            login_index_list.append(login_index)
        login_index += 1
    new_df = new_df.drop(df.index[login_index_list])
    new_df = new_df.reset_index()
    if (len(new_df) > 0):
        file_name = subfolder_dirsctory + 'authentication_file_' + project_id + '.csv'
        new_df.to_csv(file_name, sep = ",", header=True, index=False)
        log.info('Successfully extract data file {}'.format(os.path.basename(file_name)))