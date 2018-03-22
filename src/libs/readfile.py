#coding:utf-8
'''

'''

def readfile():
        filename ='business.txt'
        exmail_addr = []
        user_name = []
        with open(filename, 'r',encoding='utf8') as file_to_read:
            while True:
                lines = file_to_read.readline()
                if not lines:
                    break
                    pass
                p_tmp, E_tmp = [str(i) for i in lines.split()]
                exmail_addr.append(p_tmp)
                user_name.append(E_tmp)
        return exmail_addr

                # pos = np.array(pos)  # 将数据从list类型转换为array类型。
                # Efield = np.array(Efield)
                # pass



if __name__ == "__main__":
    print(readfile())