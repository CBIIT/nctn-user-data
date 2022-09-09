from os import environ
import yaml


class Config:
    def __init__(self, config_file):
        # Read the credentials from local variables
        self.password = environ.get('NCTN_PASSWORD')
        self.username = environ.get('NCTN_USER_NAME')
        self.api = environ.get('NCTN_API')
        with open(config_file) as f:
            self.data = yaml.load(f, Loader = yaml.FullLoader)
        self.output_folder = self.data['OUTPUT_FOLDER']


