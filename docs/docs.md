# Document

![](./arch_figure.png)

In order to support other backends, class `ExpInfo` and class `NotifierBackend` should be inherited and implemented. (There is a special `LogInfo` class which can be regarded as a simplified version of `ExpInfo`.)

The APIs needed to be (or can be) implemented are commented in the code. Follow the existing code and the comments in DingTalk backends to implement the new backend.