# HPC Auth 2023


## High Performance Computing Account and Authorization Management 
Every summer that the High Performance Computing Engineering Academy is hosted, the academy needs to create and add users to each node on every cluster, and at the end of those 3 months, all user accounts need to be removed. This process is repeated again and again for every summer the academy is hosted. For example, this summer the academy hosted 6 interns. Each intern was given a six-node cluster to build and work out. That's 36 machines and at least 36 accounts that need to be added and removed. Instead of doing all this account stuff manually, we sought to implement an account management system that would work in an HPC environment that would simplify the creation and management of users on our clusters.

## Goals of Our Project
We defined several goals for our project:

    Centralized authentication​

        - Login to several systems/services with single set of credentials​

        - Robust authentication methods​

    User/Group Management​

        - Tools for admin to manage users, groups, and roles​

        - Web UI that makes system simpler to visualize​

    Host-Based Access Control​

        - Control which users/groups can access specific servers in the network​

    Certificate Authority​

        - Provides secure communication for web services​

## FreeIPA
We decided to use FreeIPA as our Identity Management Provider. In this repo, you can find several tutorials and documentation for FreeIPA server/client installations and configurations. You can find their official open source github repo here.

TLDR of FreeIPA:

_What is it?_

FreeIPA is a tool to create a security, identity and authentication network that utilizes existing Linux technologies. The domains created in the framework consist of a server providing shared resources (similar to a management node) and several clients (similar to compute nodes).

_What services does it provide?_

The FreeIPA allows you to create and manage users/machines across clients in a domain. You can also write policies and determine access controls for shared resources among users.

_How does it work?_

FreeIPA servers manage client identities and works as an authentication server that hosts shared resources such as DNS, NTP, Kerberos, and authentication certificates. (Though the FreeIPA server doesn't need to be all these other servers). FreeIPA client machines are configured to share identification information with the server and ask for authentication policies.

## Google Authenticator
We decided to use GoogleAuth as our 2 Factor Authentication Provider. It offers a six-digit time based one time password from their mobile app. 

## Support / References
    FreeIPA - https://freeipa.org/page/Quick_Start_Guide#getting-started-with-ipa ​

    FreeIPA Manual - https://abbra.fedorapeople.org/.todo/freeipa-docs/​

    FreeIPA Tutorial - https://linux.how2shout.com/how-to-install-freeipa-on-almalinux-or-rocky-8/​

    RedHat IPA - https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/configuring_identity_management/installing_the_ipa_client_on_linux ​

    Dogtag PKI + FreeIPA - https://www.admin-magazine.com/Archive/2022/70/Certificate-management-with-FreeIPA-and-Dogtag ​

    Risk-Based Authentication - https://riskbasedauthentication.org/ 


## Authors and acknowledgment
Megan Acosta & 
Shane Cancilla

Mentor: Dave Fox

