  

# 1. High Level Specifications

## 1. Transaction Flow
	 
The Sequence Diagram has the following objects:
External Devices, Pdf Base, GoogleDocsPlugin, Output Database
![enter image description here](https://i.ibb.co/ZMRRQS8/detailarchitecture-3.png)

These objects have 10 flows which are as briefly explained below.

 1.  In this Data from the external device to **Pdf** **Base** is sent. It’ll add data to the database and will assign a UniqueID to the request.
    
 2.  Data from **Pdf Base** is sent to Plugin Request Fetcher.
    
 3.  **Request fetcher** will return the error,raw data and tags to the Pdf Base. Raw Data include received data and configuration data
    
 4.  The mapped data is then sent to Plugin **Values Mapper** which will fetch mapping values and optionsvalue from sheet.
    
 5.  The **Values Mapper** will return error or raw_data which will include mapping values and options value.
    
 6.  The mapped data will then sent to **Plugin Pdf Creator**. Which will then which will then map the mapping values and options value to that of the received data and then urlencode this data and pass this data to app script and app script either return error or generated pdf url.
    
 7.  **Plugin Pdf Creator** then either return generated pdf url or error to pdf builder.
    
 8.  The data (pdf url) is then given to the Plugin Pdf Uploader which will then upload the PDF to local server or third party storage.
    
 9.  The **Plugin Pdf Uploader** will return error or filename to pdf builder.
    
 10.  The data relevant to the request is then exported from the Pdf builder to the **Output Database**.
 

## 2. Failure
 

 1.  **Failure at 2 & 4:**  The failure can occur in these steps due to permission error i.e. the project doesn’t have the read-only permission to access the google spreadsheet.
            
  2.  **Failure at 6:** In these steps failures can occur due to mapping error i.e. due to incorrect mapping. Whereas incorrect mapping means that the mapping from the sheet does not match the data provided. And error can also occur due to App Script execution can occur e.g. if we exceed the number of url fetches.
            
  3.  **Failure at 8:** In this case error can happen due to downloading error, which may mean the storage in the external volume is full OR download directory is not found.
            
  4.  **Failure at 10**:  In these cases no error is expected.

