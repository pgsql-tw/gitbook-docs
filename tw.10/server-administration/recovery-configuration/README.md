# 27. Recovery Configuration

This chapter describes the settings available in the `recovery.conf` file. They apply only for the duration of the recovery. They must be reset for any subsequent recovery you wish to perform. They cannot be changed once recovery has begun.

Settings in `recovery.conf` are specified in the format `name = 'value'`. One parameter is specified per line. Hash marks \(`#`\) designate the rest of the line as a comment. To embed a single quote in a parameter value, write two quotes \(`''`\).

A sample file, `share/recovery.conf.sample`, is provided in the installation's `share/` directory.

