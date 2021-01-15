
from scrapy import cmdline

#cmdline.execute(['scrapy','crawl','qcc'])
#cmdline.execute(['scrapy', 'crawl', 'invest'])
#cmdline.execute(['scrapy','crawl','wechat_mp'])
#cmdline.execute(['scrapy', 'crawl', 'nhsa'])

'''
medlive; fund; newswire; ipo_us; ispor; patent_google; cde; newswire; pmc_article;
wind; wind_invest; 
'''
cmdline.execute(['scrapy', 'crawl', 'pmc_article',])

#cmdline.execute(['scrapy', 'crawl', 'cde','-a' 'spider_test=electronics'])

#cmdline.execute(['scrapy','crawl','qccnew'])


#cmdline.execute(['scrapy', 'crawl', 'wechat_like_nums'])


