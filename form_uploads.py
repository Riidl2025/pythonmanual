from pydantic import BaseModel
from botocore.exceptions import ClientError
from  hashlib import md5
from datetime import datetime
from mail_mod import teamEmailList
from urllib.parse import quote_plus,unquote
from resources import member_log_table,approve_reject_table,startup_table
from dotenv import dotenv_values



class Form(BaseModel):
  startupName: str
  founderName: str
  description : str
  startupStage : str
  hearAbout:str
  isRegisteredCompany : str
  fromSomaiya : str
  companyEmail: str
  companyMobile :str
  industries:str

initalUserLogMap = {}
for mail in teamEmailList:
  initalUserLogMap[mail] = "TBD"


config = dotenv_values(".env")

bucket = config.get("PITCHDECK_S3_BUCKET")

def fillInitialUserLog(startUpName : str):
  table = member_log_table
  try:
    table.put_item(
      Item = {
        "startup" : startUpName,
        "members" : initalUserLogMap
      }
    )
  except ClientError as err:
    print(err)
    return False

  return True




def fillInitialStartupLog(startUpName : str):

  table = approve_reject_table
  try : 
    table.put_item(
      Item = {
        "startup" : startUpName,
        "approvals" : 0,
        "rejections" : 0,
        "status" : "pending"
      }
    )
  except ClientError as err:
    print(err)
    return False 

  return True

def UploadStartupInfo(form: Form,fileName : str):
  startUp_dic = form.model_dump()
  startUp_dic["id"] = md5(form.startupName.encode()).hexdigest()
  startUp_dic["pitchDeckUrl"] = unquote(quote_plus(f"https://{bucket}.s3.amazonaws.com/{form.startupName}/{fileName}"))
  now = datetime.now().strftime("%d-%m-%y %H:%M:%S")
  startUp_dic["createdAt"] = now
  startUp_dic["updatedAt"] = now
  startUp_dic["status"] = "submitted"
  table = startup_table
  try :
    table.put_item(
    Item = startUp_dic
  )
    return True
    
  except ClientError as err:
    print(err)
    return False
  

