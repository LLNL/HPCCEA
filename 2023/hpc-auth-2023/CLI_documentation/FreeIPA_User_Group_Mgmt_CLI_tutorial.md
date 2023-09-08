<a name="br1"></a> 

**FreeIPA User & Group Management**

**References**

[Manage users and group (CLI)](https://computingforgeeks.com/manage-users-and-groups-in-freeipa-using-cli/)

[Official Documenation: OTP (w/commands)](https://freeipa.org/page/V4/OTP)

[RedHat How to Add tokens to users](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/linux_domain_identity_authentication_and_policy_guide/otp#add-token-admin-ui-cmd)

[User and Group mgmt commands](https://computingforgeeks.com/manage-users-and-groups-in-freeipa-using-cli/?expand_article=1)

[TLDR HBAC Tutorial](https://linuxgurublog.wordpress.com/2017/11/01/configure-freeipa-hbac-host-based-access-control-part-5/)

[Official Documentation: HBAC rule tutorial](https://freeipa.readthedocs.io/en/latest/workshop/4-hbac.html)

[RedHat HBAC rule tutorial](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/identity_management_guide/hbac-rules#hbac-rules-cmd)

**Add user from Server CLI**

1\. Generate a Kerberos ticket for your admin user

`# kinit admin`

Password for admin@IPA.TEST: # enter admin password

2\. List active Kerberos tickets

`# klist`

    Ticket cache: KCM:0:18722

    Default principal: admin@IPA.TEST

    Valid starting

    Expires

    Service principal

    07/26/2023 10:30:22 07/27/2023 09:35:12 HTTP/eradon2.ipa.test@IPA.TEST

3\. Add your user, specifying your first and last name and option to set a password

`# ipa user-add acosta19 --first=Megan --last=Acosta --password`

    Password:

    Enter Password again to verify:

    ---------------------

    Added user "acosta19"

    ---------------------

    User login: acosta19

    First name: Megan

    Last name: Acosta

    Full name: Megan Acosta

    Display name: Megan Acosta

    Initials: MA

    Home directory: /home/acosta19

    GECOS: Megan Acosta

    Login shell: /bin/sh

    Principal name: acosta19@IPA.TEST

    Principal alias: acosta19@IPA.TEST

    User password expiration: 20230726173043Z

    Email address: acosta19@ipa.test

    UID: 1776600003

    GID: 1776600003

    Password: True

    Member of groups: ipausers

    Kerberos keys available: True

4\. Check that there's an entry for the user you just created



<a name="br2"></a> 

`# ipa user-find`

    ---------------

    2 users matched

    ---------------

    User login: acosta19

    First name: Megan

    Last name: Acosta

    Home directory: /home/acosta19

    Login shell: /bin/sh

    Principal name: acosta19@IPA.TEST

    Principal alias: acosta19@IPA.TEST

    Email address: acosta19@ipa.test

    UID: 1776600003

    GID: 1776600003

    Account disabled: False

    User login: admin

    Last name: Administrator

    Home directory: /home/admin

    Login shell: /bin/bash

    Principal alias: admin@IPA.TEST, root@IPA.TEST

    UID: 1776600000

    GID: 1776600000

    Account disabled: False

    ----------------------------

    Number of entries returned 2

    ----------------------------

**Add One Time Password from CLI**

**\*\* DO NOT USE YOUR CAMERA ON SITE TO SCAN QR CODE\*\***

1\. Create a user called otpuser with a foopassword

`# ipa user-add otpuser`

2\. Create OTP token

`# ipa otptoken-add --owner=otpuser`

3\. Modify the otpuser to use the Google Auth OTP. The output will show updates to the otpuser, confirmation of OTP token addition, and a QR code. (check `ipa user-find otpuser` to see if otp token has been added, since this step may not be needed if so)

`# ipa user-mod otpuser --user-auth-type=otp`

4\. Copy down the OTP token URI (or scan the QR code from with your Google Auth app). You now have an OTP for otpuser on your phone!

But we're not done yet...

5\. Sync the OTP you just created

`# ipa otptoken-sync --user=otpuser`

    User ID:

    First Code:

    Second Code:

Now that you've created a user with an OTP login, you can test it by logging into one of your hosts as otpuser. You should be prompted for your "First token" and "Second token."

**Add User Scripting**

Here's this interesting [script](https://www.coveros.com/create-freeipa-users-script/)[ ](https://www.coveros.com/create-freeipa-users-script/)that automates adding users. It'd be quick to adapt this to HPC academy. (I think :])

**Add User and Host Groups**



<a name="br3"></a> 

We're going to practice making user and host groups!

1\. Create another doe user, johndoe

2\. Add a user group called doe

`# ipa group-add doe`

3\. Add jane and john doe as members

`# ipa group-add-member doe --users=janedoe`

`# ipa group-add-member doe --users=johndoe`

4\. Display the group you just created

`# ipa group-show`

    Group name: group_name

5\. Add a host group called clientx

`# ipa hostgroup-add -desc 'clusternameX' clientX`

6\. Add your cluster node to the host group you just created

`# ipa hostgroup-add-member clientX --hosts FQDN_of_client_node`

7\. Display the group you just created

`# ipa hostgroup-find`

**Add Host Based Access Controls**

Now that we have some users and clients, let's try setting some rules for them.

1\. Show all existing HBAC rules

`# ipa hbacrule-find`

2\. Disable the allow_all HBAC rule. Otherwise, the rule we add won't really do anything

`# ipa hbacrule-disable allow_all`

3\. Add a new HBAC rule

`# ipa hbacrule-add doe_rules`

4\. Add the clientx group as a host to the rule

`# ipa hbacrule-add-host doe_rules --hostgroup clientX`

5\. Add doe group to the rule

`# ipa hbac-add-user doe_rules --group doe`

6\. (you can also add/remove individual users)



<a name="br4"></a> 

`# ipa hbac-add-user doe_rules --users=USERNAME`

`# ipa hbac-remove-user doe_rules --users=USERNAME`

7\. Add service to the rule

`# ipa hbac-add-service doe_rules --servicecat=all`

8\. Test the rule!

`# ipa hbactest --host FQDN_of_client_node --service sshd --user janedoe`

You'll know the rule is correctly configured if Access granted is True and the Match rules is the doe_rules we just created

