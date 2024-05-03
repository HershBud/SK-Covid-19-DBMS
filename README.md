
# **South-Korea-COVID-19-DBMS**

## Overview
This repository contains the dataset and scripts for creating, running, and interacting with a South Korea Covid-19 database on your local machine.


## Downloading
Download all files in the repository into the same folder. Keep the path of this folder on hand, preferrably copied to the clipboard for creation of the database. 

## Creating the database
To create the database, run **`Database_Creation.py`**. This will automatically create the database, create the tables, and fill in the tables with the appropriate data from the the dataset. For the username and password, fill in your own credentials, as the ones that auto-fill may not work out of the box with your own designated username and password. It will then ask you for the path of the dataset. Copy paste the path of the dataset folder here. 

Once complete, the database can be interacted using **`CLI_main.py`**.


## Interacting with the database
To interact with the database, run **`CLI_main.py`**. You will have to use the same username and password as when you created the database. From there, you will get a menu that should look like the following: 

Autocommit: True  

Please select an option:  
1- Insert Data  
2- Delete Data  
3- Update Data  
4- Search Data  
5- Aggregate Function  
6- Sortings  
7- Joins  
8- Grouping  
9- Subqueries  
10- Transaction Control  
X- Exit  

From here you can choose an option, or exit by entering **X**.

### Inserting data
Entering **1** will give you the following menu:

Select a table to insert data into:  
1- Case  
2- Patient  
3- Date  
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose one of the tables, and enter the data based on the schema provided.


### Deleting data
Entering **2** will give you the following menu:

Select a table to delete data from:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose one of the tables, and enter the primary key of the data you want to delete based off of.

### Updating data
Entering **3** will give you the following menu:

Select a table to update data of:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose one of the tables, and enter the primary key of the data you want to update data based off of, and then the new data that should take its place.


### Searching data
Entering **4** will give you the following menu:

Select a table to search data from:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose one of the tables, and enter the condition that you would like to search the data based on. This will result in a table that shows all values that match the provided condition.


### Aggregate data
Entering **5** will give you the following menu:

Select a table to search data from:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose one of the tables, and enter the columns that you would like to aggregate the data based on. Then, enter the aggregate function. This will result in a table that shows the aggregate value of the column.


### Sort data
Entering **6** will give you the following menu:

Select a table to sort data of:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose one of the tables, and enter the columns that you would like to sort the data based on. Then, enter the sorting method. This will result in a table that shows a table of the data sorted based on the provided parameters.


### Join data
Entering **7** will give you the following menu:

Select the first table:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Choose the first table to join. Then choose to join the second table to join. Then, choose the joining conditions based on the tables chosen. This will result in a joined table. 


### Group data
Entering **8** will give you the following menu:

Select a table to group data from:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Select a table to group data from. Then select a column to view. Next, select a column to group by, and finally the aggregate function to group this column by. This will result in a table outlining the grouped column and the result of the aggregation of the second column.


### Subquery data
Entering **9** will give you the following menu:

Select the first table:  
1- Case  
2- Patient  
3- Date   
4- Weather  
5- Search Trends  
6- Region  
7- Policy  
X- Back to Menu  

Select the table for the query. Then select the column from the table to query the subquery off of. Next, select the table for the subquery. From here, select the condition to subquery off of. This will result in a table for all of the rows that match the given parameters. 


### Transaction Controls
Entering **10** will give you the following menu:

Enter one of the following for a transaction operation:     
T- Begin Transaction   
C- Commit  
R- Rollback  
X- Back to Menu  


Selecting **T** will turn **Auto Commit** off, allowing you to enter any of the data manipulation commands (**1-3**) or data selection commands (**4-9**) without updating to the database immediately. 

Selecting **C** will commit all of the data manipulation commands (**1-3**) that you have entered previously when **Auto Commit** is off, and will turn **Auto Commit** back on.

Selecting **R** will roll back all of the data manipulation commands (**1-3**) that you have entered previously when **Auto Commit** is off, and will turn **Auto Commit** back on. 