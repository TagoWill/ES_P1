from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Base, Car, Dealership



# print a nice greeting.
def say_hello(username="World"):
    return '<p>Hello %s!</p>\n' % username

def name():
    engine = create_engine('sqlite:///C:\\Users\\Faculudade2015-2016\\ES_P1\\project1_sqlalchemy_db.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Make a query to find all Users in the database
    session.query(User).all()

    # Return the first User from all Users in the database
    user = session.query(User).first()
    return '<p>Hello my hero %s!</p>\n' % user.name

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

application.add_url_rule('/name/', 'name', (lambda:
    header_text + name() + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()