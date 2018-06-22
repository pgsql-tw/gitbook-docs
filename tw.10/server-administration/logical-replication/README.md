# 31. Logical Replication

Logical replication is a method of replicating data objects and their changes, based upon their replication identity \(usually a primary key\). We use the term logical in contrast to physical replication, which uses exact block addresses and byte-by-byte replication. PostgreSQL supports both mechanisms concurrently, see [Chapter 26](https://www.postgresql.org/docs/10/static/high-availability.html). Logical replication allows fine-grained control over both data replication and security.

Logical replication uses a _publish_ and _subscribe_ model with one or more _subscribers_ subscribing to one or more _publications_ on a _publisher_ node. Subscribers pull data from the publications they subscribe to and may subsequently re-publish data to allow cascading replication or more complex configurations.

Logical replication of a table typically starts with taking a snapshot of the data on the publisher database and copying that to the subscriber. Once that is done, the changes on the publisher are sent to the subscriber as they occur in real-time. The subscriber applies the data in the same order as the publisher so that transactional consistency is guaranteed for publications within a single subscription. This method of data replication is sometimes referred to as transactional replication.

The typical use-cases for logical replication are:

* Sending incremental changes in a single database or a subset of a database to subscribers as they occur.
* Firing triggers for individual changes as they arrive on the subscriber.
* Consolidating multiple databases into a single one \(for example for analytical purposes\).
* Replicating between different major versions of PostgreSQL.
* Giving access to replicated data to different groups of users.
* Sharing a subset of the database between multiple databases.

The subscriber database behaves in the same way as any other PostgreSQL instance and can be used as a publisher for other databases by defining its own publications. When the subscriber is treated as read-only by application, there will be no conflicts from a single subscription. On the other hand, if there are other writes done either by an application or by other subscribers to the same set of tables, conflicts can arise.

