from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from hashlib import md5
from resources import startup_table
from urllib.parse import quote_plus
from dotenv import dotenv_values
from resources import calendar_invite,api_root,team_email_list




class Mailer:
  
  def __init__(self):
    config = dotenv_values(".env")
    SenderMailID = config.get("USER_EMAIL")
    password = config.get("USER_PASSWORD")
    self.mailID = SenderMailID
    self.server = SMTP("smtp.gmail.com",587)
    self.server.ehlo()
    self.server.starttls()
    self.server.login(SenderMailID,password)

  def sendMail(self,receiverMail : str, htmlMailBody: str):
    message = MIMEMultipart("alternative")
    message["To"] = receiverMail
    message["From"] = self.mailID
    html_Body = MIMEText(htmlMailBody, "html")
    message.attach(html_Body)
    
    self.server.sendmail(
      self.mailID, receiverMail, message.as_string()
    )
    





def teamMailWrapper(startupName : str,userEmail : str,startUpPitchdeckUrl : str):
  memberEmail =  quote_plus(userEmail)
  startupNameQ = quote_plus(startupName)
  email_body = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incubation Registration</title>
  </head>
  <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, Helvetica, sans-serif; height: auto; width: auto;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8; padding:20px;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:6px; padding:24px;">
            
            <tr>
              <td style="font-size:20px; font-weight:bold; color:#222222; padding-bottom:8px;">
                {startupName} has registered for incubation
              </td>
            </tr>

            <tr>
              <td style="padding-top:10px;padding-bottom: 10px;">
                <a href={startUpPitchdeckUrl}
                   target="_blank"
                   style="font-size:14px; color:#1a73e8; text-decoration:none;">
                   Pitch deck here
                </a>
              </td>
            </tr>

            <tr>
              <td style="font-size:14px; color:#555555; line-height:1.6; padding-bottom:24px;">
                Please review {startupName}'s pitch deck and choose one of the actions below.
              </td>
            </tr>

            <tr>
              <td align="center">
                <table border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td align="center" style="padding-bottom: 10px;">
                      <a href="{api_root}/user_decision?memberEmail={memberEmail}&startupName={startupNameQ}&userHasApproved=true"
                         style="display:block; background-color:#28a745; color:#ffffff;
                                text-decoration:none; padding:12px; border-radius:4px;
                                font-size:14px; font-weight:bold; width: 100px; text-align:center;">
                        APPROVE
                      </a>
                    </td>
                  </tr>
                  <tr>
                    <td align="center">
                      <a href="{api_root}/user_decision?memberEmail={memberEmail}&startupName={startupNameQ}&userHasApproved=false"
                         style="display:block; background-color:#dc3545; color:#ffffff;
                                text-decoration:none; padding:12px; border-radius:4px;
                                font-size:14px; font-weight:bold; width: 100px; text-align:center;">
                        REJECT
                      </a>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="font-size:10px; color:#999999; padding-top:20px; text-align:center;">
                This is an automated notification. Please do not reply.
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
  return email_body


registration_mail = """<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Registration Successful</title>
  </head>
  <body style="margin:0; padding:0; background-color:#f7f2f2; font-family:Arial, Helvetica, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f7f2f2; padding:30px 0;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:8px; overflow:hidden;">


        
        <tr>
          <td style="padding:22px 28px; background-color:#7a1f2b; color:#ffffff;">
            <h1 style="margin:0; font-size:20px; font-weight:600;">
              Registration Successful
            </h1>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:28px; color:#3f3f46; font-size:14px; line-height:1.6;">
            <p style="margin-top:0;">
              Hello,
            </p>

            <p>
              Your registration for incubation has been <strong>successfully completed</strong>.
            </p>

            <p style="margin-bottom:0;">
              Our team will review your application and contact you with next steps shortly.
            </p>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:16px 28px; background-color:#fafafa; color:#7a1f2b; font-size:12px; text-align:center;">
            © riidl Incubation Program
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

  </body>
</html>
"""


accepted_mail = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incubation Request Approved</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f8; font-family: Arial, Helvetica, sans-serif;">
    
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f6f8; padding: 40px 0;">
        <tr>
            <td align="center">
                
                <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-top: 6px solid #800000;">
                    
                    <tr>
                        <td align="center" style="padding: 40px 0 20px 0;">
                            <img src="https://riidl.org/assets/riidlLogo-CJMX4MZs.png" 
                                 alt="Company Logo" 
                                 width="80" 
                                 style="display: block; width: 80px; height: auto;">
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding: 0 40px;">
                            <h3 style="color: #800000; margin: 0; font-size: 24px; font-weight: bold;">
                                Incubation Request Approved
                            </h3>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding: 20px 40px;">
                            <p style="color: #555555; font-size: 16px; line-height: 1.5; margin: 0;">
                                Your incubation request has been approved!<br>
                                Please book your slot immediately using the link below.
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding-bottom: 40px;">
                            <table border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td align="center" style="border-radius: 5px;" bgcolor="#800000">
                                        <a href="{calendar_invite}" 
                                           target="_blank" 
                                           style="font-size: 16px; font-family: Arial, sans-serif; color: #ffffff; text-decoration: none; padding: 12px 30px; border-radius: 5px; border: 1px solid #800000; display: inline-block; font-weight: bold;">
                                            Book Slot
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="background-color: #eeeeee; padding: 20px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                            <p style="color: #999999; font-size: 12px; margin: 0;">
                                &copy; 2026 Our Company. All rights reserved.
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>

</body>
</html>"""



rejection_mail = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incubation Request Approved</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f8; font-family: Arial, Helvetica, sans-serif;">
    
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f6f8; padding: 40px 0;">
        <tr>
            <td align="center">
                
                <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-top: 6px solid #800000;">
                    
                    <tr>
                        <td align="center" style="padding: 40px 0 20px 0;">
                            <img src="https://riidl.org/assets/riidlLogo-CJMX4MZs.png" 
                                 alt="Company Logo" 
                                 width="80" 
                                 style="display: block; width: 80px; height: auto;">
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding: 0 40px;">
                            <h3 style="color: #800000; margin: 0; font-size: 24px; font-weight: bold;">
                                Incubation Request Rejected
                            </h3>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding: 20px 40px;">
                            <p style="color: #555555; font-size: 16px; line-height: 1.5; margin: 0;">
                                Please try next time<br>
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="background-color: #eeeeee; padding: 20px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                            <p style="color: #999999; font-size: 12px; margin: 0;">
                                &copy; 2026 Our Company. All rights reserved.
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>

</body>
</html>"""



def sendRegistrationMailToStartup(startUpEmail : str):
  m = Mailer()
  m.sendMail(startUpEmail, registration_mail)
  return True


def sendFinalDecisionMailToStartup(startupEmail : str,isAccepted : bool):
  m = Mailer()
  if(isAccepted):
    mail_body = accepted_mail
  else:
    mail_body = rejection_mail

  m.sendMail(startupEmail,mail_body)   
  return True



teamEmailList = team_email_list

def sendMailToTeam(startupName : str):
  m = Mailer()
  startup_id = md5((startupName.encode())).hexdigest()
  res = startup_table.get_item(Key = {"id" : startup_id})
  pitchDeckUrl = res["Item"]["pitchDeckUrl"]
  try :
    for mailID in teamEmailList:
      mail = teamMailWrapper(startupName,mailID,pitchDeckUrl)
      m.sendMail(mailID,mail)
  except :
    return     

  return True            



