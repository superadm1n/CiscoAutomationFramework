from CiscoAutomationFramework import connect_ssh

def custom_error_handler(error_string, last_issued_command):
    """Error handler to simply display the command that was issued and the error string that was returned
    from the device. You could add logic here to correct for the error."""
    print('Error Detected! Command Issued: {}. Error String: {}'.format(last_issued_command, error_string))


ip = '192.168.1.1'
username = 'admin'  # standard user must not login directly to priv exec mode
password = 'password'

# Login with standard user credentials and manually try to issue 'show run' without
# elevating privileges which will trigger the error handler.
with connect_ssh(ip, username, password, error_handler=custom_error_handler) as ssh:
    ssh.transport.send_command_get_output('show run')