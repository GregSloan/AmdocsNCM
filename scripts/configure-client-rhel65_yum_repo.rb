# Recipe:: configure-client-rhel65_yum_repo.rb
#    
#
# Copyright 2016, Amdocs
#
# All rights reserved - Do Not Redistribute
#
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



execute "rpm --import #{node.bws.config.rhel65.yum_repo_url}/RPM-GPG-KEY-redhat-release" do
  creates ''
end


