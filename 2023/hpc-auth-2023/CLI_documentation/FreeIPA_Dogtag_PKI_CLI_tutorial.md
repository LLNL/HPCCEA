<a name="br1"></a> 

**FreeIPA: Dogtag PKI**

FreeIPA uses Dogtag PKI (Public Key Infrastructure), which is an open-source CA (Certificate Authority) system. It is used for issuing and managing digital certificates (X.509 standard) in a variety of applications, including secure web communication. To learn more about certificates as a whole, and why they're necessary, I recommend watching this [video](https://www.youtube.com/watch?v=iQsKdtjwtYI&t=2s).

A FreeIPA server can create certificates for services within its domain. For this example, we will be creating an Nginx web server on a client IPA machine, and giving it an official certificate for the HTTPS protocol. That way, the IPA web server will now also respond to HTTPS requests with the IPA-signed certificate, so that services that run on the Nginx web server can access it. This comes from a tutorial on this [webpage](https://www.admin-magazine.com/Archive/2022/70/Certificate-management-with-FreeIPA-and-Dogtag).

1. First, we want to install nginx, make a directory for the certificate, and give it SELinux context.
```bash
#install nginx

dnf install -y nginx

#create a directory for the certificate

mkdir -p /etc/nginx/cert

#provide the context for IPA client to store certificates here

semanage fcontext -a -t cert_t "/etc/nginx/cert(/.*)?"

restorecon -v /etc/nginx/cert
```

2. Now we're going to log in to the directory with an admin account, go to the certificate directory, register the service, and request the appropriate certificate.
```bash
#login

kinit admin

#change directory and add the service

ipa service-add HTTP/client.ipa.test

#request the certificate

ipa-getcert request -f client.ipa.test.crt -k client.ipa.test.key -r -K HTTP/client.ipa.test@IPA.TEST -N

client.ipa.test
```

3. For the Nginx server to access the files, it needs the appropriate permissions:
```bash
chown -R nginx. /etc/nginx/cert/*
```

4. In the default /etc/nginx/nginx.conf, enable the commented out # Settings for a TLS enabled serversection and add the reference to your certificate:
```bash
vi /etc/nginx/nginx.conf

# Settings for a TLS enabled server.

#

server {

    listen          443 ssl http2 default_server;
    listen          [::]:443 ssl http2 default_server;
    server_name     _;
    root            /usr/share/nginx/html;

    ssl_certificate "/etc/pki/nginx/www.client.ipa.test.crt";           #change this line
    ssl_certificate_key "/etc/pki/nginx/private/www.client.ipa.test.key";       #change this line
    ssl_session_cache shared:SSL:1m; 
    ssl_session_timeout 10m;
    ssl_ciphers PROFILE=SYSTEM;
    ssl_prefer_server_ciphers on;

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    location / {
    }

    error_page 404 /404.html;
        location = /40x.html {
    }

    error_page 500 502 503 504 /50x.html;
        location = /50x.html {
    }
}
```

Challenge: see if you can complete these same task within the WebUI

