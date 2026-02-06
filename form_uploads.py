from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError
import hashlib
import datetime
from pythonmanual.mail_mod import teamEmailList
from urllib.parse import quote_plus,unquote
from pythonmanual.resources import mem_dec_table,app_rej_table,startup_info_table
from dotenv import dotenv_values



class Form(BaseModel):
  startupName: str
  founderName: str
  description : str
  startupStage : str
  hearAbout:str
  isRegisteredCompany : bool
  fromSomaiya : bool
  companyEmail: str
  companyMobile :str
  industries:str

initalUserLogMap = {}
for mail in teamEmailList:
  initalUserLogMap[mail] = "TBD"


config = dotenv_values(".env")

bucket = config.get("PITCHDECK_S3_BUCKET")

def fillInitialUserLog(startUpName : str):
  tableName = mem_dec_table
  table = boto3.resource("dynamodb").Table(tableName)
  try:
    table.put_item(
      Item = {
        "startup" : startUpName,
        "members" : initalUserLogMap
      }
    )
  except ClientError:
    return False

  return True




def fillInitialStartupLog(startUpName : str):
  tableName = app_rej_table
  table = boto3.resource("dynamodb").Table(tableName)
  try : 
    table.put_item(
      Item = {
        "startup" : startUpName,
        "approvals" : 0,
        "rejections" : 0,
        "status" : "pending"
      }
    )
  except ClientError:
    return False 

  return True

def UploadStartupInfo(form: Form,fileName : str):
  startUp_dic = form.model_dump()
  startUp_dic["id"] = hashlib.md5(form.startupName.encode()).hexdigest()
  startUp_dic["pitchDeckUrl"] = unquote(quote_plus(f"https://{bucket}.s3.amazonaws.com/{form.startupName}/{fileName}"))
  now = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
  startUp_dic["createdAt"] = now
  startUp_dic["updatedAt"] = now
  startUp_dic["status"] = "submitted"
  table = boto3.resource("dynamodb").Table(startup_info_table)
  try :
    table.put_item(
    Item = startUp_dic
  )
    return True
    
  except ClientError:
    return False
  

