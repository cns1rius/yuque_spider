# @Author: s1rius
# @Date: 2023-07-28 11:08:02
# @LastEditTime: 2023-08-10 17:01:20
# @Description: https://s1rius.space/

import os, re, requests
from time import sleep


# --------------==须填参数==-----------------------
# 语雀参数
headers = {
    "Cookie": "current_theme=default; __wpkreporterwid_=b83fdbaa-fff0-46a8-a4f1-ab5e3170c689; lang=zh-cn; _yuque_session=qUCdVYZG416IHkxIS47HQgu9EVtYTTX-aMz_GnJdCSVMUAGyZd-V3LNrLzlxkyUX3jD-TPWA9W9EbS0oKIWUeQ==; yuque_ctoken=deahv6expl562s37yfzt9hrk6r9gpmx3; _uab_collina=169052628564399948892188; acw_tc=0b68a80a16909454746673515e122855f1eed3c7c89208468fe1e304be3922",
}  # 语雀Cookie
space = "xxxx"  # 空间名 对应xxxx.yuque.com

# 团队参数
group_id = 111111111  # 打开"团队" f12查看网络 找到该url: https://xxxx.yuque.com/api/groups/{group_id}/bookstacks
group_code = "rbxx04"  # "团队"页面url最后面的一串字符 xxx.yuque.com/{group_code}

# 文库参数
sign_list = [
    "guxxne",
    "wlxx4z",
    "ecxxy9",
    "ucxx4o",
    "hsxxyo",
    "ukxxhs",
    "qcxxv4",
    "pvxx3o",
    "taxxuh",
]  # 需要爬取的库code
# ----------------==end==-------------------------

id_list = []  # 库参数
dir_list = []  # 库名对应文件夹名

book_dict = {}
dir_dict = {}  # 临时做筛选用

list_url = f"https://{space}.yuque.com/api/groups/{group_id}/bookstacks"  # 获取库列表
list_id = requests.get(list_url, headers=headers).json()
for books in list_id["data"][0]["books"]:
    book_dict.update({f'{books["slug"]}': f'{books["id"]}'})
    dir_dict.update({f'{books["slug"]}': f'{books["name"]}'})
for sign in sign_list:
    id_list.append(book_dict.get(sign))
    dir_list.append(dir_dict.get(sign))  # 库

print(id_list, dir_list)

for i in range(len(id_list)):
    slug_list = []
    title_list = []

    url = f"https://{space}.yuque.com/api/docs?book_id={id_list[i]}"
    print(url)
    list_res = requests.get(url, headers=headers).json()
    for data in list_res["data"]:
        slug = data["slug"]
        title = data["title"]
        slug_list.append(slug)
        title_list.append(title)  # 文件参数

    print(slug_list, title_list)

    if os.path.exists(f"markdown/{dir_list[i]}"):
        pass
    else:
        os.mkdir(f"markdown/{dir_list[i]}")

    for j in range(len(slug_list)):
        name = re.sub(
            r"\/|\"|\'|\\|\|", "_", title_list[j]
        )  # 将无法当作文件名的特殊替换为"_" 遇到其他特殊字符时在此处添加正则

        if os.path.exists(f"./markdown/{dir_list[i]}/{name}.md"):
            break
        else:
            md_url = f"https://{space}.yuque.com/{group_code}/{sign_list[i]}/{slug_list[j]}/markdown?attachment=true&latexcode=false&anchor=false&linebreak=false"
            print(md_url)
            md = requests.get(md_url, headers=headers).text
            print(name)

            f = open(
                f"./markdown/{dir_list[i]}/{name}.md",
                "w",
                encoding="utf-8",
            )
            f.write(md)
            f.close()  # 文件内容
            sleep(3)
