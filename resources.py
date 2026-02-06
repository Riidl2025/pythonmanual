from dotenv import dotenv_values
import boto3
import csv

config = dotenv_values(".env")
mem_dec_table = config.get("MEMBER_DECISION_TABLE")
app_rej_table = config.get("APPROVAL_REJECTION_TABLE")
startup_info_table = config.get("STARTUP_INFO_TABLE")
api_root =  config.get("BASE_API_ENDPOINT")
calendar_invite = config.get("CALENDAR_INVITE")




member_log_table = boto3.resource("dynamodb").Table(mem_dec_table)
approve_reject_table = boto3.resource("dynamodb").Table(app_rej_table)
startup_table = boto3.resource("dynamodb").Table(startup_info_table)

def read_single_column_from_csv(file):
  data_list = []
  with open(file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
      if row:
        data_list.append(row[0])
  return data_list


team_email_list = read_single_column_from_csv("userMails.csv")
