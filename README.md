# labShare

Lab 8 Team D - WAD2 Team Project - LabShare - A platform to share the labs you are enrolled in with your friends. :)

## Dependencies

{what :: version :: command :: where}

* django :: 1.11.7 :: 'pip install django==1.11.7' :: VE
* pillow :: latest :: 'pip install pillow' :: VE
* django-registration-redux :: latest :: 'pip install django-registration-redux' :: VE
* python :: 3.5+ :: see python website :: anywhere

## Set up

Once you have all the dependencies installed in a virtual env then run these commands in your VE

* 'python manage.py makemigrations'
* 'python manage.py makemigrations appLabShare' if in the previous command you did not see 'appLabShare'
* 'python manage.py migrate' to set up the database
* 'python populate.py' to populate the database with useful example data
* 'python manage.py runserver' to run the website and try it out, have fun!

## Issues

* Main menu bar, when pressed, removes the nav bar once removed from screen frame
* Details on friends list card is bigger than image
* Profile social CSS has disappeared
* Registration page bullet points
* CSS for enrol page
* Enrol page doesn't display correct error message if the level doesn't exist (views.py)
* Dynamic folders for lab posts
