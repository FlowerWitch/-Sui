#新增输出备案单位

import random
import re
import requests
import fake_useragent
import time
import argparse
import csv

r="\033[1;31m"
ret="\033[1;0m"

def get_argparser():
    parser = argparse.ArgumentParser(description="Power by ❀flower❀")
    parser.add_argument("-t",dest="target",help="Url or SuDomain Misc List Filename",required=True)
    parser.add_argument("-o",dest="output",help="output .csv filename",action="store")
    return parser.parse_args()

def suDomain_query(domain):
    if not (domain.find("com.cn") >= 0 or domain.find("org.cn")  >= 0 or domain.find("net.cn")  >= 0  or domain.find("edu.cn") >= 0 ) :
        return True
    else:
        return False

def Domain_push(domain_file):
    domain_addlist = []
    ra = r'([^\.:\d/]+\.[^\./]+\.?[^\.:/]*)'
    with open(domain_file,"r") as r :
        a = r.readlines()
    for i in a:
        ma = re.findall(ra,i[::-1])
        domain = ma[0][::-1].replace("\n","")
        if suDomain_query(domain):
            h_domain=".".join(domain[::-1].split(".")[0:2])[::-1]
            domain_addlist.append(h_domain)
        else:
            domain_addlist.append(domain)
    print("[^]Domain Push\n")
    print("Domain Length: "+str(len(domain_addlist)))
    dis_domain = set(domain_addlist)
    print("Distinct domain: "+str(len(dis_domain)))
    return dis_domain

def get_weight_list(domain):
    temp_weight_ls=[]
    weight_dict={"baidu"  : f"https://baidurank.aizhan.com/api/br?domain={domain}&style=text",
    "baidum" : f"https://baidurank.aizhan.com/api/mbr?domain={domain}&style=text",
    "sorank" : f"https://sorank.aizhan.com/api/br?domain={domain}&style=text",
    # "smrank" : f"https://smrank.aizhan.com/api/br?domain={domain}&style=text",
    "sougou" : f"https://sogourank.aizhan.com/api/br?domain={domain}&style=text",
    "googlepr" : f"https://pr.aizhan.com/{domain}/",
    "organizer":f"https://icp.aizhan.com/{domain}/"}
    flower_magic = fake_useragent.UserAgent().random
    header ={"User-Agent":flower_magic}
    ICP_header = {"User-Agent": flower_magic, "Referer": "https://dns.aizhan.com/"}
    pattern = r'>(\d+)<'
    pr_pattern = r'pr.(\d+).png'
    #icp_pattern = r'>(.+)-企业信息</h4>'
    icp_pattern = r'>(.+) &nbsp;&nbsp; 企业</p>'
    for n,url in weight_dict.items():
        time.sleep(random.uniform(0.2,0.5))
        if n == "googlepr":
            req = requests.get(url, headers=header)
            temp_weight_ls.append(re.search(pr_pattern,req.text).groups(0)[0])
        elif n == "organizer":
            try:
                req = requests.get(url,headers=ICP_header)
                a=req.text
                temp_weight_ls.append(re.search(icp_pattern,a).groups(0)[0])
            except Exception as e:
                temp_weight_ls.append("未备案")
        else:
            req=requests.get(url,headers=header)
            # print(req.text)
            temp_weight_ls.append(re.search(pattern,req.text).groups(0)[0])
    return temp_weight_ls

def weight_print(domain,weight_name,output=False):
    # domain="test.com"
    r_pt=""
    mattch_ls = get_weight_list(domain)
    r_pt+="Domain: "+domain+"|"
    for i in range(len(mattch_ls)-1):
        pt = weight_name[i]+":"+mattch_ls[i]
        rpt = r+pt+ret
        if i < 4 and int(mattch_ls[i]) >= 1:
            r_pt+=(rpt+"|")
        elif int(mattch_ls[i]) >= 3:
            r_pt+=(rpt+"|")
        else:
            r_pt+=(ret+pt+"|")
    r_pt+=weight_name[-1]+":"+mattch_ls[-1]
    o_pt = r_pt + ret
    print(o_pt)
    if output:
        csv_pt_list = [j.replace(" ","").split(":")[1] for j in ([i.replace(r,"").replace(ret,"") for i in o_pt.split("|")][0:])]
        with open(f'{output}.csv', 'a', newline='') as co_file:
            writer = csv.writer(co_file)
            writer.writerow(csv_pt_list)

def main():
    # weight_name = ["Domain","百度权重", "移动权重", "360", "神马", "搜狗", "谷歌PR"]
    weight_name = ["Domain","百度权重", "移动权重", "360", "搜狗", "谷歌PR","备案单位"]
    args = get_argparser()
    if args.output:
        with open(f'{args.output}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(weight_name)
    domain_list = Domain_push(args.target)
    # domain_list = Domain_push("list1")
    for i in domain_list:
        print("--")
        time.sleep(0.3)
        weight_print(i,weight_name[1:],output=args.output)

if __name__ == "__main__":
    main()
