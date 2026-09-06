## Chapter 26. High Availability, Load Balancing, and Replication

**Table of Contents**

[26.1. Comparison of Different Solutions](different-replication-solutions.md)

[26.2. Log-Shipping Standby Servers](warm-standby.md)
:   [26.2.1. Planning](warm-standby.md#STANDBY-PLANNING)

    [26.2.2. Standby Server Operation](warm-standby.md#STANDBY-SERVER-OPERATION)

    [26.2.3. Preparing the Primary for Standby Servers](warm-standby.md#PREPARING-PRIMARY-FOR-STANDBY)

    [26.2.4. Setting Up a Standby Server](warm-standby.md#STANDBY-SERVER-SETUP)

    [26.2.5. Streaming Replication](warm-standby.md#STREAMING-REPLICATION)

    [26.2.6. Replication Slots](warm-standby.md#STREAMING-REPLICATION-SLOTS)

    [26.2.7. Cascading Replication](warm-standby.md#CASCADING-REPLICATION)

    [26.2.8. Synchronous Replication](warm-standby.md#SYNCHRONOUS-REPLICATION)

    [26.2.9. Continuous Archiving in Standby](warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY)

[26.3. Failover](warm-standby-failover.md)

[26.4. Hot Standby](hot-standby.md)
:   [26.4.1. User's Overview](hot-standby.md#HOT-STANDBY-USERS)

    [26.4.2. Handling Query Conflicts](hot-standby.md#HOT-STANDBY-CONFLICT)

    [26.4.3. Administrator's Overview](hot-standby.md#HOT-STANDBY-ADMIN)

    [26.4.4. Hot Standby Parameter Reference](hot-standby.md#HOT-STANDBY-PARAMETERS)

    [26.4.5. Caveats](hot-standby.md#HOT-STANDBY-CAVEATS)

<a id="id-1.6.13.2"></a><a id="id-1.6.13.3"></a><a id="id-1.6.13.4"></a><a id="id-1.6.13.5"></a><a id="id-1.6.13.6"></a><a id="id-1.6.13.7"></a>

Database servers can work together to allow a second server to
take over quickly if the primary server fails (high
availability), or to allow several computers to serve the same
data (load balancing). Ideally, database servers could work
together seamlessly. Web servers serving static web pages can
be combined quite easily by merely load-balancing web requests
to multiple machines. In fact, read-only database servers can
be combined relatively easily too. Unfortunately, most database
servers have a read/write mix of requests, and read/write servers
are much harder to combine. This is because though read-only
data needs to be placed on each server only once, a write to any
server has to be propagated to all servers so that future read
requests to those servers return consistent results.

This synchronization problem is the fundamental difficulty for
servers working together. Because there is no single solution
that eliminates the impact of the sync problem for all use cases,
there are multiple solutions. Each solution addresses this
problem in a different way, and minimizes its impact for a specific
workload.

Some solutions deal with synchronization by allowing only one
server to modify the data. Servers that can modify data are
called read/write, *master* or *primary* servers.
Servers that track changes in the primary are called *standby*
or *secondary* servers. A standby server that cannot be connected
to until it is promoted to a primary server is called a *warm
standby* server, and one that can accept connections and serves read-only
queries is called a *hot standby* server.

Some solutions are synchronous,
meaning that a data-modifying transaction is not considered
committed until all servers have committed the transaction. This
guarantees that a failover will not lose any data and that all
load-balanced servers will return consistent results no matter
which server is queried. In contrast, asynchronous solutions allow some
delay between the time of a commit and its propagation to the other servers,
opening the possibility that some transactions might be lost in
the switch to a backup server, and that load balanced servers
might return slightly stale results. Asynchronous communication
is used when synchronous would be too slow.

Solutions can also be categorized by their granularity. Some solutions
can deal only with an entire database server, while others allow control
at the per-table or per-database level.

Performance must be considered in any choice. There is usually a
trade-off between functionality and
performance. For example, a fully synchronous solution over a slow
network might cut performance by more than half, while an asynchronous
one might have a minimal performance impact.

The remainder of this section outlines various failover, replication,
and load balancing solutions.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/high-availability.html)（英文原文，待翻譯）
