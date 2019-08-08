#!/bin/bash
rpm -Uvh https://yum.puppet.com/puppet6-release-el-7.noarch.rpm
yum -y install puppet
ln -s /opt/puppetlabs/bin/puppet /usr/bin/puppet}
