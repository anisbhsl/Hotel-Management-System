# Hotel-Management-System
**Hotel Management System** is under development. 
* Clone using SSH key for your own good.
  * You can refer to this [link](https://help.github.com/articles/connecting-to-github-with-ssh/) connecting to Github with SSH keys so that you don't need username and password everytime you perform push or pull request.
  * Otherwise use HTTPS but you will need password everytime.
### The software project contributors are required to install the dependencies as follows:
1. If you want to install system wide:
```shell
sudo pip install -r requirements.txt
```
2. If you want to use `virtualenv`:
* Create a virtual environment as (you can use any name of the environment as you like):
```shell
virtualenv -p python3 hms-virtual-env
```
* Then execute this:
```shell
source hms-virtual-env/bin/activate
```
* The install requirements as:
```shell
pip install -r requirements.txt
```
__Note:__ To deactivate `virtualenv`, execute 
```shell 
deactivate
```
### Finally:
* Go to Hotel-Management-System folder that you cloned before.
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
