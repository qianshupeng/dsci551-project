# ChatDB: Learning to Query Database Systems on MySQL

DSCI 551 Semester Project

Qianshu Peng (ChatDB 87 Group)

This is the documentation of ChatDB, a Python-based CLI project for interaction with MySQL database. Please find the instructions of running this project below.

## Execute ChatDB

Before executing, please make sure you have these modules installed in your environment:
- pandas
- pymysql
- nltk

Also, you need to have MySQL server on your computer to connect to ChatDB. It's recommended to use Python 3.6, and other versions of Python are possible to cause error or incorrect results. 

In your terminal, enter: <br>
<code>python main.py</code> <br>
If <code>python</code> does not work for you, try <code>python3</code> or other commands corresponding to your python version.

If this is your first time of executing ChatDB, enter your MySQL host, username, and password to connect to local MySQL server; otherwise, the configurations will be loaded automatically. Also, the nltk package will download the resources it needs. 

Then you will enter the ChatDB interface. Follow the instructions on the interface to continue. If you get any error message, please check if your environment fulfills all requirements above. 

Notice: if you have run the ChatDB, you may get several error messages like <code>Error creating table or inserting data: (1050, "Table already exists")</code>. That's because built-in database has been created when you executed it previously. This will not affect use, and you can simply **ignore them**. 

<br>
<br>

## Sample Queries
Follow the instructions on ChatDB interface to generate sample queries. After you select a table, you will be able to select the "Generate Sample Queries" option.

When you select this, ChatDB will ask you to select a certain keyword to generate queries with that keyword (select from group by/having/where/order by/sum/count/join); if you don't want to choose a keyword, simply press enter to generate queries randomly. 
<br>(Notice: If a table has no foreign key, you will not be able to generate JOIN queries, although it may be referenced by other table. It is recommended to check the table descriptions before exploring queries.)

After generating queries, you can type the index to execute corresponding query. Each query comes with a several-word description for its functionality. 

Not all sample queries can be meaningful. Some of them may look stupid, for example, summing up the IDs (since they are numbers). ChatDB will give you a number of sample queries, and you can select from them wisely. 

<br>
<br>

## Natural Language Prompts

Your prompts should follow certain patterns to be caught by ChatDB. Following are examples for each type of supported queries. Output query will be executed and return query results. 

Suppose we are in built-in table `transactions` for the examples. 

### JOIN
Input: transactions.product_id **join** products.product_id 
<br>OR<br>
product_id in transactions **join** product_id in products

Output: SELECT * FROM \`transactions\` JOIN \`products\` ON \`transactions\`.\`product_id\` = \`products\`.\`product_id\`; 

Notice: entering columns without reference relationship might not cause error, but this will not give any query results. 

### GROUP BY
Input: total/sum/average/count/max/largest/min/smallest transaction_id **by** transaction_date

Output: SELECT \`transaction_date\`, SUM/AVG/COUNT/MAX/MIN(\`transaction_id\`) FROM \`transactions\` GROUP BY \`transaction_date\`;

### WHERE

Note: "..." in the inputs below means you can add any words here, like select/get/etc. 

#### COUNT with WHERE
Different to COUNT with GROUP BY.

Input: **count** transaction_id **where** store_id >/(other operators) 3

Output: SELECT COUNT(\`transaction_id\`) FROM \`transactions\` WHERE \`store_id\` > 3;

#### WHERE with BETWEEN
Input: ... **where** transaction_id **between** 20 **and** 30
<br>OR<br>
**where** transaction_id **from** 20 **to** 30

Output: SELECT * FROM \`transactions\` WHERE \`transaction_id\` BETWEEN 20 AND 30;

#### WHERE with LIKE
Note: this example is based on table `products`, as table `transactions` does not contain any text-type data.

Input: ... **where** product_type **like** "tea"

Output: SELECT * FROM \`products\` WHERE \`product_type\` LIKE '%tea%';

#### Common WHERE
Input: ... **where** transaction_qty <=/>=/</>/= 3

Output: SELECT * FROM \`transactions\` WHERE \`transaction_qty\` <=/>=/</>/= 3;

### Common Query
You can select any columns you want. 

Input: **get/retrieve/output/return** transaction_id, transaction_qty, product_id

Output: SELECT \`transaction_id\`, \`transaction_qty\`, \`product_id\` FROM \`transactions\`;

If nothing is printed after you entering the prompt, check your words and make sure you've followed the patterns above. 

<br>
<br>

## Upload Your Data

After selecting "Upload Your Database", ChatDB will ask you to enter the name of your database. Please enter an English word. 

IMPORTANT: Then you need to enter the name of CSV files. Please enter the tables with referenced columns first, and then ones with columns referencing other tables. Please enter their relative pathes. The name of CSV files will become corresponding table names. <br>
For example: <br>
We have table `enrollments` and `students` from "../data/enrollments.csv" and "../data/students.csv", `enrollments.student_id` references to `students.id`. The input text should look like: "../data/students.csv, ../data/enrollments.csv".

Then you need to enter primary key, foreign key, and data types for each table. All inputs will be either comma-separated text or `None`. <br>
Notice:
- You MUST enter ONE column as primary key. Column combinations are not accepted. 
- If you enter `None` for data types, ChatDB will infer the data type automatically. 

If you make mistake on the inputs (such as entered a wrong name for primary key), you may get error message, or the table is not created successfully. Try again for uploading data in this case. 

After creating the database, you can explore it and execute queries as in built-in database. Please follow the instructions above. 

<br>
<br>

