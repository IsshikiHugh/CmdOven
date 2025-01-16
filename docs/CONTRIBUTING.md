# Contributing

Thank you for contributing!

**Before contributing, you are suggested to check this [issue#14](https://github.com/IsshikiHugh/ExpOven/issues/14) first**.

The implementation of [DingTalk backend](./oven/backends/dingtalk/__init__.py) should be a good example.

According to [this](https://stackoverflow.com/questions/35278957/can-i-modify-someone-elses-pull-request-and-push-it-back-in-its-branch/49854013#49854013), I *recommend* you to check "Allow edits from maintainers." when you open the pull request.

Any suggestions (as well as new feature requests) and contributions are welcome!

## Code Style

ExpOven use [blue](https://github.com/grantjenks/blue) as formatter. Please run following lines before creating the pull request.

```bash
cd ExpOven
blue .
```

## Architecture

<center><img src="./arch_figure.png" width=30%></center>

In order to support other backends, class `ExpInfo` and class `NotifierBackend` should be inherited and implemented. (There is a special `LogInfo` class which can be regarded as a simplified version of `ExpInfo`.)

The APIs needed to be (or can be) implemented are commented in the code. Follow the existing code and the comments in DingTalk backends to implement the new backend.
