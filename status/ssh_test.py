from paramiko import SSHClient, BadHostKeyException, AuthenticationException, SSHException, AutoAddPolicy
import socket
def test_ssh(id, token):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    port = 2200+int(id)
    print(port)
    try:
        ssh.connect(hostname='localhost', username='status', password=token, port=port)
        print('OK')
        ssh.close()
        return True
    except (BadHostKeyException, AuthenticationException,
            SSHException, socket.error) as e:
        print('SSH error')
        return False