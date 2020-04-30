// Update session, username and password cookie for testing and debugging in test functions
function pasteImage(body, replaceText, image) {
  //function for pasting image in place for text
  var next = body.findText(replaceText);                                   //Finding the text in document body
  var r = next.getElement();                                               //Getting the found element
  r.asText().setText("");                                                  //Setting text to ""
  var img = r.getParent().asParagraph().insertInlineImage(0, image).setWidth(250).setHeight(250);       //Insert image in place of "" with aspect ration 4:3
 }

function myFunction(fileName,mylist,templateId,sessionCookie,username,password) {

  var myError = null;
  var myUrl = null;
  var documentId = null;
  var TEMPLATE_ID = templateId;                                            //TEMPLATE_ID of the document
  try {
    var documentId = DriveApp.getFileById(TEMPLATE_ID).makeCopy().getId(); //Creating a copy of the file
  } catch(err) {
    //Failed to create a copy of the file
    myError = "Failed to access the template document. Please check permissions for the template.";
    var myReturn = '{"error":"'+ myError +'", "documentId":"'+ documentId +'", "fileName":"' + fileName +'", "url":"'+ myUrl +'"}';
    return myReturn;
 }

  var drivedoc = DriveApp.getFileById(documentId);                         //Fetching file by ID
  drivedoc.setName(fileName);                                              //Renaming the file
  var doc = DocumentApp.openById(documentId);                              //Opening the new created file by document ID
  var body = doc.getBody();                                                //Getting all the contents of the document body in var body
  var x;                                                                   //Variable to be used for Iterations
  var end = mylist.length;                                                 //Getting the length of the list (fetched through API)

  for (x=1; x<=end; x+=1){
    var element = '<<' + x + '>>';
    if (mylist[x-1].indexOf('http') > -1) {
      options = {muteHttpExceptions: true};
      options.headers = {"Authorization": "Basic " + Utilities.base64Encode(username + ":" + password), "Cookie": "JSESSIONID="+ sessionCookie};
      var resp = UrlFetchApp.fetch(mylist[x-1], options);                  //fetching the image from the url
      if(resp.getResponseCode() === 200) {
        var image = resp.getBlob();                                        //Getting the image as blob in var image
        pasteImage(body, element, image)                                   //Pasting the image in place of placeholder using function pasteImage
      } else if (resp.getResponseCode() === 401) {
        myError = "Image Hosting Server Authentication failed";
        var myReturn = '{"error":"'+ myError +'", "documentId":"'+ documentId +'", "fileName":"' + fileName +'", "url":"'+ myUrl +'"}';
        return myReturn;
      } else {
        body.replaceText(element, "[NO_IMAGE_FOUND]");                     //Replacing the placeholders with text
      }
    } else {
     try {
       if (mylist[x-1]) {
         body.replaceText(element, mylist[x-1]);                           //Replacing the placeholders with text
       } else {
         body.replaceText(element, "[NO_TEXT_FOUND]");                     //Replacing the placeholders with text
       }
     } catch(err) {
       //Failed to write text to placeholder
       myError = "Failed to write text to placeholder.";
       var myReturn = '{"error":"'+ myError +'", "documentId":"'+ documentId +'", "fileName":"' + fileName +'", "url":"'+ myUrl +'"}';
       return myReturn;
     }
   }
  }
  drivedoc.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);

  myUrl = "https://docs.google.com/document/d/" + documentId + "/export?format=pdf";
  var myReturn = '{"error":"'+ myError +'", "documentId":"'+ documentId +'", "fileName":"' + fileName +'", "url":"'+ myUrl +'"}';
  return myReturn;
}

//Function for catching data
function doGet(e) {
  var fileName = e.parameter.fileName;
  var mylist = e.parameter.mylist;
  var templateId = e.parameter.templateId;
  var sessionCookie = e.parameter.sessionCookie;
  var username = e.parameter.username;
  var password = e.parameter.password;
  var newlist = JSON.parse(mylist);
  var url = myFunction(fileName,newlist,templateId,sessionCookie,username,password);
  return ContentService.createTextOutput(url);
}

//Function for testig (it works great)
function testit_working() {
  var fileName = "testItWorking";
  var templateId = '1J-QGxmQ6LPkDfC2xkuUTxpM62jJAU6YxOpLUYpskUWs';
  var sessionCookie = 'BAA6C0042032A3673DC00DEEE26F0A9A';
  var username = '';
  var password = '';
  var mylist = ["KULLU", "KULLU-2", "UP Kullu", "GMS NEOLI", "31.97197707", "77.12937994", "1255", "6.432", "h", "Level0", "Yes", "Yes", "Not_Applicable", "Yes", "Very_Good", "Good", "Below_Average", "2", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "1", "", "Not_Reached", "Not_Applicable", "2", "1", "1", "No", "No", "", "1", "1", "NA", "No", "", "Yes", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "Yes", "Yes", "Yes", "Decrease", "No", "", "", "Yes", "Yes", "Not_Applicable", "No", "", "No", "", "Yes", "Boundary wall needed as during rain water from near by stream enter in the school ground not safe for schoool children", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "Yes", "Yes", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "Yes", "Yes", "Not_Applicable", "Yes", "One more toilet needed .", "Yes", "Yes", "Not_Applicable", "Yes", "Yes", "Yes", "Not_Applicable", "Yes"];
  var url = myFunction(fileName,newlist,templateId,sessionCookie,username,password);
  return ContentService.createTextOutput(url);
}

//Function for testing, it has wrong image url
function testit_wrong_image_url() {
  var fileName = "testitWrongUrl";
  //var templateId = '1J-QGxmQ6LPkDfC2xkuUTxpM62jJAU6YxOpLUYpskUWs';       //Sample Doc 1
  var templateId = '1AnaVW6Cdu_30FDda14aLz3hVaisiHeaDlb172cLxJCU';         //Sample Doc 2
  var sessionCookie = 'BAA6C0042032A3673DC00DEEE26F0A9A';
  var username = '';
  var password = '';
  //The url of few images are incorrect and for others it is correct
  var mylist = ["KULLU", "KULLU-2", "UP Kullu", "GMS NEOLI", "31.97197707", "77.12937994", "1255", "6.432", "h", "Level0", "Yes", "Yes", "Not_Applicable", "Yes", "Very_Good", "Good", "Below_Average", "2", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "1", "", "Not_Reached", "Not_Applicable", "2", "1", "1", "No", "No", "", "1", "1", "NA", "No", "", "Yes", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "Yes", "Yes", "Yes", "Decrease", "No", "", "", "Yes", "Yes", "Not_Applicable", "No", "", "No", "", "Yes", "Boundary wall needed as during rain water from near by stream enter in the school ground not safe for schoool children", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "Yes", "Yes", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image", "Yes", "Yes", "Not_Applicable", "Yes", "One more toilet needed .","2", "1", "1", "No", "No", "No", "No"];
  var url = myFunction(fileName,newlist,templateId,sessionCookie,username,password);
  return ContentService.createTextOutput(url);
}

function fetch_image_testing() {
  url = 'http://aggregate.cttsamagra.xyz:8080/view/binaryData?blobKey=BRCC_V1%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FBRCCs_QM_Question%5B%40key%3Duuid%3A6df88903-ccee-4e4d-af9b-d9b1ea78a2a4%5D%2FAcademic_interventions%3ALOCharts_Image';
  var username = '';
  var password = '';
  options = {muteHttpExceptions: true};
  options.headers = {"Authorization": "Basic " + Utilities.base64Encode(username + ":" + password), "Cookie": "JSESSIONID=06470CD95014EB382D1780B3EC939402"};
  Logger.log(options.headers)
  var resp = UrlFetchApp.fetch(url, options);                              //fetching the image from the url
  if(resp.getResponseCode() === 200) {
    Logger.log("success")
  } else if (resp.getResponseCode() === 401) {
    Logger.log("failed")
}
}
//The app script only needs to be published as web app and not needs to be shared publically
//Things Handled:
//If image is not found on the url [NO_IMAGE_FOUND] is pasted in the template
//If no text is found then [NO_TEXT_FOUND] is pasted pasted in the template
//Image height and width set to 4:3 (300,225) (limitation)
//exceptions handled (error and url returned in every case)
//Odk failing Authorization from app script as it uses cookies for Authorization - Fixed by sending cookie in headers
