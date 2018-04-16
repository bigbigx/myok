import CheungSSHFileTransfer

@staticmethod
def remote_file_content(super, username, id, action, file_content=""):
    cheungssh_info = {"status": False, "content": ""}
    try:
        data = RemoteFileAdmin.get_remote_file_list(super, username)
        if not data["status"]: raise CheungSSHError(data["content"])
        content = data["content"]
        try:
            if not content[id]["owner"] == username: CheungSSHError("您无权查看该资源！")
        except KeyError:
            raise CheungSSHError("您指定的资源不存在！")
        path = content[id]["path"]
        path = re.sub(" ", "", path)
        sid = content[id]["server"]
        host_info = CheungSSHControler.convert_id_to_ip(sid)
        if not host_info["status"]: raise CheungSSHError(host_info["content"])
        host = host_info["content"]
        sftp = CheungSSHFileTransfer()
        login = sftp.login(**host)
        if not login["status"]: raise CheungSSHError(login["content"])
        if action == "GET":
            cheungssh_info = sftp.get_filecontent(path)
        elif action == "WRITE":
            cheungssh_info = sftp.write_filecontent(path, file_content)
        else:
            raise CheungSSHError("CHB0000000024")
    except Exception, e:
        cheungssh_info["status"] = False
        cheungssh_info["content"] = str(e)
    return cheungssh_info