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
- Include certs in template/ssh will be placed in users .ssh directory & added to ssh-agent
