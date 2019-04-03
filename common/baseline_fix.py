import getopt
import os
import re
import sys

from requests_file import FileAdapter
from requests_html import HTMLSession


class GenFixScript():
    def __init__(self,ip_addr,baseline_type="OS",base_dir="/opt/apache-tomcat-8.5.35"):
        # self.parse_argv(argv)
        session = HTMLSession()
        session.mount('file://', FileAdapter())
        # Windows系统路径目录分隔符为反斜杠，但get需要正斜杠所以先进行一下替换
        pwd = os.getcwd().replace("\\","/")
        # 测试发现使用相对路径读不到文件，需要使用绝对路径
        baseline_type = baseline_type.lower()

        self.ip_addr = ip_addr
        self.baseline_type = baseline_type
        self.base_dir = base_dir
        # ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
        # full_reg = f"{ip_reg}_{baseline_type}\.html"
        # pwd_file_list = os.listdir()
        # for file in pwd_file_list:
        #     if re.search(full_reg,file):
        #         ip_addr = re.search(ip_reg,file).group()
        self.html_obj = session.get(f'file:///{pwd}/../4_report/{ip_addr}_{baseline_type}_report.html')
        self.shell_script_obj = open(f"../6_fix/{ip_addr}_{baseline_type}_fix.sh","w+",encoding='utf-8',newline='\n')
        self.fix_item_list={}
        # self.gen_shell_script_head_part()

#     def usage(self):
#         print(f"""
# Usage:
#   -h, --help        display this help and exit
#
#   example: python3 {self.baseline_type}_baseline_fix.py
#         """)
#
#     def parse_argv(self,argv):
#         opts, args = getopt.getopt(argv, "h", ["help", ])
#         for opt, arg in opts:
#             # -h与--help等价
#             if opt in ("-h", "--help"):
#                 self.usage()
#                 sys.exit()
    def node_xpath(self,obj,xpath_pattern):
        try:
            node = obj.xpath(xpath_pattern)
        except:
            node = None
        return node

    def text_xpath(self,obj,xpath_pattern):
        try:
            text = obj.xpath(xpath_pattern)[0].text.strip()
        except:
            text = ""
        return text

    def gen_shell_script_head_part(self):
        self.shell_script_obj.writelines("""#!/bin/bash
xml_file_name='/tmp/""" + self.ip_addr+"_"+self.baseline_type + """_fix.log'
CATALINA_HOME='""" + self.base_dir + """'
id=0

createReportXml(){
    echo '<?xml version="1.0" encoding="UTF-8"?>' > $xml_file_name
    echo '<root>' >> $xml_file_name
}
closeReportXml(){
    echo '</root>' >> $xml_file_name
}
createChecklist(){
    echo -e "\\t<checklist>" >> $xml_file_name
}
closeChecklist(){
    echo -e "\\t</checklist>" >> $xml_file_name
}
createSection(){
    echo -e "\\t\\t<section id=\"$1\">" >> $xml_file_name
}
closeSection(){
    echo -e "\\t\\t</section>" >> $xml_file_name
}
createNode(){
    echo -e "\\t\\t\\t<node id=\"$1\">" >> $xml_file_name
}
closeNode(){
    echo -e "\\t\\t\\t</node>" >> $xml_file_name
}

# 各检测项生成报告函数
appendToXml(){
    echo -e "\\t<item id="\"$id\"">" >> $xml_file_name
    echo -e "\\t\\t<fix_time>$(date  +'%Y-%m-%d 星期%w %H:%M:%S')</fix_time>" >> $xml_file_name
    echo -e "\\t\\t<fix_object>$1</fix_object>" >> $xml_file_name
    echo -e "\\t\\t<fix_command>$2</fix_command>" >> $xml_file_name
    echo -e "\\t\\t<fix_comment>$3</fix_comment>" >> $xml_file_name
    echo -e "\\t\\t<fix_result>$4</fix_result>" >> $xml_file_name
    echo -e "\\t</item>" >> $xml_file_name
    id=`expr $id + 1`
}

# 用于通过传输过来的文件与正则查找匹配
searchValueByReg(){
    file_name=$1
    regexp=$2
    found_flag="0"
    if ! [ -e $file_name ]
    then
        echo "file $file_name not found"
        return 1
    fi
    while read line
    do
        result=`echo $line | grep -E $regexp`
        if [ -n "$result" ]
        then
            found_flag="1"
            echo "$result"
            break
        fi
    done <<< "$(cat $file_name)"
    if [ $found_flag == "0" ]
    then
        echo "not found"
    fi
}
            """)

    def gen_no_need_fix_info(self):
        self.shell_script_obj.writelines("""
noNeedFixInfo(){
    echo "there is not any item need to 6_fix"
}
        """)

    def gen_shell_script_tail_part(self):
        if len(self.fix_item_list) == 0:
            self.gen_no_need_fix_info()
            self.shell_script_obj.writelines("""
main(){
    main_pre $@
    createReportXml
""")
            self.shell_script_obj.writelines("""\t\tnoNeedFixInfo\n""")
        else:
            self.shell_script_obj.writelines("""
main(){
    main_pre $@
    createReportXml
""")
            for k, v in self.fix_item_list.items():
                self.shell_script_obj.writelines(f"""\t\t{v}\n""")
        self.shell_script_obj.writelines("""\tcloseReportXml\n}\n\nmain $@\n""")
        pass

    # def __del__(self):
    #     self.gen_shell_script_tail_part()