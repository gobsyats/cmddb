You are to build a data structure for storing integers. You will not persist the database to disk, you will store the data in memory.

For simplicity's sake, instead of dealing with multiple clients and communicating over the network, your program will receive commands via stdin, and should write appropriate responses to stdout. Each line of the input will be a command (specified below) followed by a specific number of arguments depending on the command.

For example:

COMMAND a b
COMMAND2 c
END
Your database should accept the following commands.

SET name value

Set the variable name to the value value. Neither variable names nor values will contain spaces.

GET name

Print out the value of the variable name, or NULL if that variable is not set.

UNSET name

Unset the variable name, making it just like that variable was never set.

NUMWITHVALUE value

Print out the number of variables that are currently set to value. If no variables equal that value, print 0.

END

Exit the program. Your program will always receive this as its last command.

Once your database accepts the above commands and is tested and works, implement commands below.

BEGIN

Open a new transaction block. Transaction blocks can be nested (BEGIN can be issued inside of an existing block) but you should get non-nested transactions working first before starting on nested. A GET within a transaction returns the latest value by any command. Any data command that is run outside of a transaction block should commit immediately.

ROLLBACK

Undo all of the commands issued in the most recent transaction block, and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.

COMMIT

Close all open transaction blocks, permanently applying the changes made in them. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.

Your output should contain the output of the GET and NUMWITHVALUE commands. GET will print out the value of the specified key, or NULL. NUMWITHVALUE will return the number of keys which have the specified value.

Sample Input
SET ex 10
GET ex
UNSET ex
GET ex
END
Sample Output
10
NULL