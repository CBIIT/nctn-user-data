# nctn-user-data

Daily script to upload CTDC user data from NCTN to DCF

To run the extraction script, the user needs to first create three local variables, "NCTN_PASSWORD", "NCTN_USER_NAME", and "NCTN_USER_NAME", and then the user can execute the command below to extract user data from NCTN.

```python3 nctn_user_data_extract.py config/config_extract_example.yaml```

To run the data uploading script, the user needs to have the host address, the user name, and the private key file to get access to the sftp server, then the user can execute the command below to upload the extracted data.

```python3 nctn_user_data_upload.py config/config_upload_example.yaml```
