

## Template Document

The template document should have the placeholders in the following format:

```code
The name of student is <<0>> <<1>>  
Student's roll number is <<3>>  

```
 ## Google Variable Mapping Spreadsheet Details
    

-   It should contain the mapping details in sheet named mappingDetails.
    
-   It should have the options sheet named optionSheet.
    

Mapping sheet (mappingDetails) will have variable mapping in the following format

| variableInTemplate | variableType | variableInRawData |  
|--------------------|--------------|------------------------|  
|            0                         |     text     | studentFirstName |
| 1 | text  | studentLastName |
| 2 | imageLink | studentImage |
| 3 | options | myVariable1 |
| 4 | options | myVariable2 |

-   The options sheet (optionSheet) will have the mapping details in the following format:

| variable value | option1             | option2       | option3  |option4  | option5|option6       |option7|  
|----------------|---------------------|---------------|----------|---------|--------|--------------|-------|  
| myVariable1    | a::first option     | b::this might | c::value |d::value |    |           |   |     
| myVariable2    | a::this is an option| b::that value | c::value |d::value |e::value|f::values here|g::value available|
