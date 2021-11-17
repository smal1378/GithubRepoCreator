# GithubRepoCreator
A simple python application for creating multiple repository's in GitHub.

## Ver 1.1<br>

---
### Application Modules:
- LogConsole: 
This class is defined in model.py and is added at ver1.1. an object of this class should be created at application 
start and other parts can use this log manager object, creation of this object should be made at 'controller.py'.
<br> API:
  - get_log(count: int): generator function that returns last 'count' logs. each log is a tuple containing \
module name and the message.
  - log(module: str, message: str): this method will add new log to console.
  - attach_callback(callback: Callable): will add the function to callbacks, calls it whenever new log is added.
also return the id of that callback.
  - detach_callback(id: int): will remove the callback from callback list.
- 

