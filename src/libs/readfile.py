#coding:utf-8
'''

'''

def readfile():
        # filename ='/root/myok/src/libs/business.txt'
        filename = 'D:\\devops\\myok\\src\\libs\\business.txt'
        # exmail_addr = []
        # user_name = []
        result_inner = {'mail': '', 'username': ''}
        result = []
        with open(filename, 'r', encoding='utf8') as file_to_read:

            lines = file_to_read.readlines()
            # print(lines)
            for  line in lines:
                line = line.rstrip('\\n')
                # print(line)

                result_inner['mail'] = line.split()[0]
                result_inner['username'] = line.split()[1]
                result.append({'mail':result_inner['mail'],'username': result_inner['username']})

        return result

#
# if __name__ == "__main__":
#     print(readfile())