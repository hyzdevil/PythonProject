def str_methods():
    # string = "hello world\nasdfg"
    string = "hello"
    # print(string.zfill(6)) # 若字符串总长度小于所填参数，则在字符串的左侧填充0；否则不改变字符串
    # print(string.capitalize()) # 将字符串的首字母变为大写
    # print(string.swapcase()) # 将字符串的大小写相互转换
    # print(string.title())# 将字符串的每个单词的首字母变为大写，单词以空格分隔
    # print(string.upper()) # 将字符串全部变为大写
    # print(string.lower()) # 将字符串全部变为小写
    # print(string.strip()) # 删除字符串的左右空格
    # print(string.rstrip()) # 删除字符串的右边空格
    # print(string.lstrip()) # 删除字符串的左边空格
    # print(string.startswith("he")) # 判断字符串是否以给定字符串开头，返回值为布尔类型
    # print(string.endswith()) # 判断字符串是否以给定字符串结尾，返回值为布尔类型
    # print(string.splitlines()) # 将字符串以换行符分割，返回一个列表
    # print(string.split(" ")) # 将字符串以给定字符分割，返回一个列表
    # print(string.rsplit("o")) # 将字符串以给定字符分割，从右边开始，返回一个列表
    # print(string.rpartition("d")) # 将字符串以给定字符分割，从右边数第一个，返回一个列表
    # print(string.ljust(6,"0")) # 若字符串总长度小于所填参数，则在字符串的右侧填充给定字符，默认为空格；
    # print(string.rjust(8,"0")) # 若字符串总长度小于所填参数，则在字符串的左侧填充给定字符，默认为空格；
    # print(string.rindex("d")) # 返回右侧数第一个匹配的字符串的索引，没有找到则报错
    # print(string.rfind("l")) # 返回右侧数第一个匹配的字符串的索引，没有找到则返回-1
    # print(string.replace("o","s")) # 替换字符串，
    # print(string.partition("l")) # 返回以给定字符串分割的元组，(分隔符之前的字符串, 分隔符本身, 分隔符之后的字符串)
                                # 若找不到分割符则返回字符串本身和两个空字符串
    # print(string.center(11,"0")) # 若字符串总长度小于所填参数，则在字符串的两侧填充给定字符；否则不改变字符串
    # print(string.count("l")) # 统计给定字符串的出现次数
    # print(string.encode()) # 将字符串编码并返回，默认以utf8编码
    # print(string.find()) # 返回给定字符串的索引，找不到索引则返回-1
    # print(string.index()) # 返回给定字符串的索引，找不到索引则报错
    # print("asdfgh{}".format(12)) # 字符串格式化函数
    # print("qwe{name},{age}".format_map({"name":"王五", "age":10}))# 替换格式化函数
    # print(string.isalnum()) # 如果字符串至少有一个字符且都是字母或数字则返回True,否则返回False
    # print(string.isalpha()) # 如果字符串至少有一个字符且都是字母则返回True,否则返回False
    # print(string.isdecimal()) # 如果字符串只包含十进制数字则返回 True 否则返回 False.
    # print("123546".isdigit()) # 如果字符串只包含数字则返回 True 否则返回 False.
    # print(string.isupper()) # 判断字符是否都是大写
    # print(string.islower()) # 判断字符是否都是小写
    # print("123456".isnumeric()) # 如果字符串只包含数字则返回 True 否则返回 False.
    # print(string.isspace()) # 判断字符是否是空格
    # print(string.isidentifier()) # 判断字符串是否是一个有效的标识符
    # print(string.isprintable()) # 判断字符串是否是能被打印出来的
    # print("Hello World".istitle()) # 判断所有单词是否首字母大写
    # print(string.join("world")) # 将字符串添加到给定可迭代字符串的元素之间
    # print(string.translate())
    print("hello".maketrans({"1":"b"}))
    # print(string.casefold())
    # print(string.expandtabs())
    # print(string.isascii())

if __name__ == '__main__':
    str_methods()
