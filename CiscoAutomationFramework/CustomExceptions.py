'''
Copyright 2018 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

class MyException(Exception):
    pass

class UserNotValid(MyException):
    pass

class NoHostPingable(MyException):
    pass

class AuthenticationError(MyException):
    pass

class ConnectionError(MyException):
    pass

class InvokeShellError(MyException):
    pass

class OsDetectionFailure(MyException):
    pass

class NoEnablePassword(MyException):
    pass



class SerialException(Exception):
    pass

class UnableToDetermineLocation(SerialException):
    pass

class UsernameOrPasswordNotSupplied(SerialException):
    pass

class LoginFailed(SerialException):
    pass


class CafExceptions(Exception):
    pass

class EngineNotSelected(CafExceptions):
    pass


class MethodNotImplemented(Exception):
    pass

class MethodNotSupported(Exception):
    pass

class NotConfigured(Exception):
    pass