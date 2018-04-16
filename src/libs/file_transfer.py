


def  get_remote_file_list():
    pass



def get_file(action):
    sftp = CheungSSHFileTransfer()
    if action == "GET":
        cheungssh_info = sftp.get_filecontent(path)
    elif action == "WRITE":
        cheungssh_info = sftp.write_filecontent(path, file_content)
    else:
        raise CheungSSHError("CHB0000000024")