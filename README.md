# MongoDB Blogging App
### Eileen Xia and Syed Tanveer

Make sure to have pymongo installed. Run these commands:
`brew install pymongo`

To run this program, run `cat  testfile1.in  | python3 main.py > test.stdout 2> test.stderr`.

We used our own test file to verify correct operation.
These have input and expected output files included.

#### File Description

##### main.py

`home_screen()` is the main screen where the user specifies whether they want to add a post, add a comment to an existing post, delete a post, show a post, or search for a post.
`add_post()` allows the user to add a post and it's info like blog title, body, and optional tags, where tags is an array.
`add_comment()` allows the user to add a comment to a specified blog. The permalink updates to the current timestamp when a comment is added.
In `delete_post()` the post or comment matching that permalink is replaced with a standard post saying “deleted by {userName}".
`show_posts()` shows the posts as specified.
`search_posts()` searches for a post given a string that is found in the post body, tags, or comment.

#### connect.py
`connect.py` is used to help us connect to our mongo database.

#### python_mongodb_dbconfig.py
Reads the database configuration file and returns a dictionary object.

#### config.ini
Holds all of the information for accessing the Team 7 mongo database (Atlas login and password).
