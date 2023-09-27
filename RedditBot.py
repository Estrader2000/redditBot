import praw 
import config 
import time
import os
import requests

def bot_login(): 
    print("Logging in...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Quote Bot v0.1")
    print("Logged in!")
    
    return r

def run_bot(r, comments_replied_to):
    print("Obtaining comments")

    for comment in r.subreddit('quotesporn').comments(limit=25):                                            #Subreddit
        if "quote" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
            print("String \"quote\" Found" + comment.id)

            quote_request = requests.get("https://zenquotes.io/api/random").json()                          #API Request
            quote = quote_request[0]['q']
            quote_author = quote_request[0]['a']

            comment.reply("Did someone say quote? Here's a great quote by " + quote_author + ": " + quote)

            print("Quote: " + quote)
            print("Quote Athor: " + quote_author)
            print("Replied to comment" + comment.id)

            comments_replied_to.append(comment.id)

            with open ("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
    
    # 30 second intervals 
    print("Sleeping for 30 seconds...")         
    time.sleep(30)

def get_saved_comments():                                                                 # Keep track of comments  replied to
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else: 
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))


    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
    run_bot(r, comments_replied_to)

