# vagrant-ansible-devbox
Setup a devbox environment using vagrant and ansible on Virtualbox


Installs Ubuntu devbox with the following

* postgresql / postgis
* python development environment / pip
* pip: fabric, Pillow, gunicorn, fogbugz, jira & dependencies
* nodejs / npm
* git
* exim
* subversion
* imaging support
* npm: grunt, grunt-cli, grunt-init

# setup on linux / mac

1) Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)

2) Install pip and Ansible (You need Xcode for this on the Mac, see App Store):
     
     sudo easy_install pip
     sudo pip install ansible

3) Install [Vagrant](https://www.vagrantup.com/downloads.html)

4) Download this repository. i.e.:

    cd ~
    git clone https://github.com/radlws/vagrant-ansible-devbox.git
    cd vagrant-ansible-devbox

5) Edit the Vagrantfile to use 64-bit ubuntu, 32-bit is default. i.e.

    config.vm.box = "ubuntu/trusty32"
    # or
    config.vm.box = "ubuntu/trusty64"

Update other options if necessary, i.e. nfs for synced_folders or change memory or cpu amounts.

6) Update the playbook.yml vars for git_username and git_email used for bitbucket auth.

7) Include all required private keys in your ~/.ssh host folder, the ones starting with the name id_rsa will be copied over. Keys to consider are for access to AWS, Bitbucket, Trapsshman / project server access.

8) Include shared projects in ~/projects, make the directory it it doesn't exist. Can be empty to start. The same directory will be synced on the guest dev box.

9) Run: `vagrant up` , when done run `vagrant ssh` to get on.  Run `vagrant provision` to update any provision changes. Run `vagrant suspend` to shut down the box. 

10) Browse a project. You may start django server using: `manage.py runserver 0.0.0.0:8000` and access it at `localhost:9000` on your host machine. Optionally, run `gunicorn wsgi:application` to start your app.

# setup on windows / other

1) Install and provision your VM with ubuntu 14.04 either using Vagrant or manually. See Steps 1 & 2 from linux/ mac install.

Essentially you just need to comment out the following in the Vagrantfile to provision Ubuntu using Vagrant:

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.host_key_checking = false
      ansible.extra_vars = { ansible_ssh_user: 'vagrant',
              ansible_connection: 'ssh',
              ansible_ssh_args: '-o ForwardAgent=yes'}
    end

2) Once complete, SSH into your instance & install ansible


    vagrant ssh
    sudo pip install ansible


3) Install sshpass to be able to log in using password

    sudo apt-get install sshpass

4) Run the playbook locally

    ansible-playbook -i inventory/local playbook.yml  -vvvv
