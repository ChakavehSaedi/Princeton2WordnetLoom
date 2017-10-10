# Princeton2WordnetLoom
This code, in Python 2.7, transfers data.noun from Princeton format into the format acceptable by WordNetLoom.

Make sure you have "MySQLdb" installed.

You can start the code by running "wnl_db_creator.py"
But before that you need to initialize variables that are marked with "<------ to be set" in the code in following files:
* wnl_db_creator.py
* dataMigrate.py

All required data files are saved in the data folder:
1- "en_wnet" contains English Princeton Wordnet version3.0 data and index files.
2- "dumps" is where the sql dumps are saved while the code progresses.
3- "table_default_values" contains all the default values to be used in WordnetLoom UI. There is a "read me" file in that folder which describes how the code uses the data and how you can modify it according to your needs.


This code is originally written to transfer data from Portuguese WordNet, as well as from English Princeton Wordnetin to WordnetLoom format ,so there are some values "both in the code and in set-up files" which are initialized based on the Portugues data. However it is possible to change them. For this purpose,
* In the code Look for "<------ to be set" and change the values according to your needs.
* For table default values, edit the files saved in ".../data/table_default_values/" considering the information in the "ReadMe" file located in the same folder.

In case you are to include more languages to your database, you need to 
1- inclued all the required and related data in the files located in "table_default_values" folder.
2- call "db_creator" for the third language.
NOTE: The code needs some changes to be able to handle more than two languages.
Going through the code you will be able to identify the required changes.
