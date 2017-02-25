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
_ssh_command(session, channel, 'cd /stage', prompt)
_ssh_command(session, channel, 'mkdir -p /var/www/html/cdrom/iso', prompt)
_ssh_command(session, channel, 'mount -o loop /stage/rhel-server-5.8-x86_64-dvd.iso /var/www/html/cdrom/iso', prompt)
_ssh_command(session, channel, 'rpm --import /var/www/html/cdrom/iso/RPM-GPG-KEY-redhat-release',prompt)
_ssh_command(session, channel, 'yum install deltarpm-3.5+0.5.20090913git.e16.x86_64.rpm python-deltarpm-3.5-0.5.20090913git.e16.x86)64.rpm','.*y/N.*')
_ssh_command(session, channel, 'y', prompt)
_ssh_command(session, channel, 'rpm -i /var/www/html/cdrom/iso/Packages/createrepo*.noarch.rpm', prompt)
_ssh_command(session, channel, 'cd /var/www/html/cdrom', prompt)
_ssh_command(session, channel, 'createrepo .', prompt)
_ssh_command(session, channel, 'rm -rf /etc/yum.repos.d/rhel-source.repo', prompt)
_ssh_command(session, channel, 'echo [RHEL-Repository] > /etc/yum.repos.d/file.repo', prompt)
_ssh_command(session, channel, 'echo name=RHEL repository >>  /etc/yum.repos.d/file.repo', prompt)
_ssh_command(session, channel, 'echo baseurl=file:///var/www/html/cdrom >> /etc/yum.repos.d/file.repo', prompt)
_ssh_command(session, channel, 'echo enabled=1 >> /etc/yum.repos.d/file.repo', prompt)
_ssh_command(session, channel, 'echo gpgcheck=0 >> /etc/yum.repos.d/file.repo', prompt)

_ssh_command(session, channel, 'yum clean all', prompt)


