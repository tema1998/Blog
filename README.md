# Blog Django application
It is a blog application

Functions |
-- |
`Follow/unfollow people` |
`Share photos with your friends` |
`Edit/delete posts` |
`View friends posts` |
`Like posts` |
`Write comments` |
`Like comments` |
`Turn off/on comments` |
`Add posts to favorites` |
`Chat with friends` |

Functions 'Follow/unfollow', 'Like/dislike', 'Add posts to favorites' implemented using **JS**(*without page refresh*). \
\
Chat(*in real time*) application implemented using **Channels**


## URL
[http://tema98.pythonanywhere.com/](http://tema98.pythonanywhere.com/)

## Installation on linux
First of all - clone repository.
Then create virtual environment:
```
python3 -m venv venv
```
Activate virtual environment:
```
source venv/bin/activate
```
Install all the required dependencies by running
```
pip install -r requirements.txt
```

Install Tailwind CSS dependencies, by running the following command:
```
python manage.py tailwind install
```

Migrate:
```
python manage.py makemigrations
```

Then start up Django's development server.
```
python manage.py runserver
```
