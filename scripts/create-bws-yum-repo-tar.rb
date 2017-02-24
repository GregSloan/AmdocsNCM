# Cookbook Name:: bws_9_dot_9_telus
# Recipe:: create-bws-yum-repo-tar.rb
#    
#
# Copyright 2016, Amdocs
#
# All rights reserved - Do Not Redistribute
#



########################################################################
## install the httpd  so that we can server the yum repo
#######################################################################
directory node.bws.config.bws_yum_repo.dir do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

########################################################################
#copy package files to the staging directory
########################################################################
node.bws.packages.each_key do |groupKey| 
    sourceDir = node.bws.packages.defaultSourceDir
    if groupKey != "defaultSourceDir"
        if !node.bws.packages[groupKey][:skip].nil?
          next
        end
        if !node.bws.packages[groupKey][:sourceDir].nil?
            sourceDir = node.bws.packages[groupKey][:sourceDir]
        end
        node.bws.packages[groupKey].each_pair  do |pkgKey,pkgName|
            if pkgKey != "sourceDir"
                remote_file "#{node..config.bws_yum_repo.dir}#{pkgName}" do
                    source "#{sourceDir}#{pkgName}"
                    action :create_if_missing
                end
            end
        end     
    end
end














