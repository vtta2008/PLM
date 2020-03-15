
This is the last directory we have in this project. It holds configurations for GitHub Actions which we use for CI/CD.
We have two files, first of them - build-test.yml is responsible for building, testing and linting our source code on
every push. Second file - push.yml pushes our built application to GitHub Package Registry every time we create
tag/release on GitHub. More on this in a separate blog post.
