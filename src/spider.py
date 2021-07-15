import requests
import random
import calendar
from lxml import etree
import time
import re
import traceback
import pandas as pd
requests.adapters.DEFAULT_RETRIES = 5

class Spider():
    def __init__(self, config):
        self.config = config
        self.path_start = 10
        self.path_end = 1260
        self.path = "https://nextfin.uk/equity/pitches/"
        self.headers = {"User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Connection": "close"}
        self.xpath = {"title": r'//*[@id="maintop"]/div[@class="row p-4"]/div[@class="container-fluid"]/div[@class="row clearfix"]/div[@class="col-lg-9 clearfix homecontent"]/div[@class="row"]//div[@class="pitches"]//div[@class="titlerow"]//span[@class="pitchtitle"]',
            "title_url": r'//*[@id="maintop"]/div[@class="row p-4"]/div[@class="container-fluid"]/div[@class="row clearfix"]/div[@class="col-lg-9 clearfix homecontent"]/div[@class="row"]//div[@class="pitches"]//div[@class="titlerow"]/a/@href',
            "industry": r'//*[@id="maintop"]/div[@class="container-fluid"]/div[@class="row clearfix align-bottom"]/div[@class="col-sm-6 markettop"]/a',
            "page_title": r'//*[@id="maintop"]/div[1]/div[1]/div[1]/h1',
            "status": r'//*[@id="maintop"]/div[@class="container-fluid"]/div[@class="row clearfix align-bottom"]//p/strong',
            "time": r'normalize-space(//*[@id="maintop"]/div[@class="container-fluid"]/div[@class="row clearfix align-bottom"]//p/strong/small)',
            "pledged_goal": r'//*[@id="newinfo"]/div[1]//article//li/strong',
            "target": r'//*[@id="newinfo"]/div[1]//article//ul[2]/p/strong',
            "target_text": r'//*[@id="newinfo"]//article/div[3]/ul[2]/p/text()',
            "company_num": r'//*[@id="newinfo"]//ul[2]/p/strong/a',
            "incorporated_text": r'//*[@id="newinfo"]//ul[2]/p[8]/text()',
            "graph_func": r'//*[@id="newinfo"]//article/div[@class="row clearfix"]//script'}
        self.use_proxy = config["use_proxy"]

    def get_proxy(self):
        proxy = self.config["proxy"]
        https_proxy = "https://" + proxy
        http_proxy = "http://" + proxy
        
        proxies = {"https":https_proxy, "http": http_proxy}
        return proxies

    """get title page"""
    def get_title_raw_page(self, _params):
        if (self.use_proxy):
            _proxy = self.get_proxy()
            self.get_random_headers()
            _r = requests.get(self.path, headers = self.headers, proxies = _proxy, params = _params)
        else:
            self.get_random_headers()
            _r = requests.get(self.path, headers = self.headers, params = _params)

        return _r
    
    def get_detailed_page(self, url_path):
        if (self.use_proxy):
            _proxy = self.get_proxy()
            self.get_random_headers()
            _r = requests.get(url_path, headers = self.headers, proxies = _proxy)
        else:
            self.get_random_headers()
            _r = requests.get(url_path, headers = self.headers)
 
        time.sleep(5)
        return _r

    def parse_html(self, raw_page):
        page = etree.HTML(raw_page.text)
        return page

    def get_info(self, _xpath, page):
        return page.xpath(_xpath)
    
    def get_random_headers(self):
        USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        
        random_agent = USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]
        self.headers['User-Agent'] = random_agent
        return

    def process_graph(self, func_text, label_prog, total_prog, company_name):
        
        time_labels = label_prog.search(func_text).group(0).split(",")
        total_num = total_prog.search(func_text).group(0).split(",")

        time_series = list(map(lambda x: x[-3:-1] + "-" + x[1:3], time_labels))
        # time_series = list(map(lambda x: datetime.datetime.strptime(x[1:-1], "%d-%m").strftime("%m-%d"), time_labels))
        df = pd.DataFrame(total_num, index = time_series, columns = [str(company_name)])
        return df


    def get_detailed_info(self, page):
        target = self.get_info(self.xpath['target'], page)
        incorporated_text = self.get_info(self.xpath['incorporated_text'], page)
        if incorporated_text != []:
            num_incorporated = incorporated_text[1].strip("\n").strip("\t")
        else:
            num_incorporated = 0
        company_num = self.get_info(self.xpath['company_num'], page)
        # [target, pre_money, equity, investor, pledge_avg, company_num, status, incorporated, price]

        flag = 0
        if company_num == []:
            flag = 1
        for i in range(0, len(target)):
            tmp_target = target[i]
            if tmp_target.text is not None:
                target[i] = tmp_target.text.strip("\n").strip("\t")
            else:
                target[i] = company_num[0].text

        if "%" not in target[2]: #equity
            target.insert(2, "null")
        if "£" in target[3]: # investors
            target.insert(3, "0")
        if "£" not in target[4]: # avg pledge
            target.insert(4, "0")
        if flag == 1: # company_num
            target.insert(5, "null")
        if flag == 1: # company_status
            target.insert(6, "null")
        if (len(target) < 8) or ("/" not in target[7]): #incorporated
            target.insert(7, "0")
        if (len(target) < 9) or ("£" not in target[-1]):# price
            target.append("0")
                 
        target[0] = target[0][1:]
        target[1] = target[1][1:]
        target.append(num_incorporated)
        return target

    def proxy_util(self):
        if self.config['use_proxy']:
            current_time = time.strftime("%M", time.localtime())
            if (current_time == "59"):
                time.sleep(120)
            if (current_time == "58"):
                time.sleep(180)

    def process_date(self, date):
        splited_date = date.split(" ")
        month = list(calendar.month_abbr).index(splited_date[0])
        day = splited_date[1][:-2]
        year = splited_date[-1]
        return year + '/' + str(month) + "/" + day

    """crawl for the company page url
    
    ---
    Args:
        csv_path: the saved csvfile path for the company page url
    """
    def get_company_url(self, csv_path):
        payload = {"crowdfunding_projects_page": "10",
                    "crowdfunding_site": "7"}

        titles = []
        try:
            for page_num in range(self.path_start, self.path_end, 10):
                payload["crowdfunding_projects_page"] = str(page_num)
                raw_title_page = self.get_title_raw_page(payload)
                title_page = self.parse_html(raw_title_page)
                # title_tmp = self.get_info(self.xpath["title"], title_page)
                title_urls = self.get_info(self.xpath["title_url"], title_page)
                for url in title_urls:
                    if url[:2] == "//":
                        titles.append(url)
                sleep_time = random.randint(5, 10)
                time.sleep(sleep_time)
                print(page_num)
                # for title in title_tmp:
                #     titles.append(title.text)
            
        finally:
            df = pd.DataFrame(titles)
            df.to_csv(csv_path)
            print("write complete")

        print("load complete")

    def start_get_info(self, title_path, graph_path, log_path, saved_path, t = 630):
        df = pd.read_csv(title_path, index_col=0)
        
        df_lst = df.iloc[:, 0].tolist()[t:]
        n = len(df_lst)
        saved_df = pd.DataFrame(columns = ['company_name', "industry", "status", "orig_start", "orig_end", "process_start", "process_end", \
            "pledged", "goal", "target", "pre_money", "equity", "investor", "pledge_avg", "company_num", "company_status", "incorporated", \
                "price", "incorporated_text", "url"])
        graph_label_pattern = r'(?<=graph_labels=(\[))([^(\]);]+)'
        graph_label_prog = re.compile(graph_label_pattern)
        total_pattern = r'(?<=view_data=(\[))([^(\]);]+)'
        total_prog = re.compile(total_pattern)

        try:
            for i in range(0, n):
                self.proxy_util()
                url_path = "https:" + df_lst[i]
                sleep_time = random.randint(5, 10)
                time.sleep(sleep_time)
                
                raw_detailed_page = self.get_detailed_page(url_path)
                detailed_page = self.parse_html(raw_detailed_page)
                tmp_title = self.get_info(self.xpath["page_title"], detailed_page)
                if (tmp_title == []):
                    with open(log_path, "a+") as f:
                        f.write(url_path + "\n")
                    saved_df.loc[i] = [tmp_title, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
                    print(url_path + " failed")
                    continue
                
                tmp_title = tmp_title[0].text
                tmp_lst = [tmp_title]
                industry = self.get_info(self.xpath["industry"], detailed_page)[0].text
                tmp_lst.append(industry)
                tmp_lst.append(self.get_info(self.xpath["status"], detailed_page)[0].text) # status

                crowd_time = self.get_info(self.xpath['time'], detailed_page).split(" - ")
                tmp_lst.extend(crowd_time)
                process_crowd_time = list(map(lambda x: self.process_date(x), crowd_time))
                tmp_lst.extend(process_crowd_time)

                pledge_goal = self.get_info(self.xpath['pledged_goal'], detailed_page)
                pledge_goal = list(map(lambda x: x.text, pledge_goal))
                pledge_goal[0] = pledge_goal[0][1:]
                tmp_lst.extend(pledge_goal)
                
                detailed_info = self.get_detailed_info(detailed_page)
                tmp_lst.extend(detailed_info)
                tmp_lst.append(url_path)
                if (len(tmp_lst) < 20):
                    with open(log_path, "a+") as f:
                        f.write(tmp_title + "\n")
                    saved_df.loc[i] = [tmp_title, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
                    print(tmp_title + " failed")
                    continue
                saved_df.loc[i] = tmp_lst
                
                elem_graph = self.get_info(self.xpath['graph_func'], detailed_page)
                if elem_graph == []:
                    graph_df = pd.DataFrame(["not enough data"], columns = [tmp_title])
                else:
                    graph_df = self.process_graph(elem_graph[0].text, graph_label_prog, total_prog, tmp_title)
                if ("*" in tmp_title):
                    tmp_title = tmp_title.replace("*", "")
                new_graph_path = graph_path + tmp_title + ".csv"

                graph_df.to_csv(new_graph_path)
                print(tmp_title + " load complete", i + self.config['t'])

        except Exception as e:
            print(tmp_title)
            traceback.print_exc()
        finally:
            saved_df.to_csv(saved_path)
    
    def main(self):
        self.proxy_util()
        if self.config['mode'] == "info":
            self.start_get_info(self.config["title_save_path"], self.config["graph_path"],
                                self.config["log_path"], self.config["detailed_save_path"], self.config["t"])
        else:
            self.get_company_url(self.config["title_save_path"])
        print("task complete")