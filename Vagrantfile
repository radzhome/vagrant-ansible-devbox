VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # For setting up multiple boxes
  #config.vm.define :ubuntuvm do |ubuntu_config|
    # Every Vagrant env. requires a box to build off of
    #ubuntu_config.vm.box = "ubuntu/trusty64"
    config.vm.box = "ubuntu/trusty32"

    # This will change default user away from vagrant, and use password not cert
    #config.ssh.username = "devbox-user"
    #config.ssh.password = "123TestPass"  # vagrant (default)
    # If true, then any SSH connections made will enable agent forwarding.
    config.ssh.forward_agent = true
    # Didn't change the default cert
    #config.ssh.private_key_path = "~/.ssh/id_rsa"

    # Virtuaqlbox options, default is 512MB memory
    config.vm.provider "virtualbox" do |v|
      v.memory = 1024
      #v.cpus = 2
    end
    # Give a name to the vm in virtualbox
    config.vm.provider "virtualbox" do |v|
      v.name = "ubuntu-devbox"
    end

    # Forward ports from guest to host
    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.network "forwarded_port", guest: 8000, host: 9000
    config.vm.network "forwarded_port", guest: 8001, host: 9001
    config.vm.network "forwarded_port", guest: 8002, host: 9002
    #config.vm.network :public_network
    #config.vm.network :private_network, ip: '192.168.50.5'

    command = "cp -r /host_ssh/id* /home/vagrant/.ssh/"
    config.vm.provision :shell, :inline => command
    #config.vm.provision :shell, :inline => "cp -r /host_ssh/id* /root/.ssh/"
    #config.vm.provision :shell, :inline => "ssh-keygen -R bitbucket.org"
    #config.vm.provision :shell, :inline => "ssh-keyscan bitbucket.org >> /home/vagrant/.ssh/known_hosts"
    #config.vm.provision :shell, :inline => "ssh-keygen -R github.com"
    #config.vm.provision :shell, :inline => "ssh-keyscan github.com >> /home/vagrant/.ssh/known_hosts"

    # Enable provisioning with ansible, specifying the playbook file
    config.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook.yml"
      #ansible.extra_vars = { ansible_ssh_user: 'devbox-user' }
    end

    # Shared folders local path, guest path
    config.vm.synced_folder ".", "/vagrant", disabled: true
    # TODO: change the <local_user> variable
    #config.vm.synced_folder "/home/<local_user>", "/home/<local_user>" 
    #config.vm.synced_folder "/home/<local_user>", "/home/vagrant", create: true
    #config.vm.synced_folder "/home/<local_home>/projects", "/home/<guest_home>/projects"
    #config.vm.synced_folder "/home/<local_home>/projects", "/home/vagrant/projects"
    config.vm.synced_folder "~/projects", "/home/vagrant/projects"
    config.vm.synced_folder "~/.ssh", "/host_ssh", create: true
  #end
end
