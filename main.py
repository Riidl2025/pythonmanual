from fastapi import FastAPI,Response,status
from form_uploads import fillInitialUserLog,fillInitialStartupLog,UploadStartupInfo,Form
from user_decision import updateTables
from mail_mod import sendMailToTeam,sendRegistrationMailToStartup
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from resources import s3_client

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
  out = s3_client.generate_presigned_post(
    bucket,
    Key = f"{startUpName}/${{filename}}",
  )
  return out


@app.post("/upload_startup_info")
def UplaodStartupInfo(form: Form,fileName : str):
    
    UploadStartupInfo(form = form,fileName = fileName)
    fillInitialStartupLog(form.startupName)
    fillInitialUserLog(form.startupName)
    sendMailToTeam(form.startupName)
    sendRegistrationMailToStartup(form.companyEmail)
     
    return form


@app.get("/user_decision")
def user_decision_handler(memberEmail: str,startupName : str,userHasApproved : bool , response : Response):
  code = updateTables(startupName,memberEmail,userHasApproved)
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


 