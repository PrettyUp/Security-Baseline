import re
from lxml import etree

class BaselineParse:
    def __init__(self,ip_addr,baseline_type="OS"):
        self.baseline_type = baseline_type
        baseline_type_lower = baseline_type.lower()
        self.xml_obj = etree.parse(f"../2_info/{ip_addr}_{baseline_type_lower}_info.xml")
        # self.xml_obj = untangle.parse('os_report_xml.xml')
        # ip_addr = self.xml_obj.xpath("/root/hostinfo/ipaddr")[0].text
        self.html_report_obj = open(f"../4_report/{ip_addr}_{baseline_type_lower}_report.html", "w+", encoding='utf-8')
        self.config_right = 0
        self.config_warn = 0
        self.config_error = 0
        self.gen_html_report_before_sections()


    # 生成html头部信息
    def gen_html_report_head(self):
        ip_addr = self.xml_obj.xpath("/root/hostinfo/ipaddr")[0].text
        self.html_report_obj.writelines("<!Doctype html>\n")
        self.html_report_obj.writelines("<html>\n")
        self.html_report_obj.writelines("<head>\n")
        self.html_report_obj.writelines(f"""<meta charset="utf-8" />\n""")
        self.html_report_obj.writelines(f"<title>{ip_addr}_{self.baseline_type}基线扫描报告</title>\n")
        self.html_report_obj.writelines(f'<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css" />\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/jquery-3.3.1.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/popper.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/bootstrap.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="highcharts/highcharts.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="highcharts/highcharts-3d.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="highcharts/exporting.js"></script>\n')
        self.html_report_obj.writelines("</head>\n")

    # 生成报告头
    def gen_html_report_header(self):
        self.html_report_obj.writelines("<body>\n")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines(f'<h3 style="text-align:center;">{self.baseline_type}基线扫描报告</h3>\n')
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""</div>\n""")


    def gen_html_report_tail(self):
        self.html_report_obj.writelines("</body>\n")
        self.html_report_obj.writelines("</html>\n")

    # 生成主机信息节区
    def gen_html_report_hostinfo_table(self):
        hostname = self.xml_obj.xpath("/root/hostinfo/hostname")[0].text
        ip_addr = self.xml_obj.xpath("/root/hostinfo/ipaddr")[0].text
        try:
            os_version = self.xml_obj.xpath("/root/hostinfo/os_version")[0].text.strip()
        except:
            os_version = ""
        kernel_version = self.xml_obj.xpath("/root/hostinfo/kernel_version")[0].text.strip()
        tcp_services = self.xml_obj.xpath("/root/hostinfo/tcp_services")[0].text
        udp_services = self.xml_obj.xpath("/root/hostinfo/udp_services")[0].text
        tcp_services_lines = tcp_services.split("\n")
        udp_services_lines = udp_services.split("\n")
        listen_addr_reg = "[\.|\d]+:\d+"
        process_reg = "(\d+/\w+)|-"

        tcp_listen_process_str = ""
        for line in tcp_services_lines:
            if "tcp6" not in line:
                listen_addr = re.search(listen_addr_reg, line)
                if listen_addr is not None:
                    listen_addr = listen_addr.group()
                    process = re.search(process_reg, line).group().split("/")[-1]
                    tcp_listen_process_str += f"{listen_addr}-{process}<br />"

        udp_listen_process_str = ""
        for line in tcp_services_lines:
            if "tcp6" not in line:
                listen_addr = re.search(listen_addr_reg, line)
                if listen_addr is not None:
                    listen_addr = listen_addr.group()
                    process = re.search(process_reg, line).group().split("/")[-1]
                    udp_listen_process_str += f"{listen_addr}-{process}<br />"

        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>1. 主机基本信息</h4>\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<table id="hostinfo" class="table table-striped table-bordered">\n""")
        # self.html_report_obj.writelines("""<tr><th colspan="4" style="text-align:center;">主机基本信息<th></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>主机名</th><td>{hostname}</td><th>IP地址</th><td>{ip_addr}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>操作系统</th><td>{os_version}</td><th>内核</th><td>{kernel_version}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>TCP服务</th><td>{tcp_listen_process_str}</td><th>UDP服务</th><td>{udp_listen_process_str}</td></tr>\n""")
        self.html_report_obj.writelines(f"""</table>\n""")
        self.html_report_obj.writelines("""</div>\n""")

    # 写入图表控件div
    def gen_html_report_pie(self):
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>2. 合规统计信息</h4>\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div id="pie_container" style="min-width:400px;height:400px"></div>""")
        self.html_report_obj.writelines("""</div>\n""")

    # 数据在后边各项统计完成后才能得出所以得分出来
    def gen_html_report_pie_fill_data(self):
        self.html_report_obj.writelines("""
                <script>
                    var  chart = Highcharts.chart('pie_container', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                options3d: {
                    enabled: true,
                    alpha: 45,
                    beta: 0
                }
            },
            title: {
                text: '合规检测统计图'
            },
            tooltip: {
                headerFormat: '{series.name}<br>',
                pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    depth: 35,
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    },
                    states: {
                        hover: {
                            enabled: false
                        }  
                    },
                    slicedOffset: 10,         // 突出间距
                    point: {                  // 每个扇区是数据点对象，所以事件应该写在 point 下面
                        events: {
                            // 鼠标滑过是，突出当前扇区
                            mouseOver: function() {
                                this.slice();
                            },
                            // 鼠标移出时，收回突出显示
                            mouseOut: function() {
                                this.slice();
                            },
                            // 默认是点击突出，这里屏蔽掉
                            click: function() {
                                return false;
                            }
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: '检测项占比',
                data: [
                    {name:'合规',   """)
        # 这里不没有很好的格式化办法，各项数据只能单独写入
        self.html_report_obj.writelines(f"y:{self.config_right}")
        self.html_report_obj.writelines(""",color:'#28a745'},
                    {name:'待审查',""")
        self.html_report_obj.writelines(f"y: {self.config_warn}")
        self.html_report_obj.writelines(""",color:'#ffc107'},
                    {name:'不合规',   """)
        self.html_report_obj.writelines(f"y:{self.config_error}")
        self.html_report_obj.writelines(""",color:'#dc3545'}
                ]
            }]
        });
                </script>\n""")

    # 生成展开卡片
    def create_accordion_card(self, accordion_id, accordion_title, collapse_id, show_flag=0, card_class="bg-danger text-white"):
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines(f"""<div id="{accordion_id}">\n""")
        self.html_report_obj.writelines("""<div class="card">\n""")
        self.html_report_obj.writelines(f"""<div class="card-header {card_class}">\n""")
        self.html_report_obj.writelines(f"""<a class="card-link text-white" data-toggle="collapse" href="#{collapse_id}">{accordion_title}</a>\n""")
        self.html_report_obj.writelines("""</div>\n""")
        if show_flag == 1:
            self.html_report_obj.writelines(f"""<div id="{collapse_id}" class="collapse show" data-parent="#{accordion_id}">\n""")
        else:
            self.html_report_obj.writelines(f"""<div id="{collapse_id}" class="collapse" data-parent="#{accordion_id}">\n""")
        self.html_report_obj.writelines("""<div class="card-body" style="padding:0.25rem">\n""")

    def close_div_label(self,times=1):
        for _ in range(times):
            # print(f"{i}")
            self.html_report_obj.writelines("""</div>\n""")

    def gen_html_report_create_section_collect(self):
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>3. 合规检测项详情</h4>\n""")
        self.html_report_obj.writelines("""<br />""")

    def gen_html_report_close_section_collect(self):
        self.close_div_label()

    # 生成“4. 说明”节区
    def gen_html_report_explain(self):
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>4. 说明</h4>\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<table id="report_explain" class="table table-striped table-bordered">\n""")
        self.html_report_obj.writelines(f"""<tr><td><span class="badge badge-danger">红色</span></td><td>不符合配置规范要求，需要进行加固</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><td><span class="badge badge-warning" style="color:#fff;">黄色</span></td><td>不确定是否符合配置规范要求，需要人工介入确认</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><td><span class="badge badge-success">绿色</span></td><td>确认符合配置规范要求，不需要进行修改</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.html_report_obj.writelines("""</div>""")

    # 生成各检测项html报告之前的部分
    def gen_html_report_before_sections(self):
        self.gen_html_report_head()
        self.gen_html_report_header()
        self.gen_html_report_hostinfo_table()
        self.gen_html_report_pie()
        self.gen_html_report_create_section_collect()

    # 生成各检测项html报告之后的部分
    def gen_html_report_after_sections(self):
        self.gen_html_report_close_section_collect()
        self.gen_html_report_explain()
        self.gen_html_report_pie_fill_data()
        self.gen_html_report_tail()

    def replace_n_by_bar_label(self,org_content):
        modify_content = org_content.replace("\n","<br />")
        return modify_content
    def correct_accordion_class(self,collapse_id,accordion_class_sign):
        if "bg-danger" in accordion_class_sign:
            accordion_class = "card-header bg-danger text-white"
        elif "bg-warning" in accordion_class_sign:
            accordion_class = "card-header bg-warning text-white"
        else:
            accordion_class = "card-header bg-success text-white"
        self.html_report_obj.writelines(f"""
<script>
    var accordion_obj = document.getElementById("{collapse_id}").previousElementSibling;
    accordion_obj.setAttribute("class","{accordion_class}")
</script>""")
    def __del__(self):
        self.gen_html_report_after_sections()