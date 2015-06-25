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

# setup on windows

CONCERNS:

 * home directory not same as unix system, how to solve this for ssh keys and projects? 

 * how will NFS work, windows fs is case insenstive and does not support symbolic links of projects


1) Install and provision your VM with ubuntu 14.04 either using Vagrant or manually.

     See Steps 1) & 2) from linux/ mac install.  
     Also follow step 4) from the linux/ mac install.

You need to comment out /remove the following in the Vagrantfile to provision Ubuntu using Vagrant:

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.host_key_checking = false
      ansible.extra_vars = { ansible_ssh_user: 'vagrant',
              ansible_connection: 'ssh',
              ansible_ssh_args: '-o ForwardAgent=yes'}
    end

This will disable the ansible provision to happen from your host os. Also comment out / change the virtualbox filesharing in the VagrantFile:

    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.synced_folder "~/projects", "/home/vagrant/projects", nfs: true #nfs requires private network
    config.vm.synced_folder "~/.ssh", "/host_ssh", create: true #, nfs: true

Commenting /removing all of this out will revert back to defaults.

2) Once complete, SSH into your instance & install ansible

    vagrant up
    vagrant ssh
    sudo pip install ansible


3) Install sshpass to be able to log in using password. This allows ansible to ssh localhost and provision.

    sudo apt-get install sshpass

NOTE: user / pass is vagrant / vagrant, might not be required.

4) Edit the playbook, comment out the following parts, which will not work in windwos (step 2):

        - name: retrieve the certs in dir
          shell: cp -r /host_ssh/id* /home/vagrant/.ssh/
          sudo: false

This tries to copy the uers ssh keys, will not work in windows.

6) Disable host key checking:
    export ANSIBLE_HOST_KEY_CHECKING=False

7) Run the playbook locally

    ansible-playbook -i inventory/local playbook.yml  -vvvv

    Note: If you get executable file errors, you will have to copy the shared /vagrant directory to local directory on the guest machine and remove the executable permission.


`
COLOR SUPPORT

#export PS1="\[\e[34m\]\u\[\e[m\]@\[\e[33;40m\]\h\[\e[m\]:\w\\$ "
#export PS1='\T-\u \w$(__git_ps1 "(%s)")\$ '
export PS1="\[\e[34m\]\u\[\e[m\]@\[\e[33;40m\]\h\[\e[m\]:\w$(__git_ps1 '(%s)')\$ "

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# enable color support of ls and also add handy aliases
 if [ -x /usr/bin/dircolors ]; then
      test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
      alias ls='ls --color=auto'
 fi
 `
