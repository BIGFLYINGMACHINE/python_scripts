import re
import sys
import urllib

import requests


def get_onepage_urls(onepageurl):
    """获取单个翻页的所有图片的urls+当前翻页的下一翻页的url"""
    if not onepageurl:
        print('已到最后一页, 结束')
        return [], ''
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []  #list
        fanye_url = ''  #字符串
        return pic_urls, fanye_url
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    #re.compile制作模板，去掉后也能执行
    #fanye_urls = re.findall(r'<a href="(.*)" class="n">下一页</a>', html)
    fanye_urls = re.findall(r'<a href="(.*)"><span class="pc" data="right">[0,1]?[0-9]</span></a>', html) 
    fanye_url = 'http://image.baidu.com' + fanye_urls[0] if fanye_urls else ''
     
    return pic_urls, fanye_url


def down_pic(pic_urls):
    """给出图片链接列表, 下载所有图片"""
    for i, pic_url in enumerate(pic_urls):    
        try:    
            pic = requests.get(pic_url, timeout=3)
            string = str(i + 1) + '.jpg'
            if str(pic.status_code)[0] == "4":
                print('2下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
                continue
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('1下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue
        """
        try:
            pic = requests.get(pic_url, timeout=3)
            string = str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue
       """
#直接执行时，执行下列代码，引用时不执行
if __name__ == '__main__':
    keyword = '石原里美'  # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    url_init_first = r'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1497491098685_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1497491098685%5E00_1519X735&word='
    #quote对keyword进行url编码
    url_init = url_init_first + urllib.parse.quote(keyword, safe='/')
    all_pic_urls = []
    #onepage_urls为当前页图片url
    onepage_urls, fanye_url = get_onepage_urls(url_init)
    #储存图片url
    all_pic_urls.extend(onepage_urls)

    fanye_count = 0  # 累计翻页数
 
    while 1:
        onepage_urls, fanye_url = get_onepage_urls(fanye_url)
        fanye_count += 1

        print('第%s页' % fanye_count)
        if fanye_url == '' and onepage_urls == []:
            break
        all_pic_urls.extend(onepage_urls)

    down_pic(list(set(all_pic_urls)))
 