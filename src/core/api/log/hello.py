import paramiko
import os
import socket


class CheungSSHFileTransfer(object):
    def __init__(self):
        pass

    def login(self, ip='', username='', password='', port=22, login_method='', keyfile='', keyfile_password="", **kws):
        self.username = username
        self.owner = kws['owner']
        self.password = password
        self.port = port
        self.login_method = login_method
        self.ip = ip
        self.keyfile = os.path.join(cheungssh_settings.keyfile_dir, self.owner, keyfile)
        self.port = port

        self.keyfile_password = keyfile_password
        cheungssh_info = {"status": False, "content": ""}
        try:
            ssh = paramiko.Transport((self.ip, int(self.port)))
            if login_method == "PASSWORD":
                ssh.connect(username=self.username, password=self.password)
            # else:
            #
            #     if len(self.keyfile_password) > 0 and not self.keyfile_password == "******":
            #         key = paramiko.RSAKey.from_private_key_file(self.keyfile, password=self.keyfile_password)
            #
            #     else:
            #         key = paramiko.RSAKey.from_private_key_file(self.keyfile)
            #     ssh.connect(username=username, pkey=key)
            sftp = paramiko.SFTPClient.from_transport(ssh)
            self.ssh = ssh
            self.sftp = sftp
            self.get_username_to_uid()
            self.get_groupname_to_gid()
            cheungssh_info["status"] = True
        except socket.error:
            cheungssh_info["content"] = "连接错误"
        except socket.timeout:
            pass

    def download(self, remote_file='', local_file='', tid=""):
        transfer_type = "download"
        self.transfer_type = "download"
        cheungssh_info = {"status": False, "content": ""}
        try:
            _local_file = os.path.basename(local_file)
            local_file = os.path.join(cheungssh_settings.download_dir, _local_file)

            if os.path.isfile(local_file): local_file = "%s_%s" % (local_file, self.ip)
            try:
                self.sftp.listdir(remote_file)

            except Exception as  e:
                print(e)
            try:
                data = {"tid": tid, "content": "", "status": True}
                callback = functools.partial(self.set_progress, data)
                self.sftp.get(remote_file, local_file, callback=callback)
                cheungssh_info["remote_file"] = remote_file
                cheungssh_info["local_file"] = local_file
                cheungssh_info["transfer_type"] = transfer_type
                cheungssh_info["tid"] = tid
                cheungssh_info["progress"] = 0
                cheungssh_info["status"] = True
            except Exception as e:
                print(e)
                # if e == 2:
                #     raise CheungSSHError("源文件[%s]不存在" % remote_file)
                # else:
                #     raise IOError(str(e))

        except Exception as e:
            if hasattr(e, "errno"):
                if e.errno is None:
                    cheungssh_info["content"] = "指定的源文件路径不存在"
            else:
                cheungssh_info["content"] = str(e)
            cheungssh_info["status"] = False
            cheungssh_info["tid"] = tid

    def get_filecontent(self, filename):
        cheungssh_info = {"content": "", "status": False}
        try:
            a = self.sftp.open(filename)
            content = "".join(a.readlines())
            cheungssh_info["content"] = content
            a.close()
            cheungssh_info["status"] = True
        except Exception as e:
            cheungssh_info["status"] = False
            cheungssh_info["content"] = str(e)
        return cheungssh_info

    def write_filecontent(self, filename, content):
        cheungssh_info = {"content": "", "status": False}
        try:
            a = self.sftp.open(filename, "w")
            a.write(content)
            a.close()
            cheungssh_info["status"] = True
        except Exception as e:
            cheungssh_info["status"] = False
            cheungssh_info["content"] = str(e)
        return cheungssh_info

    def __del__(self):
        self.logout()
