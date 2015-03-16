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

5) Edit the Vagrantfile to use 32-bit or 64-bit ubuntu, change any other confugration. i.e.

    config.vm.box = "ubuntu/trusty32"
    # or
    config.vm.box = "ubuntu/trusty64"

Update other otions i.e. nfs for synced_folders or change memory or cpu amounts. 

6) (OPTIONAL) Update the playbook.yml vars for git_username and git_email used for bitbucket auth.

7) Include all required private keys in your ~/.ssh host folder, the ones starting with the name id_rsa will be copied over. Keys to consider are for access to AWS, Bitbucket, Trapsshman / project server access.

8) Include shared projects in ~/projects, make the directory it it doesn't exist. Can be empty to start. The same directory will be synced on the guest dev box. Note: *inux sym links don't work on NTFS

9) Start the devbox: 

    vagrant up 

When done run: 
    vagrant ssh
    
Run `vagrant provision` to update any provision changes any time. Run `vagrant suspend` to put the box on standby, or use `vagrant halt` to shut it down. Note, you can use `vagrant destroy` later when you are done with the box. 

10) Browse a project. You may start django server using: `manage.py runserver 0.0.0.0:8000` and access it at `localhost:9000` on your host machine. You can also use `192.168.222.220:8000` or whatever it is that you configured private networking with.  Optionally, run `gunicorn wsgi:application` to start your app.

# setup on windows / other

Note: Does not work with symlinks, will figure out a way to host files on vm instead for windows users.

This setup should work on any os becuase instead of installing ansible on your host os, we install it on the guest instead and let it provision itself.  Instead of trying to install ansible in windows, you can do it this way.

1) Install and provision your VM with ubuntu 14.04 either using Vagrant or manually. See Steps 1 & 2 from linux/ mac install.

Essentially you just need to comment out the following in the Vagrantfile to provision Ubuntu using Vagrant:

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.host_key_checking = false
      ansible.extra_vars = { ansible_ssh_user: 'vagrant',
              ansible_connection: 'ssh',
              ansible_ssh_args: '-o ForwardAgent=yes'}
    end

Note: "nfs" synced_folders will be ignored. It's a good idea to use "smb" for this settting. SMB only works for windows hosts, NFS only works for linux hosts.

2) Once complete, SSH into your instance & install ansible


    vagrant ssh
    sudo pip install ansible


3) Install sshpass to be able to log in using password

    sudo apt-get install sshpass

4) Run the playbook locally

    ansible-playbook -i inventory/local playbook.yml  -vvvv
