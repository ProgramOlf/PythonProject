HOLZBAU AG
DBMS

To be able to run the code: - run python version 3.12.0 64bit
                            - install flask and pandas
                            - keep in mind, to use the absolute paths to your csv files, else the flask application
                              won't be able to find them

Currently the web application starts by showing the user the homepage. There he finds a navigation bar leading him to the customer data and order data.
On the order data (customer data) pages, they can see the data of the corresponding csv file displayed as a table.
Beside each row there is an Action button to chose which row should be edited. After selecting ONE row, there is a button to be clicked which leads to a mask where every cell can be changed of the selected row.
For now you can only select one row at a time.
Also I could not figure out how to display the selected row in the mask, to make the editing process easier.
