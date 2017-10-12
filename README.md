# pythonAccessLogDash
A Python based Access Log dashboard

To intialise the application please access the driectory where this is hosted and use python run.py. 

In the browser use http://localhost:5050/ in order to access the homepage, this page doesn't have any details as yet. 

You will need to use Sqlite3 as the database and use thelogFileSplitter.py & csvToSql.py scripts that I have previously uploaded to break the log file down and create a database in Sqlite3. Currently Sqlite3 is installed in C:\SQLite\Databases\ this will need to be changed in each of the scripts if it is required elsewhere. 

Bug:
  - There is currently a bug where the database will attempt to use favicon.ico, I haven't done any errorhandling on this as yet and is something for the next version 
