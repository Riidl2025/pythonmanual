from dotenv import dotenv_values
from boto3 import resource,client
from csv import reader
from os import environ

config = dotenv_values(".env")
mem_dec_table = config.get("MEMBER_DECISION_TABLE")
app_rej_table = config.get("APPROVAL_REJECTION_TABLE")
startup_info_table = config.get("STARTUP_INFO_TABLE")
api_root =  config.get("BASE_API_ENDPOINT")
calendar_invite = config.get("CALENDAR_INVITE")
access_key = environ.get("AWS_ACCESS_KEY_ID")
secret_access_key = environ.get("AWS_SECRET_ACCESS_KEY")
region = environ.get("AWS_REGION")



dynamodb_res = resource(
  service_name = "dynamodb",
  aws_access_key_id = access_key,
  aws_secret_access_key = secret_access_key,
  region_name = region
  )

s3_client = client(
  service_name = 's3',
  aws_access_key_id = access_key,
  aws_secret_access_key = secret_access_key,
  region_name = region
  )

member_log_table = dynamodb_res.Table(mem_dec_table)
approve_reject_table = dynamodb_res.Table(app_rej_table)
startup_table = dynamodb_res.Table(startup_info_table)

def read_single_column_from_csv(file):
  data_list = []
  with open(file, mode='r', newline='', encoding='utf-8') as file:
    rd = reader(file)
    for row in rd:
      if row:
        data_list.append(row[0])
  return data_list


team_email_list = read_single_column_from_csv("userMails.csv")
