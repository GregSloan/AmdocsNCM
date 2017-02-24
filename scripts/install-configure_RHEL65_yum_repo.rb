# Cookbook Name:: bws_9_dot_9_telus
# Recipe:: install-configure-RHEL65_yum_repo_server.rb
#    
#
# Copyright 2016, Amdocs
#
# All rights reserved - Do Not Redistribute
#

########################################################################
## make the /chef/rhel65_yum_repo directory 
########################################################################
directory "#{node.bws.config.rhel65.iso_dest_dir}" do
  owner 'root'
  group 'root'
  mode '0755'
end


#########################################################################
## get the RHEL65 image to the right place
########################################################################
remote_file "Copy RHEL 6.5 ISO" do
  path "#{node.bws.config.rhel65.iso_dest_dir}#{node.bws.config.rhel65.iso_name}"
  source "#{node.bws.config.rhel65.iso_src_dir}#{node.bws.config.rhel65.iso_name}"
  owner 'root'
  group 'root'
  mode 0755
  action :create_if_missing
end


#########################################################################
## make the /var/www/html/cdrom/iso directory tree  (assume /var is already there)
########################################################################
directory '/var/www/' do
  owner 'root'
  group 'root'
  mode '0755'
end

directory '/var/www/html/' do
  owner 'root'
  group 'root'
  mode '0755'
end

directory '/var/www/html/cdrom/' do
  owner 'root'
  group 'root'
  mode '0755'
end

directory '/var/www/html/cdrom/iso/' do
  not_if {::File.exist? '/var/www/html/cdrom/iso/'}
  owner 'root'
  group 'root'
  mode '0755'
  ignore_failure true
end

#########################################################################
## mount it!
########################################################################
mount '/var/www/html/cdrom/iso/' do
  device "#{node.bws.config.rhel65.iso_dest_dir}#{node.bws.config.rhel65.iso_name}"
  fstype 'iso9660'
  pass 0
  options ' loop'
  action [:mount, :enable]
end


########################################################################
## import the GPG key locally
#######################################################################
execute 'installing RHEL 6.5 GPG key' do
  command "rpm --import /var/www/html/cdrom/iso/RPM-GPG-KEY-redhat-release"
  creates ''
  action :run
end


########################################################################
## install the deltarpm package
########################################################################
execute 'installing deltarpm' do
  command "rpm -i /var/www/html/cdrom/iso/Packages/deltarpm*.x86_64.rpm"
  creates '/usr/bin/applydeltarpm'
  action :run
end

########################################################################
## install the python-deltarpm package
########################################################################
execute 'installing python-deltarpm' do
  command "rpm -i /var/www/html/cdrom/iso/Packages/python-deltarpm*.x86_64.rpm"
  creates '/usr/lib64/python2.6/site-packages/deltarpm.py'
  action :run
end

########################################################################
## install createrepo from the ISO image
#######################################################################
execute 'installing createrepo' do 
  command "rpm -i /var/www/html/cdrom/iso/Packages/createrepo*.noarch.rpm"
  creates '/usr/bin/createrepo'
  action :run
end

########################################################################
## create the repomd from the image
#######################################################################
execute 'creating the repomd data for the ISO' do
  command 'createrepo /var/www/html/cdrom/'
  creates '/var/www/html/cdrom/iso/repodata'
end


template "/etc/yum.repos.d/rhel65.repo" do
    source "rhel65.repo.erb"
    variables(
        :baseurl => node.bws.config.rhel65.yum_repo_url
    ) 
    owner "root"
    group "root"
    mode "0644"
    action :create
end




