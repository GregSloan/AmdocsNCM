import paramiko
from cloudshell.helpers.scripts import cloudshell_scripts_helpers as helper
import re

def _ssh_write(ssh, channel, command):

    channel.send(command)



def _ssh_read(ssh, channel, prompt_regex):

    rv = ''

    while True:
        # self.channel.settimeout(30)

        r = channel.recv(2048)

        if r:
            rv += r
        if rv:
            t = rv
            t = re.sub(r'(\x9b|\x1b)[[?;0-9]*[a-zA-Z]', '', t)
            t = re.sub(r'(\x9b|\x1b)[>=]', '', t)
            t = re.sub('.\b', '', t)  # not r''
        else:
            t = ''
        if not r or len(re.findall(prompt_regex, t)) > 0:
            rv = t
            if rv:
                rv = rv.replace('\r', '\n')

            return rv


def _ssh_command(ssh, channel, command, prompt_regex):

    _ssh_write( ssh, channel, command + '\n')
    rv = _ssh_read( ssh, channel, prompt_regex)
    if '\n%' in rv.replace('\r', '\n'):
        es = 'CLI error message: ' + rv

        raise Exception(es)
    return rv

resource_context = helper.get_resource_context_details()
session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
session.connect(resource_context.address, 22, 'root','amdocs')

channel = session.invoke_shell()
prompt = '.*]#'
_ssh_command(session, channel, 'mkdir -p /stage', prompt)
_ssh_command(session, channel, 'scp root@10.53.212.103:/stage/BSR9.9/bms/* /stage/', '.*yes/no.*')
_ssh_command(session, channel, 'yes','.*password.*')
_ssh_command(session, channel, 'amdocs','.*]#')
_ssh_command(session, channel, 'scp root@10.53.212.105:/stage/iso/* /stage/','.*password.*')
_ssh_command(session, channel, 'amdocs', '.*]#')

