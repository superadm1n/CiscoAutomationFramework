'''
Copyright 2021 Kyle Kowalczyk

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
from CiscoAutomationFramework.IOS import IOS


class IOSXE(IOS):
    """Because IOS and IOSXE are so similar from the CLI, I chose to inherit all methods and attributes
    from the IOS class. If it is determined that a method does not behave as expected it can be overrode
    here. This eliminates duplication of code for both firmware types."""
    pass