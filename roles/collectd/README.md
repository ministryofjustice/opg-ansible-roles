================
opg-collectd-formula
================

A salt formula that installs and configures collectd. The system statistics collection daemon.

.. note::

    See the full `Salt Formulas installation and usage instructions
    <http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html>`_.
    This is based on the official `Collectd Salt Formula <https://github.com/saltstack-formulas/collectd-formula>`_.
Available states
================

.. contents::
    :local:

``collectd``
------------

Installs the collectd package, and starts the associated collectd service.

``collectd.service``
------------

Metastate used to include service into respective plugin states, included in ``collectd`` state.

``collectd.modules``
------------

This state helps distributing collectd external modules written in various languages
(see [python](https://collectd.org/wiki/index.php/Plugin:Python) or
[perl](https://collectd.org/wiki/index.php/Plugin:Perl) for example).

Sample usage:

* Include ``collectd.modules`` in your topfile.
* Create collectd/modules/files folder in your states.
* Put modules you need in that folder.
* Modules will be put in ``collectd.moduledirconfig`` folder.


``collectd.ntpd``
------------

Enables and configures the ntpd plugin.

``collectd.packages``
------------

This state is used to install OS packages collectd plugins depend on.

``collectd.syslog``
------------

Enables and configures the syslog plugin.

``collectd.python``
------------

Enables and configures the python plugin, which allows executiong arbitrary python scripts.

``collectd.btrfs``
------------

Enables and configures a custom btrfs plugin, which monitors btrfs filesystems


Usage
================

Custom state file
-----------------

Create a custom state file (for example ``collectd-custom.sls``) that includes the plugins you want and the base state. ::

    include:
      - collectd
      - collectd.ntpd
      - collectd.syslog

Then in your topfile: ::

    'servername':
      - collectd-custom

Directly in topfile
-------------------

Or if you don't mind having long lists in your topfile, just add whatever plugins you want and the base state. ::

    'servername':
      - collectd
      - collectd.ntpd
      - collectd.syslog

Combined
--------

Or you can combine both - default plugins in custom state and specific in topfile. ::

    'docker-server':
      - collectd-custom
      - collectd.btrfs
