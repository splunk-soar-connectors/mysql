[comment]: # "Auto-generated SOAR connector documentation"
# MySQL

Publisher: Splunk  
Connector Version: 2\.1\.2  
Product Vendor: Oracle Corporation  
Product Name: MySQL  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app supports investigative actions against a MySQL database

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2017-2021 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
This app will ignore the HTTP_PROXY and HTTPS_PROXY environment variables, as it does not use HTTP
to connect to the database.  
Below are the ports used by MySQL Server.

|         Service Name      | Port | Transport Protocol |
|---------------------------|------|--------------------|
|          **MySQL(mysql)** | 3306 | tcp                |
|          **MySQL(mysql)** | 3306 | udp                |

  

## SDK and SDK Licensing details for the app

### PyMySQL

This app uses the PyMySQL module, which is licensed under MIT License('MIT').


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a MySQL asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**host** |  required  | string | Hostname or IP address
**username** |  required  | string | Username
**password** |  required  | password | Password
**database** |  required  | string | Database Name

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list columns](#action-list-columns) - List the columns of a table  
[list tables](#action-list-tables) - List the tables in the database  
[run query](#action-run-query) - Run a query against a table or tables in the database  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list columns'
List the columns of a table

Type: **investigate**  
Read only: **True**

Describes the structure of a table in the database by displaying information about its columns\. The only tables which it will be able to query for must have a name composed of only alphanumeric characters \+ '\_' and '$'\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of table | string |  `mysql table name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.table\_name | string |  `mysql table name` 
action\_result\.data\.\*\.Default | string | 
action\_result\.data\.\*\.Extra | string | 
action\_result\.data\.\*\.Field | string | 
action\_result\.data\.\*\.Key | string | 
action\_result\.data\.\*\.Null | string | 
action\_result\.data\.\*\.Type | string | 
action\_result\.summary\.total\_rows | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list tables'
List the tables in the database

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.table\_name | string |  `mysql table name` 
action\_result\.summary\.total\_rows | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'run query'
Run a query against a table or tables in the database

Type: **investigate**  
Read only: **False**

It is recommended to use the <b>format\_vars</b> parameter when applicable\. For example, if you wanted to find a specific IP, you could set <b>query</b> to a formatted string, like "select \* from my\_hosts where ip = %s" \(note the use of %s\), and set <b>format\_vars</b> to the IP address\. This will ensure the inputs are safely sanitized and avoid SQL injection attacks\. Regardless of the type of input it's expecting, the only format specifier which should be used is %s\.<br>Setting <b>no\_commit</b> will make it so the App does not commit any changes made to the DB \(So, you can ensure its a run only query\)\. However, many statements on MySQL will implicitly commit \(as can be read about <a href="https\://dev\.mysql\.com/doc/refman/5\.6/en/implicit\-commit\.html">here</a>\) meaning that this parameter will have no effect in cases where these statements are used\.<br><br>The <b>format\_vars</b> parameter accepts a comma seperated list\. You can escape commas by surrounding them in double quotes, and escape double quotes with a backslash\. Assuming you have a list of values for the format vars, you can employ this code in your playbooks to properly format it into a string\:<br> <code>format\_vars\_str = ','\.join\(\['"\{\}"'\.format\(str\(x\)\.replace\('\\\\', '\\\\\\\\'\)\.replace\('"', '\\\\"'\)\) for x in format\_vars\_list\]\)</code>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  required  | Query string | string |  `sql query` 
**format\_vars** |  optional  | Comma seperated list of variables | string | 
**no\_commit** |  optional  | Do not commit changes to database | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.format\_vars | string | 
action\_result\.parameter\.no\_commit | boolean | 
action\_result\.parameter\.query | string |  `sql query` 
action\_result\.data\.\* | string | 
action\_result\.summary\.total\_rows | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 