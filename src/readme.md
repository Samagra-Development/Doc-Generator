## 1. Architecture

The following diagram illustrates the overall architecture of PDF Builder solution that allows various applications to interact with the PDF Builder solution to send requests and retrieve outputs.


![enter image description here](https://i.ibb.co/NSk5p2H/Architecture-Diagram-PDF-Builder.png)


A brief description of the function of each element of the architecture is provided below.

a) **External Application**: Any mobile application, data storage and publishing platform that either request for pdf generation or search pdf status.

b) **Auth Server**: It verifies whether request is made by verified user or not and return token.

c) **PDF Server**: It receives request and pass this data to database and send request to Pdf Base.

d) **Queue Manager**: It save all the request and process it whenever possible.

e) **Database**: It saves requested data and and progress of pdf generation process and if pdf is generated then it’s path is save.

f) **PDF Base**:It is middleware which takes data from database and interact with plugin for pdf generation and then send pdf data to database.

g) **Plugin**:

1. **Request Fetcher**:It fetch variable mapping content from data source which can be excel sheet.

2. **Variable Mapper**: This will fetch the mapping variables and option variable from the data source.

3. **Pdf Creator**: This will map the data provided by the variable mapper with the data provided in the request(i.e by the request fetcher) and then encode mapped data in the url format and then call the app script which take the request and write all the content to doc and then return the pdf link to that doc.

4. **Pdf Uploader**: It take pdf url from pdf creator and then upload this pdf to storage which can be disk storage or storage provided by some third party.

5. **Retrieve Pdf** : It take pdf name from pdfbase and return the pdf content.

h) **Data Source**: It is source from where we get the data and it can be google sheet.

i) **Storage**: Here we save the pdf .

j) **Logging Module**: This module get logging data from pdf base,plugin,queue manager and pass this data to central logging system.

k) **Central Logging System**: It will save error if any occur while proccessing request.
