package { ['puppet', 'socat', 'erlang', 'rabbitmq-server', 'redis']:
  ensure   => 'installed',
  provider => 'yum',
}
exec { 'delete_guest':
  command => "sh add_user.sh",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}
exec { 'install_pip':
  command => "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py; python get-pip.py",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}
package { 'Celery':
  ensure   => 'installed',
  provider => 'pip',
}
exec { 'certs':
  command => "sh ssl.sh",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}
service { ['redis', 'rabbitmq-server']:
  ensure => running,
  enable => true,
}
file { '/etc/rabbitmq/rabbitmq.config':
  ensure   => 'file',
  group    => 0,
  mode     => '0644',
  owner    => 0,
  seltype  => 'usr_t',
  seluser  => 'system_u',
  source   => '/tmp/rabbitmq.config',
}
