package { ['puppet', 'socat', 'erlang', 'rabbitmq-server', 'redis']:
  ensure   => 'installed',
  provider => 'yum',
}
service { ['redis', 'rabbitmq-server']:
  ensure => running,
  enable => true,
}
exec { 'delete_guest':
  command => "cd /opt/puppetlabs/puppet/manifests ; sh add_user.sh",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}
package { 'celery':
  ensure   => '4.3.0',
  provider => 'pip',
}
