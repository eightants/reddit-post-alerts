# Reddit Post Alerts

This project uses the Discord and Reddit bot APIs to find new posts in subreddits matching your keywords and notifying you via Discord. The program is developed in Python and hosted on Heroku. I will give an overview on how the bot was created and a guide to use the code to customize and host your own version of this bot!

## Setting up the bots

There are four components that make up this bot: the Python scripts, the Reddit app, the Discord app, and Heroku for hosting. The Python scripts are all provided in this repository and changing the subreddit and keyword variables will provide the customization. The other parts of this project need to be set up by the user. 

To ensure that the bot can watch for new posts on the subreddits specified, we need a Reddit bot. Visit [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/) and select Create App. The app will be a script, name it anything you want and set the redirect uri to a default `http://127.0.0.1`. 

The Reddit bot has been created, and now we should set up our Discord bot. Head to [http://discordapp.com/developers/applications](http://discordapp.com/developers/applications) and login to your Discord account. Select New Application and give your app a name. Now, navigate to the Bot tab on the left, and select Add Bot. 

You have set up your Discord bot, now you'll want to add it to one of your servers, so it's able to notify you and your members of the Reddit posts. To do so, visit the OAuth2 tab on the Developer portal. Select `bot` from the Scopes section and select the permissions you'd like your bot to have. Messaging permissions are sufficient. Copy the URL generated and paste it into a browser, then select the server you'd like your bot to join. Go onto Discord and check the server, your bot should be added. 

Your Discord bot should post their messages in a specific channel on your server for easy access. Choose a channel you'd like the bot to post in, then copy the channel ID and change `bot.py`. [Guide to finding channel ID](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
```
# change this at the top of bot.py, replace with your channel id
channelid = 1234567890123456 
```


## Setting up Heroku

Now, to set up the service that hosts your bots. Make sure git is installed, then [install Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). Verify that you installed it with `$ heroku --version`. 

Make an account on [Heroku](https://www.heroku.com/) then login to Heroku on your terminal. 
```
$ heroku login
Enter your Heroku credentials.
Email: anthony@example.com
Password (typing will be hidden):
Authentication successful.
```
Now initialize a local git repository for the project, if it has not been initialized yet. 
```
Initializing a local git repository

# Change your directory to your base directory
$ cd directory/to/repo
$ git init
Initialized empty Git repository in .git/
$ git add .
$ git commit -m "My first commit"
Created initial commit 5df2d09: My first commit
44 files changed, 8393 insertions(+), 0 deletions(-)
create mode 100644 README
create mode 100644 Procfile
create mode 100644 app/controllers/source_file
  ...
```

## Creating a Remote Heroku
### For a new Heroku App

The heroku create CLI command creates a new empty application on Heroku, along with an associated empty Git repository. If you run this command from your app’s root directory, the empty Heroku Git repository is automatically set as a remote for your local repository.
```
$ heroku create
Creating app... done, ⬢ thawing-inlet-61413
https://thawing-inlet-61413.herokuapp.com/ | https://git.heroku.com/thawing-inlet-61413.git
```
You can use the git remote command to confirm that a remote named heroku has been set for your app:
```
$ git remote -v
heroku  https://git.heroku.com/thawing-inlet-61413.git (fetch)
heroku  https://git.heroku.com/thawing-inlet-61413.git (push)
```
### For an existing Heroku App

If you have already created your Heroku app, you can easily add a remote to your local repository with the heroku git:remote command. All you need is your Heroku app’s name:
```
$ heroku git:remote -a thawing-inlet-61413
set git remote heroku to https://git.heroku.com/thawing-inlet-61413.git
```
### Changing your App name on Heroku

You can rename an app at any time with the heroku apps:rename command. For example, to rename an app named “oldname” to “newname”, run the heroku apps:rename command from your app’s Git repository:
```
$ heroku apps:rename newname
Renaming oldname to newname... done
http://newname.herokuapp.com/ | git@herokuapp.com:newname.git
Git remote heroku updated
```
You can also rename an app from outside of its associated Git repository by including the --app option in the command:
```
$ heroku apps:rename newname --app oldname
http://newname.herokuapp.com/ | git@herokuapp.com:newname.git
```

## Setting environment variables on Heroku

The authentication keys for your bots should be kept secret from the public. To do this, you should set up environment variables in Heroku that the code will then grab from. In the Python code, the environment variables are obtained with this code. 
```
RedditScrape.py
username = os.environ['BOTONE_USERNAME']
password = os.environ['BOTONE_PASSWORD']
client_id = os.environ['BOTONE_ID']
client_secret = os.environ['BOTONE_SECRET']
user_agent = os.environ['BOTONE_AGENT']
---
bot.py
token = os.environ['DISCORDBOT_TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']
```

To set environment variables, use the code below. If you use a different variable name for your environment variables, be sure to change that in the Python code too. The `BOTONE_ID` is the code right below the name of your Reddit bot, under 'personal use script'. `BOTONE_SECRET` is the bot secret, both are found on the Reddit [bot page](https://www.reddit.com/prefs/apps/). `BOTONE_AGENT` is the name you want to give this release of the bot, e.g. `reddit-post-alerts-v1`

The token for your Discord bot can be found on the Developer Portal on the Bots page for your bot.
```
# Set heroku config/env variables
$ heroku config:set BOTONE_USERNAME=<your_reddit_username>
$ heroku config:set BOTONE_PASSWORD=<your_reddit_password>
$ heroku config:set BOTONE_ID=<your_bot_id>
$ heroku config:set BOTONE_SECRET=<your_bot_secret>
$ heroku config:set BOTONE_AGENT=<name_of_app>
$ heroku config:set DISCORDBOT_TOKEN=<your_discord_bot_token>

# Confirm they're set with this command
$ heroku config
```
## Setting up the database

Since this script will check every 5 minutes, we want to make sure it doesn't notify us of the same post twice. For this, we need a way to store the `post_id` of each post we have already been notified of. We will be using PostgreSQL as it is free and integrated with Heroku. Start by [installing Postgres](https://www.postgresql.org/download/) on your local machine. 

Then, add Postgres to your Heroku app by logging onto the Heroku website. 
`Log in to Heroku > Heroku dashboard > Choose your app > Resources > Add-ons > Select Heroku Postgres > Click on Provision`

After adding it, check information about Postgres with the below command. 
```
$ heroku pg:info
=== DATABASE_URL
Plan:                  Hobby-dev
Status:                Available
Connections:           2/20
PG Version:            10.6
Created:               2019-10-09 20:22 UTC
Data Size:             7.8 MB
Tables:                0
Rows:                  0/10000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-clear-32269
```

Start a psql session with the remote database with `heroku pg:psql`
```
$ heroku pg:psql
--> Connecting to postgresql-clear-32269
psql (10.6 (Ubuntu 10.6-1.pgdg16.04+1))
SSL connection (protocol: TLSv1.2, cipher: DHE-RSA-AES256-SHA, bits: 256, compression: off)
Type "help" for help.

reddit-post-alerts::DATABASE=> 
```

In the session, [create a table](http://www.postgresqltutorial.com/postgresql-create-table/) for the database that the script will pull from. As you can see from `bot.py` we are checking and inserting into a table named `redditpostalerts` and a column named `post_id`.
```
CREATE TABLE redditpostalerts (post_id TYPE UNIQUE);
```

Verify that it has been created with `heroku pg:info`, the number of tables should be 1. You can pull and push to and from a database on your local machine and many other operations you can find [here](https://devcenter.heroku.com/articles/heroku-postgresql).

## Deploying your app

Since you have committed the files on your local repo, check that in `Procfile` contains `worker: python post-alert-bot/bot.py`. Then deploy your app by pushing to Heroku. 
```
$ git push heroku master
Initializing repository, done.
updating 'refs/heads/master'
  ...
```

Your bot should be up and running! The free Dynos provided by Heroku will be enough to keep one app up 24/7, so it will always be up. Modify the subreddits and keywords checked at the top of `bot.py`. You can check as many subs and keywords as you like. 
```
subs = ['askreddit', 'sub2']
keywords = [['keyword1 for askreddit', 'keyword2 for askreddit'], ['kw1 for sub2', 'kw2 for sub2']]
```

