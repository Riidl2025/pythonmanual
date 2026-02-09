from fastapi import FastAPI,Response,status
import boto3
import form_uploads
import pythonmanual.user_decision as user_decision
import pythonmanual.mail_mod as mail_mod
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values


config = dotenv_values(".env")
bucket = config.get("PITCHDECK_S3_BUCKET")


app = FastAPI()
origins = [] #Add requied origin headers
app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,  
      allow_methods=["*"],     
      allow_headers=["*"],     
  )

@app.get("/")
def index():
  return {"status" : "online"}

  
  

@app.get("/get_presigned_url")
def S3Uploads(startUpName : str):
  s3 = boto3.client('s3')
  out = s3.generate_presigned_post(
    bucket,
    Key = f"{startUpName}/${{filename}}",
  )
  return out


@app.post("/upload_startup_info")
def UplaodStartupInfo(form: form_uploads.Form,fileName : str):
    
    form_uploads.UploadStartupInfo(form= form,fileName = fileName)
    form_uploads.fillInitialStartupLog(form.startupName)
    form_uploads.fillInitialUserLog(form.startupName)
    mail_mod.sendMailToTeam(form.startupName)
    mail_mod.sendRegistrationMailToStartup(form.companyEmail)
     
    return form


@app.get("/user_decision")
def user_decision_handler(memberEmail: str,startupName : str,userHasApproved : bool , response : Response):
  code = user_decision.updateTables(startupName,memberEmail,userHasApproved)
  if(code == 200):
    response.status_code = status.HTTP_200_OK

  if(code == 401):
    response.status_code = status.HTTP_401_UNAUTHORIZED

  if(code == 404):
    response.status_code = status.HTTP_404_NOT_FOUND    

  if(code == 500):
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


  body = ""
  if code == 403 :
    body = "You have already made a decision"
  else:
    if(userHasApproved):
      body = f"You have approved {startupName} succesfully"
    else:
      body = f"You have disapproved {startupName} succesfully"

  return body


 