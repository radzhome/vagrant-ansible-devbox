VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty32"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 9000
  config.vm.network "forwarded_port", guest: 8001, host: 9001
  config.vm.network "forwarded_port", guest: 8002, host: 9002

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "playbook.yml"
  end

  # shared folders local path, guest path
  config.vm.synced_folder ".", "/vagrant", disabled: true
  # TODO: change the <local_user> variable
  #config.vm.synced_folder "/home/<local_user>", "/home/<local_user>" 
  config.vm.synced_folder "/home/devbox_user", "/home/devbox_user", create: true
  #config.vm.synced_folder "/home/<local_home>/projects", "/home/<guest_home>/projects"

end
