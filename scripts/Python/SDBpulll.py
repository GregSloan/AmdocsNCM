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
reservation_context = helper.get_reservation_context_details()
res_id = reservation_context.id
api = helper.get_api_session()
session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
session.connect(resource_context.address, 22, 'root','amdocs')

channel = session.invoke_shell()
prompt = '.*]#'
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending command "mkdir -p /stage"')
_ssh_command(session, channel, 'mkdir -p /stage', prompt)
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending command "scp root@10.53.212.107:/stage/BSR9.9/sdb/* /stage/"')
_ssh_command(session, channel, 'scp root@10.53.212.107:/stage/BSR9.9/sdb/* /stage/', '.*yes/no.*')
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending "yes"')
_ssh_command(session, channel, 'yes','.*password.*')
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending password "*****"')
_ssh_command(session, channel, 'amdocs','.*]#')
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending command "scp root@10.53.212.105:/stage/iso/* /stage/"')
_ssh_command(session, channel, 'scp root@10.53.212.105:/stage/iso/* /stage/', '.*yes/no.*')
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending "yes"')
_ssh_command(session, channel, 'yes','.*password.*')
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
api.WriteMessageToReservationOutput(res_id, resource_context.name + ' sending password "*****"')
_ssh_command(session, channel, 'amdocs', '.*]#')
api.WriteMessageToReservationOutput(res_id, resource_context.name + '  --previous command complete')
