package { ['yum-utils', 'device-mapper-persistent-data', 'lvm2' ]:
  ensure   => 'installed',
  provider => 'yum',
}

exec { 'repo':
  command => "yum-config-manager add-repo https://download.docker.com/linux/centos/docker-ce.repo",
  path => '/sbin:/bin:/usr/sbin:/usr/bin',
}

package { ['docker-ce', 'docker-ce-cli', 'containerd.io' ]:
  ensure   => 'installed',
  provider => 'yum',
}
