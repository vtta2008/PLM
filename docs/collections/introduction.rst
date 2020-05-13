
This is the last directory we have in this project. It holds configurations for GitHub Actions which we use for CI/CD.
We have two files, first of them - build-test.yml is responsible for building, testing and linting our source code on
every push. Second file - push.yml pushes our built application to GitHub Package Registry every time we create
tag/release on GitHub. More on this in a separate blog post.


In case you are not familiar with all of the tools used here, I will give quick description:

Flake8 — is a tool for enforcing code style in your projects — in other words — it’s linter similar to pylint, which we
will use as well. Why use both? It’s true that they overlap, but both of them have some rules that the other doesn’t,
so in my experience it’s worth to use them both.

Bandit — is a tool for finding common security issues in Python code. It works by creating AST (abstract syntax tree)
from your code and running plugins against its nodes. Developers are generally not security experts and also all of us
make mistakes here-and-there, so it’s always nice to have a tool that can spot at least some of those security mistakes
for us.

Coverage.py — is a tool for measuring code coverage of Python programs. It gets triggered when we run our test suite
with Pytest and generates coverage report from the test run. These reports can be in the form of terminal output, but
also XML format which then can be consumed by CI tools.

With that out of the way, let’s go over what we have in setup.cfg. For Flake8 we define exclusion patterns so that we
don't lint code that we don't care about. Below that is an empty ignore section in case we need to ignore some rule
globally. We also set max line length to 120, as keeping line length to 80 is in my opinion unreasonable with the size
of today's screens. Final line sets McCabe complexity threshold to 10, if you are not familiar with cyclomatic complexity
you can find out more here.

Next up is Bandit, all we configure here is target directory, which is the name of our package. We do this so that we
can avoid specifying targets on the command line.

After that follows Coverage.py. First, we enable branch coverage, which means that in places where a line in your
program could jump to more than one next line, Coverage.py tracks which of those destination lines are actually visited.
Next, we omit some files that shouldn’t or can’t be included in coverage measurement, like tests themselves or virtual
environment files. We also exclude specific lines, e.g. lines that are labeled with pragma: no cover comment. Last
Coverage.py config line tells the tool to store generated reports in reports directory. This directory is created
automatically if it doesn't exist already.

The final tool we need to configure is Pylint, the configuration though, is very extensive, like more than 100 lines…
So, I will leave this one out and point you the source here as well as commented and explained pylintrc in Pylint
repository here.

We went through all the tools in setup.cfg but there is one more that cannot be added to setup.cfg and that is Pytest -
even though Pytest docs tell you that you can use setup.cfg, it's not exactly true... As per this issue, the option to
use setup.cfg is being deprecated and there are some bugs like interpolation errors, that won't be fixed, therefore we
will also need pytest.ini file for configuration of Pytest:

The first thing we do here is set a bunch of command line arguments — we enable colors in terminal output, then we
enable coverage reporting for blueprint directory, after that we enable both generations of XML and stdout ( term)
coverage reports. Final 2 arguments (-ra) tell Pytest to output short summary for non-passing tests.

On the next line, we have filterwarnings option which allows us to disable some annoying warnings in the output, for
example, deprecation warnings coming out of some library which we have no control over.

Rest of the config sets up logging. First one just turns it on and other 3 configure level, format and datetime format.
Easier than explaining the format config is just seeing the output itself, which is shown in the next section.

With all the configurations in pytest.ini, all we will need to do to run our test suite is run pytest, not even the
package argument needed!

Last actual configuration file we have is requirement.txt, which contains a list of our dependencies. All you can find
in this file is a list of Python packages, one per line with the optional version of the package. As noted, the package
version is optional, but I strongly suggest you lock versions in requirements.txt to avoid situations, where you might
download newer, incompatible package during build and deployment, and end-up breaking your application.

There are 2 remaining files which aren’t actually config files — our Dockerfiles, namely, dev.Dockerfile and
prod.Dockerfile used for development and production images respectively. I will leave those out for time being as we
will explore those in a separate article where we will talk about CI/CD and deployment. You can, however, check those
files out already in GitHub repository here - https://github.com/MartinHeinz/python-project-blueprint/blob/master/dev.Dockerfile.