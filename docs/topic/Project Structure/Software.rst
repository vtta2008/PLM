PYTHON SOFTWARE PROJECS STRUCTURE
#################################

OVERVIEW
--------

.. code-block:: python

    |- entry-script.py  '# most projects need a file that spins up processes or start the app'
    |- helpers/         '# scaffolding, sometimes unstructured code needed for your app'
    |- utils/           '# code that has been written for this project but can be easily generalized'
    |- models/
    |- tests/
    |- docs/


.. topic:: Helper

    "*This can be thought of as scaffolding code.*"

    This is where we put 'dirty code', code that does not contain core business rules but that's nonetheless needed for the
    project.

    It's important to have a separate for this kind of code because if you place it together with actual business logic code,
    it will be increasingly hard to understand the business logic because there's so much other stuff mixed in.

    Having a separate place for this stops it from contaminating your main business logic, which are the most important parts
    of the application.

    Examples of helper code:

        * Converting things from one structure to another
        * Input validation
        * Formatting stuff for display purposes

.. topic:: Utils

    Here is where you should put code that you need for your application, but that is general enough that it could be
    used somewhere else.

    Using a separate folder for this helps you rememeber to write this code in a way that is totally decoupled from the
    rest of your application.

    The Hollywood Principle1 applies here: in other words, code in utils/ does not call methods or use stuff from other
    parts of the project. If it did, it would get coupled with the rest of the project and you wouldn't be able to reuse
    it outside.

.. topic:: Models

    This is where the core of your business logic goes. Here you write classes, modules and components that make up the domain you are writing code for.

    Here you go all-in with everything you learned about software engineering, domain-driven design and all that. Here is where you build

    * code that's easy to change

    * code that you can test easily

    * code that does only what it's supposed to and no more

    * code that knows only enough about the external world so that it's loosely coupled with other components

    * code you feel proud about.

.. topic:: Tests

    Here's something I find funny about tests. Most people think that you need testing because you want to make sure
    method add(x,y) return 2 when you call add(1,1). That's not it.

    I see **two main reasons for writing tests.**

        - Tests are documentation

            * You write tests so that people can quickly see the use cases for you code and how to use it.

        - Tests allow you to update and modify your project

            * Without tests you will never be comfortable making your code better, because you'll be afraid it will
              break what currently works.

            * Without tests, you can never alter the structure of your project, fix bad architectural decisions of refactor.

    .. note:: Remember

        Too much testing is just as bad as too little testing. Writing too many test cases or testing the wrong things
        will make you code brittle (i.e. easily breakable) and it may hinder change and updates.

API projects
------------

You will need another directory called controllers/ to place the request handlers. Depending upon the web framework you
are using, it will place additional constraints on how you strcuture your code, but the advice in the main strcuture
remains.

    - Specific directory for controllers

        * In my experience, we generally tend to structure our web applications around the controllers, so they tend to
          get bloated if we don't watch out.

    - Specialized Helpers

        * Controller code tends to get large an complex fast. It's better to have one helper class for each controller
          or specific API method handler.

        * Each controller should only call its own helper and, if needed, that helper will in turn call other generic
          helpers in the helpers/ directory.

.. code-block:: python

    |-  entry-script.py
    |-  controllers/                            # one file per controller
        |-  user_controller.py
    |-  helpers/
        |- controllers/
            |- user_controller_helper.py        # this should only be called by user_controller.py
    |- utils/
    |- models/
    |- tests/
        |- web_tests/                           # a specific folder tests against the HTTP API


COMMANDLINE tools
------------------

For projects that you will want to use from the command-line (CLI), you need a directory called bin/ which is what you
will tell your users to add to their $PATH environment variable to use your code. Everything else stays the same.

DATA SCIENCE projects
---------------------

For data science projects, the Cookie Cutter data science project is probably a good start: Cookie cutter data science.

I would suggest removing a few things I think are overkill and adding a couple directories, so that it looks like a very
minimal version of the original thing:

.. code-block:: python

    |-  data/
        |-  raw/                '# raw data, as you receive it '
        |-  processed/          '# datasets with extracted features'
        |-  output/             '# output datasets generated by your models'
        |-  cache/              '# you want to cache stuff that takes too long to calculate'
    |-  docs/                   '# still important, but do not overdo it'
        |-  presentations/      '# good to keep track of what you presented to clients/boss'
    |-  models/                 '# saved models go here'
    |-  notebooks/              '# most of the action happens HERE'
    |-  src/                    '# as per my original structure suggestion'
        |-  helpers/            '# helpers for plotting, preprocessing, etc'
        |-  utils/              '# stuff you can reuse in other projects'

