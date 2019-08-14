package { ['yum-utils', 'device-mapper-persistent-data', 'lvm2' ]:
  ensure   => 'installed',
  provider => 'yum',
}

exec { 'repo':
  command => "yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}

package { ['docker-ce', 'docker-ce-cli', 'containerd.io' ]:
  ensure   => 'installed',
  provider => 'yum',
}
service { 'docker':
  ensure => 'running',
  enable => 'true',
}
exec { 'docker-compose':
  command => "sudo curl -L 'https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compos; chmod +x /usr/local/bin/docker-compose",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}
