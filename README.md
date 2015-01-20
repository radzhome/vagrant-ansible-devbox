# vagrant-ansible-devbox
Setup a devbox environment using vagrant and ansible on Virtualbox


Installs Ubuntu devbox with the following
* nginx
* postgresql 
* postgis
* python development environment
* pip: fabric, Pillow, gunicorn
* nodejs
* git

# usage

- Edit the vagrant file to use 64-bit ubuntu, 32-bit is default
- Include all required private keys in your ~/.ssh folder starting with the name id_rsa
- Include shared projects in ~/projects
- Run: vagrant ssh 
- You may start django server using: manage.py runserver 0.0.0.0:8000  and access it at localhost:9000 on your host machine.
