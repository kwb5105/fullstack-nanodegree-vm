# Instructions for Linux Server Configuration

Setup up Linux server for the sixth project for the Udacity Full Stack Nano Degree

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

EC Host Name: http://ec2-18-188-132-132.us-east-2.compute.amazonaws.com/

Host Name: http://18.188.132.132/

IP Address: 18.188.132.132

## google OAuth instructions

```
1. Go to [Google Devloper Console](https://console.developers.google.com/)
2. Sign in or Sign up if prompted
3. Go to Credentials
4. Click Create Crednetials then OAuth client ID
5. Select Web Application and click create
6. Enter name Item catalog app
7. Under Authorized JavaScrip Origins enter http://ec2-18-219-95-16.us-east-2.compute.amazonaws.com
8. Under Authorized redirect URIs enter http://ec2-18-188-132-132.us-east-2.compute.amazonaws.com 
and http://ec2-18-188-132-132.us-east-2.compute.amazonaws.com/gconnect
10. Click Create
11. Copy the Client ID and paste it into the data-clientID in login.html
12. Copy App Security at the bottom of the application.py after app.secret_key =
13. Under OAuth 2.0 Client IDs click download JSON
14. Rename JSON file to client_secrets.json and place file in /vagrant/catalog
```
## log into server
```
1. Change director to where pem file is saved
2. open up terminal (git hub for windows users)
3. $ ssh -i PrivateKey.pem -p 2200 grader@18.188.132.132
```

## walkthrough of Amazon Webservice and server configuration changes

```
1. Setuping up LightSail server
    * [Amazon LightSail](https://lightsail.aws.amazon.com)
    * Sign in or Sign up if prompted
    * Click Create an instance
    * Go to OS only and click ubantu
    * Pick instance plan
    * Give instance a hostname and click connect ssh
    * Networking tab under firewall add UDP 123 and TCP 2200
    * Download .pem public key file
    
2. Set up the server by downloading all needed files for application to run
    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo do-release-upgrade
    $ sudo apt-get install finger
    $ sudo apt-get install apache2
    $ sudo apt-get install postgresql
    $ sudo apt-get install libapache2-mod-wsgi
    $ sudo apt autoremove
    $ sudo apt-get install git
    $ sudo apt-get install python-pip
    $ sudo pip install Flask
    $ sudo pip install --upgrade pip
    $ sudo pip install --upgrade google-api-python-client
    $ sudo pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
    $ sudo pip install --upgrade flask
    $ sudo pip install --upgrade requests
    $ sudo pip install sqlalchemy
    $ sudo apt install upstart
    $ sudo apt-get install postgresql postgresql-contrib
    $ sudo pip install --upgrade pip
    $ sudo pip install virtualenv
    $ sudo apt-get install python3-venv
    $ sudo apt-get install libpq-dev python-dev
    $ sudo apt install unattended-upgrades
    $ sudo dpkg-reconfigure --priority=low unattended-upgrades
    $ sudo apt-get dist-upgrade
    
3. Set up the firewall and security settings
    $ sudo nano /etc/ssh/sshd_config 
    change port from 22 to 2200 
    set PermitRootLogin from prohibit-password to No
    $ sudo nano /etc/init.d/sshd restart
    $ sudo ufw allow 2200/tcp
    $ sudo ufw allow 80/tcp
    $ sudo ufw allow 123/udp
    $ sudo ufw default deny incoming
    $ sudo ufw default allow outgoing
    $ sudo ufw allow ntp
    $ sudo ufw added
    $ sudo ufw enable
    $ sudo ufw status
    
4. Set up the time zone
    $ sudo dpkg-reconfigure tzdata (configure time zone)
    $ sudo reboot
    
5. Setting up ssh to the amazon server
    Launch a Unix/Linux like terminal (e.g. Git Bash for Windows, Terminal for Mac)
    $ mkdir .ssh
    Put the pem file in the .ssh directory, in this case it's named PrivateKey.pem
    $ ssh -i PrivateKey.pem -p 2200 ubuntu@18.188.132.132
    
6. Set up the user grader and give admin privs (password not shown)
    $ sudo su -
    $ sudo adduser grader
    $ sudo visudo
    $ append grader	ALL=(ALL:ALL) 
    Create a new file in the sudoers directory: 
    $ sudo nano /etc/sudoers.d/grader. 
    Give grader the super permisssion grader ALL=(ALL:ALL) ALL
    set up authorized key
    $ sudo chown grader:grader /home/grader/.ssh
    $ sudo chmod 700 /home/grader/.ssh
    $ sudo cp /root/.ssh/authorized_keys /home/grader/.ssh/
    $ sudo chown grader:grader /home/grader/.ssh/authorized_keys
    $ sudo chmod 644 /home/grader/.ssh/authorized_keys
    remove everything before ssh-rsa so grader isn't stopped like root
    $ sudo nano /home/grader/.ssh/authorized_keys
    $ su - grader
    $ mkdir .ssh
    
7. Set up the database
    $ sudo -u postgres createuser -P catalog
    $ sudo -u postgres createdb -O catalog catalog
    $ sudo -u postgres -i
    $ psql
    # \c catalog
    # REVOKE ALL ON SCHEMA public FROM public;
    # GRANT ALL ON SCHEMA public TO catalog;

8. Review all the privs for the database
    # \du
    #\q
    $ exit
    $ cd /var/www
    $ sudo mkdir catalog
    $ sudo chown -R grader:grader catalog
    $ cd catalog
    $ git clone https://github.com/bad2thuhbone/Catalog catalog
    $ cd catalog
    $ sudo a2enmod wsgi
    $ sudo service apache2 start
    $ sudo service apache2 restart
    $ mv application.py __init.py__

9. Change the database engine sqlite has permissions issues and its easier to use postgres
   change sqlite engine to postgresql (was running into permission issues with sqlite, took me weeks to figure out) 
   engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
   $ sudo nano database_setup.py
   $ sudo nano categories_setup.py
   $ sudo nano __init__.py
    
10. Install virtual environment
    $ sudo virtualenv venv
    $ source venv/bin/activate
    $ python3 -m venv env
    $ sudo chmod -R 777 venv
    $ sudo pip install Flask
    $ sudo pip install bleach httplib2 request oauth2client sqlalchemy
    $ pip install psycopg2
    $ sudo python database_setup.py
    $ sudo python categories_setup.py
    $ sudo a2ensite catalog
    
11. Use the nano __init__.py command to change the client_secrets.json line 
    to /var/www/catalog/catalog/client_secrets.json as follows 
    CLIENT_ID = json.loads( open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id'] 
    Ensure to look through __ini__.py for every instance of this change and replace as stated. 
    Also replace if __name__ == '__main__': app.secret_key = 'your_secret_key' app.debug = True app.run(0.0.0.0, port=5000 
    with if __name__ == '__main__': app.secret_key = 'your_secret_key' app.debug = True app.run()
    
12. Create catalog.wsgi file
    $ sudo nano /var/www/catalog/catalog.wsgi
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0, "/var/www/catalog/")

    from catalog import app as application
    application.secret_key = 'your_secret_key'
    
13. Configure and enable virtual host
    $ sudo nano /etc/apache2/sites-available/catalog.conf
   <VirtualHost *:80>
         ServerName 18.188.132.132
         ServerAdmin admin@18.188.132.132
         WSGIScriptAlias / /var/www/catalog/catalog.wsgi
         <Directory /var/www/catalog/catalog/>
            Order allow,deny
            Allow from all
         </Directory>
         Alias /static /var/www/catalog/catalog/static
         <Directory /var/www/catalog/catalog/static/>
            Order allow,deny
            Allow from all
         </Directory>
         ErrorLog ${APACHE_LOG_DIR}/error.log
         LogLevel warn
         CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
    $ sudo service apache2 restart

```

## Built With
* [Python 2.7.13](https://www.python.org/downloads/)
* [Git-2.14.2.2 64 bit](git-scm.com)
* [Vagrant 2.0.1](https://www.vagrantup.com/downloads.html)
* [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
* [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm)
* [VirtualBox](https://www.virtualbox.org/)
* [Google Devloper Console](https://console.developers.google.com/)
* [Amazon lightsail] (https://lightsail.aws.amazon.com)

## Author
* **Angela Carpio** - *Initial work*

## Acknowledgments
* FullStack-nanodegree-vm from Udacity was used in creating this project
* [Udacity OAuth2.0 OAuth](https://github.com/udacity/OAuth2.0) images and design layout was used
* [philoniare](https://github.com/philoniare/Item-Catalog) used templates as I liked the collapsable edit and delete style
* [Udacity Lesson 2](https://github.com/udacity/ud330/blob/master/Lesson2/step5/project.py) used google authentication code
* [Oauth 2.0 Installation](https://developers.google.com/api-client-library/python/auth/web-app)
* [Google Sign-in](https://developers.google.com/identity/sign-in/web/)
* [Mohllal](https://github.com/Mohllal/udacity-fsnd/tree/master/p7-linux-server-configuration)
* [judekuti](https://github.com/judekuti/Linux-Configuration)
* [Amazon ssh Windows](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-windows.html)
* [SteveWooding](https://github.com/SteveWooding/fullstack-nanodegree-linux-server-config)
* [Kundan Singh](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps) How To Deploy a Flask Application on an Ubuntu VPS
* [sqlite error](http://fredericiana.com/2014/11/29/sqlite-error-open-database-file/)


Using this as a placeholder for setting up Linux machine
