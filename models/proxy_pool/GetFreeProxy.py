import inspect
import re
from queue import Queue
from time import sleep
import threading
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from models.dataBase.redis import rds
from utils.request import getHtmlTree, ex_request


class GetFreeProxy(object):
    @staticmethod
    def freeProxy01():
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :return:
        """
        url = 'http://www.data5u.com/'
        key = 'ABCDEFGHIZ'
        html_tree = getHtmlTree(url)
        ul_list = html_tree.xpath('//ul[@class="l2"]')
        for ul in ul_list:
            try:
                ip = ul.xpath('./span[1]/li/text()')[0]
                class_names = ul.xpath('./span[2]/li/attribute::class')[0]
                classname = class_names.split(' ')[1]
                port_sum = 0
                for c in classname:
                    port_sum *= 10
                    port_sum += key.index(c)
                port = port_sum >> 3
                yield '{}:{}'.format(ip, port)
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxy02(page_count=2):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        print(str(e))

    @staticmethod
    def freeProxy03():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))

                # HTML中的port是随机数，真正的端口编码在class后面的字母中。
                # 比如这个：
                # <span class="port CFACE">9054</span>
                # CFACE解码后对应的是3128。
                port = 0
                for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                                          "/attribute::class")[0]. \
                        replace("port ", ""):
                    port *= 10
                    port += (ord(_) - ord('A'))
                port /= 8

                yield '{}:{}'.format(ip_addr, int(port))
            except Exception as e:
                print(str(e))

    @staticmethod
    def freeProxy04():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy05():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = ex_request(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy06():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        for url in urls:
            r = ex_request(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy07(page_count=2):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&?page={}'.format(i)
            html_tree = getHtmlTree(url)
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy08(max_page=2):
        """
        http://www.qydaili.com/free/?action=china&page=1
        齐云代理
        :param max_page:
        :return:
        """
        base_url = 'http://www.qydaili.com/free/?action=china&page='
        for page in range(1, max_page + 1):
            url = base_url + str(page)
            r = ex_request(url)
            proxies = re.findall(r'<td.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td.*?>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy09(max_page=2):
        """
        http://www.89ip.cn/index.html
        89免费代理
        :param max_page:
        :return:
        """
        base_url = 'http://www.89ip.cn/index_{}.html'
        for page in range(1, max_page + 1):
            url = base_url.format(page)
            r = ex_request(url)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy10():
        urls = ['http://www.xiladaili.com/putong/',
                "http://www.xiladaili.com/gaoni/",
                "http://www.xiladaili.com/http/",
                "http://www.xiladaili.com/https/"]
        for url in urls:
            r = ex_request(url)
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", r.text)
            for ip in ips:
                yield ip.strip()

    @classmethod
    def checkAllGetProxyFunc(cls):
        member_list = inspect.getmembers(cls, predicate=inspect.isfunction)
        proxy_count_dict = dict()
        for func_name, func in member_list:
            print(u"开始运行 {}".format(func_name))
            try:
                proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
                proxy_count_dict[func_name] = len(proxy_list)
            except Exception as e:
                print(u"代理获取函数 {} 运行出错!".format(func_name))
                print(str(e))
        print(u"所有函数运行完毕 " + "***" * 5)
        for func_name, func in member_list:
            print(u"函数 {n}, 获取到代理数: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))

    @classmethod
    def checkGetProxyFunc(cls, func_name):
        """
        检查指定的getFreeProxy某个function运行情况
        Args:
            func: getFreeProxy中某个可调用方法

        Returns:
            None
            :param func_name:
        """
        func = getattr(cls, func_name)
        print("start running func: {}".format(func_name))
        count = 0
        for proxy in func():
            if verifyProxyFormat(proxy):
                print("{} fetch proxy: {}".format(func_name, proxy))
                count += 1
        print("{n} completed, fetch proxy number: {c}".format(n=func_name, c=count))

    @classmethod
    def proxyNames(cls):
        return [i[0] for i in inspect.getmembers(cls, predicate=inspect.isfunction)]


def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def validUsefulProxy(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode("utf8")
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=5, verify=False)
        if r.status_code == 200:
            return True
    except:
        pass
    return False


def ProxyScheduler():
    proxy_set = set()
    for i in GetFreeProxy.proxyNames():
        try:
            for p in getattr(GetFreeProxy, i)():
                proxy = p.strip()
                if proxy and verifyProxyFormat(proxy) and (proxy not in proxy_set):
                    proxy_set.add(proxy)
                    rds.sadd("proxies", proxy)
            print(f"proxies size == {rds.scard('proxies')}")
        except:
            pass
    ProxyCheckThreads(RawProxyCheck, "proxies", 10)
    ProxyCheckThreads(UsefulProxyCheck, "useful_proxies", 5)


def ProxyCheckThreads(func, db, threads):
    proxy_queue = Queue()
    for _proxy in rds.smembers(db):
        proxy_queue.put(_proxy)
    thread_list = list()
    for index in range(threads):
        thread = threading.Thread(target=func, args=(proxy_queue,))
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


def RawProxyCheck(p_queue):
    while True:
        if p_queue.empty():
            break
        proxy = p_queue.get(block=False)
        status = validUsefulProxy(proxy)
        if status:
            rds.sadd("useful_proxies", proxy)
            print(f"add useful_proxies {proxy},useful_proxies size = {rds.scard('useful_proxies')}")
        else:
            rds.srem("proxies", proxy)
            print(f"del proxies {proxy},proxies size = {rds.scard('proxies')}")
        p_queue.task_done()


def UsefulProxyCheck(p_queue):
    while True:
        if p_queue.empty():
            break
        proxy = p_queue.get(block=False)
        status = validUsefulProxy(proxy)
        if not status:
            rds.srem("useful_proxies", proxy)
            print(f"del useful_proxies {proxy},useful_proxies size = {rds.scard('useful_proxies')}")
        p_queue.task_done()


def runProxy():
    ProxyScheduler()
    scheduler = BlockingScheduler()
    scheduler.add_job(ProxyCheckThreads, trigger='interval', args=(RawProxyCheck, "proxies", 10), minutes=7,
                      id="raw_proxy_check", name="raw_proxy定时采集")
    scheduler.add_job(ProxyCheckThreads, trigger='interval', args=(UsefulProxyCheck, "useful_proxies", 5), minutes=2,
                      id="useful_proxy_check", name="useful_proxy定时检查")
    scheduler.start()


if __name__ == '__main__':
    runProxy()
    # GetFreeProxy().checkAllGetProxyFunc()
    # GetFreeProxy().checkGetProxyFunc("freeProxy09")
    # for i in GetFreeProxy.proxyNames():
    #     GetFreeProxy.checkGetProxyFunc(i)
