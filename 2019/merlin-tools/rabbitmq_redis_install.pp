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
  ensure   => 'installed',
  provider => 'pip',
}
exec { 'certs':
  command => "sh ssl.sh",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}
file { '/etc/rabbitmq/rabbitmq.config':
  ensure   => 'file',
  group    => 0,
  mode     => '0777',
  owner    => 0,
  #selrole  => 'object_r',
  seltype  => 'usr_t',
  seluser  => 'unconfined_u',
  #source   => './rabbitmq.config',
}
