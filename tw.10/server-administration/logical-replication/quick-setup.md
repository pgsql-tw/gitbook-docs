---
description: 版本：10
---

# 31.9. Quick Setup

First set the configuration options in `postgresql.conf`:

```text
wal_level = logical
```

The other required settings have default values that are sufficient for a basic setup.

`pg_hba.conf` needs to be adjusted to allow replication \(the values here depend on your actual network configuration and user you want to use for connecting\):

```text
host     all     repuser     0.0.0.0/0     md5
```

Then on the publisher database:

```text
CREATE PUBLICATION mypub FOR TABLE users, departments;
```

And on the subscriber database:

```text
CREATE SUBSCRIPTION mysub CONNECTION 'dbname=foo host=bar user=repuser' PUBLICATION mypub;
```

The above will start the replication process, which synchronizes the initial table contents of the tables `users` and `departments` and then starts replicating incremental changes to those tables.

