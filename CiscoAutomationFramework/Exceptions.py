import paramiko


class CiscoAutomationFrameworkException(Exception):
    """
    Base exception for all custom exceptions raised by CiscoAutomationFramework.
    """
    pass


class EnablePasswordError(CiscoAutomationFrameworkException):
    """
    Raised when entering privileged exec mode fails due to an enable password issue.
    """
    pass


class ParserError(CiscoAutomationFrameworkException):
    """
    Raised when an output parser encounters unexpected or unparseable data.
    """
    pass


class ForbiddenError(CiscoAutomationFrameworkException):
    """
    Raised when a forbidden command is issued to a read-only transport engine.
    """
    pass


class AuthenticationException(CiscoAutomationFrameworkException, paramiko.AuthenticationException):
    """
    Base exception for all authentication and authorization failures within the framework.

    Inherits from both :exc:`CiscoAutomationFrameworkException` and :exc:`paramiko.AuthenticationException`
    to ensure complete backwards compatibility with scripts catching either exception type.
    """
    pass


class JumpHostAuthenticationException(AuthenticationException):
    """
    Raised when authentication fails against the Linux SSH Jump Host (bastion server).

    :param message: Human-readable error message explaining the failure
    :type message: str
    :param jumphost: The JumpHost object representing the bastion server that rejected credentials
    :type jumphost: JumpHost
    """
    def __init__(self, message=None, jumphost=None):
        self.jumphost = jumphost
        if message is None and jumphost:
            message = f"Authentication failed on jump host '{jumphost.username}@{jumphost.ip}:{jumphost.port}'"
        super().__init__(message)


class DeviceAuthenticationException(AuthenticationException):
    """
    Raised when authentication or authorization fails against the target network device.

    :param message: Human-readable error message explaining the failure
    :type message: str
    :param ip: The IP address or hostname of the network device
    :type ip: str
    :param username: The username used when attempting authentication
    :type username: str
    """
    def __init__(self, message=None, ip=None, username=None):
        self.ip = ip
        self.username = username
        if message is None and ip:
            user_part = f" for user '{username}'" if username else ""
            message = f"Authentication failed on network device '{ip}'{user_part}"
        super().__init__(message)


class JumpHostConnectionException(CiscoAutomationFrameworkException):
    """
    Raised when establishing a network connection to the jump host fails (e.g. timeout, connection refused).

    :param message: Human-readable error message explaining the failure
    :type message: str
    :param jumphost: The JumpHost object representing the bastion server
    :type jumphost: JumpHost
    """
    def __init__(self, message=None, jumphost=None):
        self.jumphost = jumphost
        if message is None and jumphost:
            message = f"Failed to connect to jump host '{jumphost.ip}:{jumphost.port}'"
        super().__init__(message)


class JumpHostTunnelException(CiscoAutomationFrameworkException):
    """
    Raised when opening a direct-tcpip forwarding channel through the jump host fails
    (e.g. destination unreachable from jump host or AllowTcpForwarding disabled in sshd_config).

    :param message: Human-readable error message explaining the failure
    :type message: str
    :param jumphost: The JumpHost object representing the bastion server
    :type jumphost: JumpHost
    :param dest_ip: The target device IP
    :type dest_ip: str
    :param dest_port: The target device port (default 22)
    :type dest_port: int
    """
    def __init__(self, message=None, jumphost=None, dest_ip=None, dest_port=22):
        self.jumphost = jumphost
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        if message is None and jumphost and dest_ip:
            message = f"Failed to open direct-tcpip channel through jump host '{jumphost.ip}' to '{dest_ip}:{dest_port}'"
        super().__init__(message)
