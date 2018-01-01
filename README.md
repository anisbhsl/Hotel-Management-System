# Hotel-Management-System
**Hotel Management System** is under development. The software project contributors are required to install the dependencies as follows:
```shell
sudo pip install -r requirements.txt
```
* Clone using SSH key for your own good.
  * You can refer to this [link](https://help.github.com/articles/connecting-to-github-with-ssh/) connecting to Github with SSH keys so that you don't need username and password everytime you perform push or pull request.
  * Otherwise use HTTPS but you will need password everytime.
* Execute the followings: 
```shell
python3 manage.py migrate
```
Then,
```shell
python3 manage.py runserver
```
* This will work if correctly set up.
## For more information, visit [Django Documentation](https://docs.djangoproject.com/en/2.0/).

*You are supposed to be using linux environment with **Python 3**. Everything else is simple. The packages mentioned in requirements files are required for deployment especially in heroku.*
