cd /tmp
rpmbuild -ta munge-0.5.13.tar.xz
rpm -ivh --force ~/rpmbuild/RPMS/x86_64/munge-*
rpmbuild -ta slurm-20.11.7.tar.bz2
rpm -ivh ~/rpmbuild/RPMS/x86_64/slurm-*
