SMViewer
========

What's this?
------------

SMView is a web app that provides a simple GUI for NuSMV_.

The server-side is written in Python_ using the CherryPy_ web framework and a sqlite_ database. It also uses neat stuff like CodeMirror_, CoffeeScript_, Underscore_ and jQuery_. Fancy, eh?

.. _NuSMV: http://nusmv.fbk.eu
.. _Python: http://www.python.org
.. _CherryPy: http://cherrypy.org
.. _sqlite: http://sqlite.org
.. _CodeMirror: http://codemirror.net
.. _CoffeeScript: http://coffeescript.org
.. _Underscore: http://underscorejs.org
.. _jQuery: http://jquery.com

Due to the NuSMV licence I cannot give you a demo, just trust me: it's super cool. A screenshot of SMView is available at http://arnovanlumig.com/static/smview.png


How to install
--------------

SMViewer requires a slightly customised version of NuSMV because we need the trace output to be in XML format for easy parsing. This can be done by executing ``set default_trace_plugin 4`` in interactive mode, but I wanted to run NuSMV in batch mode for simplicity. The only required modification is adding this after line 815 in ``cinit/cinitData.c`` (i.e. right after NuSMV has detected that it is running in batch mode)::

   set_default_trace_plugin(OptsHandler_get_instance(), 4);

Then build NuSMV as usual and make sure the executable is in the PATH of the web process.

Then simply run ``python app.py`` after ensuring that you have installed all the dependencies. First visit ``localhost:8080/setup`` to create the sqlite database.


Licence
-------

The SMViewer code in this repository (i.e. everything except ``static/lib``, ``static/jquery*`` and ``static/underscore.js``) is BSD-licenced. See LICENCE.


How to read the code
--------------------

Okay, so the code is a bit messy. I don't usually code in Python.

- app.py is the web-app side of the code. It contains a few functions to make CherryPy happy and does the database interaction
- parse.py contains functions to parse NuSMV output
- test.py contains a function runs NuSMV on the given code and either parses the errors or the trace output.