import re
from datetime import datetime


def verify_birthday(birthday):
    if len(birthday) == 6:
        birthday = "19" + birthday
        try:
            datetime.strptime(birthday, "%Y%m%d")
            return True
        except Exception as e:
            return False


def checkIdcard(idcard):
    """

    :param idcard:身份证号
    :return: 成功返回： 省份、生日、性别
            失败返回： 失败结果与信息
    """
    ret = {"code": 0, "msg": ""}
    Errors = ['验证通过！', '身份证号码位数不对', '身份证号码出生日期超出范围或含有非法字符', '身份证号码校验错误', '身份证地区非法']
    area = {"11": "北京", "12", "天津"}
    idcard = str(idcard)
    idcard_list = list(idcard)

    # 地区校验
    if not area[idcard[0:2]]:
        ret["msg"] = Errors[4]
        return ret

    """
    15位身份证号码检测
    1-2位 省、自治区、直辖市代码；
    3-4位地级市、盟、自治州代码；
    5-6位 县、县级市、区代码；
    7-12位 出生年月
    13-15位为顺序号，其中15位男为单数 女为双数
    
    
    18位身份证号码检测
    排列顺序从左到右依次为 六位数字地址码、八位数字出生日期码、三位数字顺序码、最后一位是数字校验码
    1、将前面的身分证号码17位数分别乘以不同的系数。从第一位到第17位的系数分别为 7、9、10、5、8、4、2、1、6、3、7、9、10、5、8、4、2；
    2、将这17位数字和系统相乘的结果相加；
    3、用加出来的和 除以11 看余数是多少；
    4、余数只可能有 0，1，2，3，4，5，6，7，8，9，10 这11个数字。其分别对应的最后一位身份证的号码为 10，X、9、8、7、6、5、4、3、2
    5、通过上面得知如果余数为2，就会在身份证的第18位数字上出现x
    """
    if len(idcard) == 15:
        verify_re = re.compile('\d{15}$')
        if re.match(verify_re, idcard):
            if verify_birthday(idcard[6:12]):
                ret["code"] = 1
                ret["msg"] = Errors[0]
            else:
                ret["msg"] = Errors[2]

        else:
            ret["msg"] = Errors[2]
    elif len(idcard) == 18:
        verify_re = re.compile('\d{17}[0-9|X]$')
        if re.match(verify_re, idcard):
            if verify_birthday(idcard[6:14]):
                # 计算校验位

                S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + \
                    (int(idcard_list[1]) + int(idcard_list[11])) * 9 + \
                    (int(idcard_list[2]) + int(idcard_list[12])) * 10 + \
                    (int(idcard_list[3]) + int(idcard_list[13])) * 5 + \
                    (int(idcard_list[4]) + int(idcard_list[14])) * 8 + \
                    (int(idcard_list[5]) + int(idcard_list[15])) * 4 + \
                    (int(idcard_list[6]) + int(idcard_list[16])) * 2 + \
                    int(idcard_list[7]) * 1 + \
                    int(idcard_list[8]) * 6 + \
                    int(idcard_list[9]) * 3
                Y = S % 11
                JYM ="10X98765432"
                M = JYM[Y]
                if M == idcard_list[17]:
                    ret["code"]=1
                    ret["msg"]=Errors[0]

                else:
                    ret["msg"] = Errors[3]
            else:
                ret
