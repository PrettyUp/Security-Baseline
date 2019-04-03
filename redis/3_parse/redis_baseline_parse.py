import os
import re
from lxml import html
import html
import lxml
import sys
sys.path.append('../../')
from common.baseline_parse import BaselineParse
from common.baseline_param_parse import BaselineParamParse


class GenRedisHtmlReport(BaselineParse):
    def __init__(self,ip_addr):
        baseline_type = "Redis"
        super().__init__(ip_addr,baseline_type)

    # 为redis设置密码
    def gen_html_report_RedisPassword_section(self):
        accordion_id = "accordion1"
        accordion_title = "为redis设置密码"
        collapse_id = "collapse1"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkRedisPassword']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")
        if "not found" not in check_result:
            card_class = "bg-success text-white"
            self.config_right += 1
        else:
            card_class = "bg-danger text-white"
            self.config_error += 1
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="RedisPassword_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 禁用高危命令FLUSHALL、FLUSHDB、KEYS
    def gen_html_report_RedisDangerCommand_section(self):
        accordion_id = "accordion2"
        accordion_title = "禁用高危命令FLUSHALL、FLUSHDB、KEYS"
        collapse_id = "collapse2"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkRedisDangerCommand']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")
        if "FLUSHALL" in check_result and "FLUSHDB" in check_result and "KEYS" in check_result:
            card_class = "bg-success text-white"
            self.config_right += 1
        else:
            card_class = "bg-danger text-white"
            self.config_error += 1
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="RedisPassword_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 建议只监听本地地址
    def gen_html_report_RedisAddress_section(self):
        accordion_id = "accordion3"
        accordion_title = "建议只监听本地地址"
        collapse_id = "collapse3"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkRedisAddress']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")
        regexp = "^\s*bind\s*127.0.0.1\s*$"
        if re.search(regexp,check_result) is not None:
            card_class = "bg-success text-white"
            self.config_right += 1
        else:
            card_class = "bg-warning text-white"
            self.config_warn += 1
            check_result = ""
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="RedisAddress_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 禁止以root用户运行
    def gen_html_report_RedisRunner_section(self):
        accordion_id = "accordion4"
        accordion_title = "禁止以root用户运行"
        collapse_id = "collapse4"

        current_item=self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkRedisRunner']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")
        if check_result.split()[0] != "root":
            card_class = "bg-success text-white"
            self.config_right += 1
        else:
            card_class = "bg-warning text-white"
            self.config_warn += 1
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="RedisRunner_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 确认redis是最新版本
    def gen_html_report_RedisVersion_section(self):
        accordion_id = "accordion5"
        accordion_title = "确认redis是最新版本"
        collapse_id = "collapse5"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkRedisVersion']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")

        card_class = "bg-warning text-white"
        self.config_warn += 1

        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="RedisVersion_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)


    # 这里只需要调用自己生成各检测项报告的函数即可
    # 头部已由在__init__()中调用super().__init()生成
    # 尾部已由在__del__()中调用super().__del__()生成
    def gen_html_report(self):
        self.gen_html_report_RedisPassword_section()
        self.gen_html_report_RedisDangerCommand_section()
        self.gen_html_report_RedisAddress_section()
        self.gen_html_report_RedisRunner_section()
        self.gen_html_report_RedisVersion_section()

    def __del__(self):
        super().__del__()
        self.html_report_obj.close()


if __name__ == "__main__":
    bpp_obj = BaselineParamParse()
    model, ip = bpp_obj.param_parse(sys.argv[1:])
    if model == "ip":
        # 如果ip模式中未给出ip列出则报错退出
        if ip is None:
            bpp_obj.usage()
            sys.exit(1)
        else:
            ip_list = ip.split(",")
            for ip_addr in ip_list:
                # 如果指定的ip对应的文件并不存在则跳过
                if not os.path.exists(f"../2_info/{ip_addr}_redis_info.xml"):
                    print(f'sorry, file "../2_info/{ip_addr}_redis_info.xml" is not exist, it will be skip')
                    continue
                gen_report_obj = GenRedisHtmlReport(ip_addr)
                gen_report_obj.gen_html_report()
    # 如果指定文件夹模式
    elif model == "dir":
        ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
        full_reg = f"{ip_reg}_redis_info\.xml"
        pwd_file_list = os.listdir("../2_info")
        for file in pwd_file_list:
            if re.search(full_reg, file):
                ip_addr = re.search(ip_reg, file).group()
                gen_report_obj = GenRedisHtmlReport(ip_addr)
                gen_report_obj.gen_html_report()