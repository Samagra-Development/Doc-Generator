function deleteFile(fileId) {
  var  myFolder, allFiles, file;
  //DriveApp.getFileById(fileId).setTrashed(true);
  Drive.Files.remove(fileId);
}

function myFunction(fileId) {
  try{
  deleteFile(fileId)
  msg = 'Deleted Successfully'
  var myReturn = '{"success":"'+ msg +'", "fileId":"'+ fileId +'"}';
    return myReturn;
  }catch(err) {
    //Failed to create a copy of the file
    var myReturn = '{"error":"'+ err +'", "fileId":"'+ fileId +'"}';
    return myReturn;
 }
}
//Function for catching data
function doGet(e) {
  var fileId = e.parameter.fileId;
  var url = myFunction(fileId);
  return ContentService.createTextOutput(url);
}

