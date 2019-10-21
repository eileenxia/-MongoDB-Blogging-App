"""
******
* Syed Tanveer & Eileen
* Team 7
* CS61
******


"""
from connect import connect
import pymongo  # mongodb connector
import re
import shlex # to help split each line

def home_screen():

    collections = mongoConnect()
    print("Welcome! reading lines in file...")

    try:
        line = input()
    except EOFError:
        return

    if line == '':
        print("no file was given, press enter and rerun this program using the command `python3 lab3b.py < [filename]`")
        return

    while line != '':
        word = shlex.split(line)
        if  word[0] == 'post':
            add_post(collections, word[1], word[2], word[3], word[4], word[5], word[6])
        elif word[0] == 'comment':
            add_comment(collections, word[1], word[2], word[3], word[4], word[5])
        elif word[0] == 'delete':
            delete_post(collections, word[1], word[2], word[3], word[4])
        elif word[0] == 'show':
            show_posts(collections, word[1])
        elif word[0] == 'search':
            search_posts(collections, word[1], word[2])
        else:
            print("Found an error in the file! please look over the first word in every line to make sure they are proper queries. [ post, commment, delete, show, search]")
            break
        try:
            line = input()
        except EOFError:
            break

    print("cleaning up")
    collections[0].drop()
    collections[1].drop()
    print("connection closed! Goodbye")
    return

def mongoConnect():

    db = connect()

    server = "mongodb://" + str(db['user']) + ":" + str(db['password']) + "@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/" + str(db['database']) + "?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
    # server = "mongodb://localhost"

    try:  # initialize db connection
        connection = pymongo.MongoClient(server)

        print("Connection established.")

        # connection.server_info()  # force connection on a request as the
        # connect=True parameter of MongoClient seems
        # to be useless here
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Connection failure:")
        print(err)
    else:

        # get handle for team database
        db = connection.Team07DB

    print("connected to db")
    post_collection = db['Posts']
    comment_collection = db['Comments']

    return post_collection, comment_collection

def make_permalink(blogname, title):
    return str(blogname+'.'+re.sub('[^0-9a-zA-Z]+', '_', title))

def add_post(collections, blogName, userName, postTitle, postBody, postTags, postTimestamp):

    permalink = make_permalink(blogName, postTitle)

    # post blogName userName title postBody tags timestamp
    try:

        post = {"blogname": str(blogName),
                 "permalink": str(permalink),
                 "userName": str(userName),
                 "title": str(postTitle),
                 "body": str(postBody),
                 "tags": str(postTags),
                 "timestamp": str(postTimestamp)}

        collections[0].insert_one(post)

    except Exception as e:
        print("Error trying to read collection:", type(e), e)


def add_comment(collections, blogName, post_timestamp, username, comment_body, comment_timestamp):
    try:
        name_len = len(blogName)
        query = {"blogname": blogName, "timestamp": post_timestamp[int(name_len)+1:]}
        blog_doc = collections[0].find(query)
        if blog_doc == {}:
            print("The blog name might be spelled incorrectly or it might not exist! the following error was given")
            return
    except Exception as e:
        print("Error trying to read collection:", type(e), e)
        return
    else:
        permalink = blog_doc[0]['permalink']

 # comment blogname permalink userName commentBody timestamp
    try:
        post = {"blogname": str(blogName),
                 "permalink": str(permalink),
                 "userName": str(username),
                 "commentBody": str(comment_body),
                 "timestamp": str(comment_timestamp)}

        collections[1].insert_one(post)
    except Exception as e:
        print("Error trying to read collection:", type(e), e)

    return


def delete_post(collections, blogName, post_timestamp, userName, delete_timestamp):

    name_len = len(blogName)
    myquery = {"blogname": blogName, "timestamp": post_timestamp[int(name_len)+1:]}

    blog_exists = collections[0].find_one(myquery)

    if blog_exists == {}:
        print("This blog does not exist")
        return

    newvalues = {"$set": {"body": "Blog deleted by {} at {}".format(userName, delete_timestamp)}}

    collections[0].update_many(myquery, newvalues)
    collections[1].update_many(myquery, newvalues)

    return

def show_posts(collections, blogName):

    myquery = {"blogname": blogName}
    posts = collections[0].find(myquery)
    comments = collections[1].find(myquery)
    prev_post = posts[0]['blogname']
    print("\n-- showing content in {} --\n".format(prev_post))
    for post in posts:
        if prev_post != post['blogname']:
            print("in {}\n".format(post['blogname']))
            prev_post = post['blogname']
        print(' username : {}\n'
              ' tags: {}\n'
              ' timestamp: {}\n'
              ' permalink: {}\n'
              ' body: {}\n'
        " -------------\n".format(post['userName'], post['tags'], post['timestamp'], post['permalink'], post['body']))
        for comment in comments:
            if comment['permalink'] == post['permalink']:
                print("    username : {}\n"
                      "    permalink: {}\n"
                      "    commentBody: {}\n"
                      "    -------------\n".format(comment['blogname'],post['permalink'],
                                               comment['commentBody']))

    return

def search_posts(collections, blogName, searchString):

    myquery = {"blogname": blogName}
    posts = collections[0].find(myquery)
    comments = collections[1].find(myquery)
    already_printed = True
    print("\n -- beginning search query in {} for: {} -- \n".format(blogName, searchString))
    for post in posts:
        for comment in comments:
            if searchString in post['body'] and already_printed == True:
                print(' username : {}\n'
                      ' tags: {}\n'
                      ' timestamp: {}\n'
                      ' permalink: {}\n'
                      ' body: {}\n'
                      " -------------\n".format(post['userName'], post['tags'], post['timestamp'], post['permalink'],
                                                post['body']))
            elif already_printed == True:
                print(' username : {}\n'
                      ' tags: {}\n'
                      ' timestamp: {}\n'
                      ' permalink: {}\n'
                      ' body: {}\n'
                      " -------------\n".format(post['userName'], post['tags'], post['timestamp'], post['permalink'],
                                                post['body']))
            already_printed = False
            if searchString in comment['commentBody']:
                if searchString in comment['commentBody']:
                    print("    username : {}\n"
                          "    permalink: {}\n"
                          "    commentBody: {}\n"
                          "    -------------\n".format(comment['blogname'], post['permalink'],
                                                       comment['commentBody']))

    return

home_screen()