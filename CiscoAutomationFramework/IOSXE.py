from CiscoAutomationFramework.IOS import IOS


class IOSXE(IOS):
    """Because IOS and IOSXE are so similar from the CLI, I chose to inherit all methods and attributes
    from the IOS class. If it is determined that a method does not behave as expected it can be overrode
    here. This eliminates duplication of code for both firmware types."""
    pass