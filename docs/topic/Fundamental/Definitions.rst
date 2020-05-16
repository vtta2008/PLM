
PEP 8 and Naming
================

Python style is governed largely by a set of documents called Python Enhancement Proposals, abbreviated PEP. Not all PEPs are actually adopted, of course - that's why they're called "Proposals" - but some are. You can browse the master PEP index on the official Python website. This index is formally referred to as PEP 0.

Right now, we're mainly concerned with PEP 8, first authored by the Python language creator Guido van Rossum back in 2001. It is the document which officially outlines the coding style all Python developers should generally follow. Keep it under your pillow! Learn it, follow it, encourage others to do the same.

(Side Note: PEP 8 makes the point that there are always exceptions to style rules. It's a guide, not a mandate.)

Right now, we're chiefly concerned with the section entitled "Package and Module Names"..

.. note::

    Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.

We'll get to what exactly modules and packages are in a moment, but for now, understand that modules are named by filenames, and packages are named by their directory name.

In other words, filenames should be all lowercase, with underscores if that improves readability. Similarly, directory names should be all lowercase, without underscores if at all avoidable. To put that another way...

Packages and Modules
====================

This is going to feel anticlimactic, but here are those promised definitions:

Any Python (.py) file is a module, and a bunch of modules in a directory is a package.

Well...almost. There's one other thing you have to do to a directory to make it a package, and that's to stick a file called __init__.py into it. You actually don't have to put anything into that file. It just has to be there.

There is other cool stuff you can do with __init__.py, but it's beyond the scope of this guide, so go read the docs to learn more.

If you do forget __init__.py in your package, it's going to do something much weirder than just failing, because that makes it an implicit namespace package. There's some nifty things you can do with that special type of package, but I'm not going into that here. As usual, you can learn more by reading the documentation: PEP 420: Implicit Namespace Packages.

So, if we look at our project structure, awesomething is actually a package, and it can contain other packages. Thus, we might call awesomething our top-level package, and all the packages underneath its subpackages. This is going to be really important once we get to importing stuff.

Let's look at one a snapshot of my real-world projects, omission, to get an idea of how we're structuring stuff...

.. code-block:: BASH

    omission-git
    |-  LICENSE.md
    |-  omission
        |-  app.py
        |-  common
            |-  classproperty.py
            |-  constants.py
            |-  game_enums.py
            |-  __init__.py
        |-  data
            |-  data_loader.py
            |-  game_round_settings.py
            |-  __init__.py
            |-  scoreboard.py
            |-  settings.py
        |-  game
            |-  content_loader.py
            |-  game_item.py
            |-  game_round.py
            |-  __init__.py
            |-  timer.py
        |-  __init__.py
        |-  __main__.py
        |-  resources
        |-  tests
            |-  __init__.py
            |-  test_game_item.py
            |-  test_game_round_settings.py
            |-  test_scoreboard.py
            |-  test_settings.py
            |-  test_test.py
            |-  test_timer.py
    |-  pylintrc
    |-  README.md
    |-  .gitignore

(In case you're wondering, I used the UNIX program tree to make that little diagram above.)

You'll see that I have one top-level package called omission, with four sub-packages: common, data, game, and tests. I also have the directory resources, but that only contains game audio, images, etc. (omitted here for brevity). resources is NOT a package, as it doesn't contain an __init__.py.

I also have another special file in my top-level package: __main__.py. This is the file that is run when we execute our top-level package directly via python -m omission. We'll talk about what goes in that __main__.py in a bit.

