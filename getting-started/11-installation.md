# 1.1. 安裝[^1]

Before you can usePostgreSQLyou need to install it, of course. It is possible thatPostgreSQLis already installed at your site, either because it was included in your operating system distribution or because the system administrator already installed it. If that is the case, you should obtain information from the operating system documentation or your system administrator about how to accessPostgreSQL.

If you are not sure whetherPostgreSQLis already available or whether you can use it for your experimentation then you can install it yourself. Doing so is not hard and it can be a good exercise.PostgreSQLcan be installed by any unprivileged user; no superuser \(root\) access is required.

If you are installingPostgreSQLyourself, then refer to[Chapter 16](https://www.postgresql.org/docs/10/static/installation.html)for instructions on installation, and return to this guide when the installation is complete. Be sure to follow closely the section about setting up the appropriate environment variables.

If your site administrator has not set things up in the default way, you might have some more work to do. For example, if the database server machine is a remote machine, you will need to set the`PGHOST`environment variable to the name of the database server machine. The environment variable`PGPORT`might also have to be set. The bottom line is this: if you try to start an application program and it complains that it cannot connect to the database, you should consult your site administrator or, if that is you, the documentation to make sure that your environment is properly set up. If you did not understand the preceding paragraph then read the next section.

---

[^1]: [PostgreSQL: Documentation: 10: 1.1. Installation](https://www.postgresql.org/docs/10/static/tutorial-install.html)

