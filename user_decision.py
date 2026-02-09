from hashlib import md5
from pythonmanual.resources import member_log_table,approve_reject_table,startup_table,team_email_list
from pythonmanual.mail_mod import sendFinalDecisionMailToStartup

THRESHOLD_NUMBER = 3   # no of votes required for the final_mail to be sent to the startup



def updateTables(startupName : str , userEmail : str,userHasApproved : bool):
  print(userEmail)
  if(userEmail not in team_email_list):
    return 401
  
  res = member_log_table.get_item(
    Key = {"startup" : startupName}
  )

  if(not res['Item']):
    return 404
  
  if(res['Item']['members'][userEmail] == "TBD"):
    
    userChoice = ""
    attribNameToUpdate = ""
    if(userHasApproved):
      userChoice = "approved"
      attribNameToUpdate = "approvals"
      
    else :
      userChoice = "rejected"
      attribNameToUpdate = "rejections"

    member_log_table.update_item(
        Key = {"startup" : startupName},
        UpdateExpression = f"SET members.#mail = :c",
        ExpressionAttributeValues={":c": userChoice},
        ExpressionAttributeNames={"#mail" : userEmail}
      )
    
    approve_reject_table.update_item(
        Key = {"startup" : startupName},
        UpdateExpression = f"ADD #attribName :val",
        ExpressionAttributeValues={":val": 1},
        ExpressionAttributeNames={"#attribName" : attribNameToUpdate}
      )


    item = approve_reject_table.get_item(
      Key = {"startup" : startupName}
    )
    num_approvals = item["Item"]["approvals"] 
    num_rejections = item["Item"]["rejections"] 
    if((num_approvals >= THRESHOLD_NUMBER) or (num_rejections >= THRESHOLD_NUMBER)) and (item["Item"]["status"] == "pending"):
      startup_id = md5(startupName.encode()).hexdigest()
      startup_email = startup_table.get_item(Key = {"id" : startup_id})["Item"]["companyEmail"]
      status = ""

      if(num_approvals >= THRESHOLD_NUMBER):
        sendFinalDecisionMailToStartup(startup_email,True)
        status = "ACCEPETED"

      else:
        sendFinalDecisionMailToStartup(startup_email,False)
        status = "REJECTED"

      approve_reject_table.update_item(
        Key = {"startup" : startupName},
        UpdateExpression = f"SET #s = :s",
        ExpressionAttributeValues={":s": status},
        ExpressionAttributeNames = {"#s" : "status"}
      )

  else:
    return 403
    

