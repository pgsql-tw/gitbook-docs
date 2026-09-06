## Chapter 18. Server Setup and Operation

**Table of Contents**

[18.1. The PostgreSQL User Account](postgres-user.md)

[18.2. Creating a Database Cluster](creating-cluster.md)
:   [18.2.1. Use of Secondary File Systems](creating-cluster.md#CREATING-CLUSTER-MOUNT-POINTS)

    [18.2.2. File Systems](creating-cluster.md#CREATING-CLUSTER-FILESYSTEM)

[18.3. Starting the Database Server](server-start.md)
:   [18.3.1. Server Start-up Failures](server-start.md#SERVER-START-FAILURES)

    [18.3.2. Client Connection Problems](server-start.md#CLIENT-CONNECTION-PROBLEMS)

[18.4. Managing Kernel Resources](kernel-resources.md)
:   [18.4.1. Shared Memory and Semaphores](kernel-resources.md#SYSVIPC)

    [18.4.2. systemd RemoveIPC](kernel-resources.md#SYSTEMD-REMOVEIPC)

    [18.4.3. Resource Limits](kernel-resources.md#KERNEL-RESOURCES-LIMITS)

    [18.4.4. Linux Memory Overcommit](kernel-resources.md#LINUX-MEMORY-OVERCOMMIT)

    [18.4.5. Linux Huge Pages](kernel-resources.md#LINUX-HUGE-PAGES)

[18.5. Shutting Down the Server](server-shutdown.md)

[18.6. Upgrading a PostgreSQL Cluster](upgrading.md)
:   [18.6.1. Upgrading Data via pg_dumpall](upgrading.md#UPGRADING-VIA-PGDUMPALL)

    [18.6.2. Upgrading Data via pg_upgrade](upgrading.md#UPGRADING-VIA-PG-UPGRADE)

    [18.6.3. Upgrading Data via Replication](upgrading.md#UPGRADING-VIA-REPLICATION)

[18.7. Preventing Server Spoofing](preventing-server-spoofing.md)

[18.8. Encryption Options](encryption-options.md)

[18.9. Secure TCP/IP Connections with SSL](ssl-tcp.md)
:   [18.9.1. Basic Setup](ssl-tcp.md#SSL-SETUP)

    [18.9.2. OpenSSL Configuration](ssl-tcp.md#SSL-OPENSSL-CONFIG)

    [18.9.3. Using Client Certificates](ssl-tcp.md#SSL-CLIENT-CERTIFICATES)

    [18.9.4. SSL Server File Usage](ssl-tcp.md#SSL-SERVER-FILES)

    [18.9.5. Creating Certificates](ssl-tcp.md#SSL-CERTIFICATE-CREATION)

[18.10. Secure TCP/IP Connections with GSSAPI Encryption](gssapi-enc.md)
:   [18.10.1. Basic Setup](gssapi-enc.md#GSSAPI-SETUP)

[18.11. Secure TCP/IP Connections with SSH Tunnels](ssh-tunnels.md)

[18.12. Registering Event Log on Windows](event-log-registration.md)

This chapter discusses how to set up and run the database server,
and its interactions with the operating system.

The directions in this chapter assume that you are working with
plain PostgreSQL without any additional
infrastructure, for example a copy that you built from source
according to the directions in the preceding chapters.
If you are working with a pre-packaged or vendor-supplied
version of PostgreSQL, it is likely that
the packager has made special provisions for installing and starting
the database server according to your system's conventions.
Consult the package-level documentation for details.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime.html)（英文原文，待翻譯）
