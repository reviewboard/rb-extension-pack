========
rbsentry
========

This extension makes it easy to connect Review Board to Sentry.io in order to
catch and aggregate exceptions from both the front-end and back-end.

To configure this, you'll need to set some data in your :file:`settings_local.py`:

.. code-block:: python

   SENTRY = {
       'DSN': '<your project DSN>',
       'ENVIRONMENT': 'prod',
   }
