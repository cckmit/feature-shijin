import requests,re,time
import json
# 辉瑞
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Content-Length":"6800",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"Hm_lvt_03879bfedd1c0d705359805a050e377c=1618835461,1618882449,1619061930; Hm_lpvt_03879bfedd1c0d705359805a050e377c=1619061930",
    "Host":"www.pfizer.cn",
    "Origin":"http://www.pfizer.cn",
    "Proxy-Connection":"keep-alive",
    "Referer":"http://www.pfizer.cn/(S(14y4dla5g4pnb0vtw31wel45))/news/pfizer_press_releases_cn.aspx",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
data = {
    "__EVENTTARGET":"DataPager$ctl00$ctl01",
    "__EVENTARGUMENT":"",
    "__VIEWSTATE":"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6IGU5ouT55Sf54mp5a6j5biD5byA5bGV5oiY55Wl5ZCI5L2c77yM5pC65omL5o6o5Yqo5Yib5paw55aX5rOV5Zyo5aSn5Lit5Y2O5Yy655qE5Y+R5bGV2wI8cD4NCgnnur3nuqbjgIHkuIrmtbflkozmma7mnpfmlq/pob/lv6vorq8mbWRhc2g7Jm1kYXNoOzIwMjDlubQxMeaciDE55pelJm1kYXNoOyZtZGFzaDvovonnkZ7vvIhOWVNF77yaUEZF77yJ5ZKM6IGU5ouT55Sf54mp5LuK5aSp5a6j5biD6L6+5oiQ5ZCI5L2c5YWz57O777yM5pC65omL5o6o5Yqo5Yib5paw6I2v54mp5Zyo5aSn5Lit5Y2O5Yy655qE5byA5Y+R5ZKM5LiK5biC44CC6IGU5ouT55Sf54mp55Sx5LiW55WM55+l5ZCN5oqV6LWE5py65p6EUGVyY2VwdGl2ZSBBZHZpc29yc+WIm+eri++8jOebruWJjeS4jui+ieeRnuW7uueri+S6huWQiOS9nOWFs+ezu++8jOWFseWQjOWvu+axguWIm+aWsOeahC4uLmQCBQ9kFgJmDxUFETIwMjDlubQxMeaciDE45pelAzY3M3rovonnkZ7lkoxCaW9OVGVjaOWuo+W4g+e7k+adn+WFtuaWsOWGoOiCuueCjuWAmemAieeWq+iLl+eahOS4ieacn+S4tOW6iueglOeptuS4lOi+vuWIsOS6huaJgOacieS4u+imgeeWl+aViOeahOe7iOeCueimgeaxgnrovonnkZ7lkoxCaW9OVGVjaOWuo+W4g+e7k+adn+WFtuaWsOWGoOiCuueCjuWAmemAieeWq+iLl+eahOS4ieacn+S4tOW6iueglOeptuS4lOi+vuWIsOS6huaJgOacieS4u+imgeeWl+aViOeahOe7iOeCueimgeaxgvkCPHVsPg0KCTxsaT4NCgkJ5Li76KaB5Yqf5pWI5YiG5p6Q6KGo5piO77ya5Zyo6aaW5qyh5o6l56eN5ZCOMjjlpKnlvIDlp4vvvIxCTlQxNjJiMuWvueaWsOWGoOiCuueCjueahOmihOmYsuS9nOeUqOS4ujk1Je+8m+ivhOS8sOS6hjE3MOS+i+ehruiviueahOaWsOWGoOiCuueCjueXheS+i++8jOWFtuS4rTE2MuS+i+S4uuWuieaFsOWJgue7hO+8jDjkvovkuLrmjqXnp43nlqvoi5fnu4TjgII8L2xpPg0KCTxsaT4NCgkJ5Zyo5LiN5ZCM5bm06b6E44CB5oCn5Yir44CB56eN5peP5ZKM5peP6KOU562J5Lq65Y+j5qaC5Ya16LWE5paZ5pa56Z2i77yM5Z2H5Y+W5b6X5LqG5LiA6Ie055qE5Yqf5pWI77yb5a+55LqONjXlsoHku6XkuIrnmoTmiJDlubTkurrvvIzop4IuLi5kAgYPZBYCZg8VBRAyMDIw5bm0MTHmnIg15pelAzY3MXDlubPlronmmbrmhafln47luILkuI7ovonnkZ7ovr7miJDmiJjnlaXlkIjkvZzvvJrmkLrmiYvmjqLntKLllYbkuJrlgaXlurfkv53pmanmlrDmqKHlvI8s5Yqp5Yqb4oCc5YGl5bq35Lit5Zu94oCdcOW5s+WuieaZuuaFp+WfjuW4guS4jui+ieeRnui+vuaIkOaImOeVpeWQiOS9nO+8muaQuuaJi+aOoue0ouWVhuS4muWBpeW6t+S/nemZqeaWsOaooeW8jyzliqnlipvigJzlgaXlurfkuK3lm73igJ37AjxwPg0KCTIwMjDlubQxMeaciDXml6XvvIzkuK3lm73kuIrmtbcgJm1kYXNoOyZtZGFzaDsg56ys5LiJ5bGK5Lit5Zu95Zu96ZmF6L+b5Y+j5Y2a6KeI5Lya5q2j5YC86auY5YWJ5pe25Yi777yM5bmz5a6J5pm65oWn5Z+O5biC5LiO6L6J55Ge5Lit5Zu95LuK5aSp5Zyo5LiK5rW3562+572y5oiY55Wl5ZCI5L2c5aSH5b+Y5b2V77yM5Y+M5pa55bCG5YWx5ZCM5o6i57Si5byA5Y+R5ZWG5Lia5YGl5bq35L+d6Zmp5paw5qih5byP44CCPC9wPg0KPHA+DQoJ5bmz5a6J6ZuG5Zui6IGU5bit6aaW5bit5omn6KGM5a6Y5YW85omn6KGM6JGj5LqL6ZmI5b+D6aKW77yISmVzc2ljYSBUYW7vvInlkozovonnkZ7lhazlj7jokaPkuovplb/lhbzpppbluK3miafooYzlrpjoib4uLi5kAgcPZBYCZg8VBRAyMDIw5bm0MTDmnIg55pelAzY3MDLovonnkZ7nvZXop4Hnl4XliJvmlrDoja/nu7TkuIflv4PCruWcqOS4reWbveiOt+aJuTLovonnkZ7nvZXop4Hnl4XliJvmlrDoja/nu7TkuIflv4PCruWcqOS4reWbveiOt+aJuekCPHA+DQoJMjAyMOW5tDEw5pyIOeaXpe+8jOS4reWbvSZtZGFzaDsmbWRhc2g76L6J55Ge5YWs5Y+45LuK5pel5a6j5biD77yM5Lit5Zu95Zu95a626I2v5ZOB55uR552j566h55CG5bGA5bey57uP5om55YeG57u05LiH5b+DJnJlZzvvvIjmsK/oi6/llJHphbjova/og7blm4rvvIxWeW5kYW1heCZyZWc777yMNjFtZ++8ieeUqOS6juayu+eWl+aIkOS6uumHjueUn+Wei+aIlumBl+S8oOWei+i9rOeUsueKtuiFuue0oOibi+eZvea3gOeyieagt+WPmOaAp+W/g+iCjOeXhe+8iEFUVFItQ03vvInvvIzku6Xlh4/lsJHlv4PooYDnrqHmrbvkuqHlj4rlv4PooYDnrqHnm7jlhbPkvY/pmaLjgILnu7TkuIflv4MmcmVnO+aYr+WFqOeQg+mmli4uLmQCCA9kFgJmDxUFEDIwMjDlubQ55pyIMzDml6UDNjY5TuWfuuefs+iNr+S4muS4jui+ieeRnui+vuaIkOaImOeVpeWQiOS9nO+8jOaQuuaJi+a7oei2s+S4reWbveiCv+eYpOayu+eWl+mcgOaxgk7ln7rnn7Poja/kuJrkuI7ovonnkZ7ovr7miJDmiJjnlaXlkIjkvZzvvIzmkLrmiYvmu6HotrPkuK3lm73ogr/nmKTmsrvnlpfpnIDmsYLnAjx1bD4NCgk8bGk+DQoJCei+ieeRnuWwhui0reWFpeS7t+WAvDLkur/nvo7lhYPnmoTln7rnn7Poja/kuJrogqHku73vvIzlubbku47ln7rnn7Poja/kuJrojrflvpflhbblpITkuo7lkI7mnJ/noJTlj5HpmLbmrrXnmoTogr/nmKTkuqflk4HoiJLmoLzliKnljZXmipfvvIhDUzEwMDHvvIxQRC1MMeaKl+S9k++8ieWcqOS4reWbveWkp+mZhuWcsOWMuueahOaOiOadgzwvbGk+DQoJPGxpPg0KCQnln7rnn7Poja/kuJrmnInmnYPojrflvpfmnIDpq5jlj6/ovr4yLjjkur/nvo7lhYPnmoToiJLmoLzliKnljZXmipfph4znqIvnopHku5jmrL7lj4rpop3lpJbnmoTnibnorrjmnYPkvb/nlKjotLk8L2xpPg0KCTxsaT4NCgkJ5Z+655+zLi4uZAIFDxQrAAJkZGQYAgUJRGF0YVBhZ2VyDxQrAARkZAIIAtMBZAUJTGlzdFZpZXcxDzwrAAoCBzwrAAgACALTAWRbCANIj9nStoaxBhbNOgN6o4msmg==",
    "__VIEWSTATEGENERATOR":"3E480FF3",
    "__EVENTVALIDATION":"/wEWBgL8rq2oCgLkoJaLBALnoJaLBALmoJaLBALhoJaLBALgoJaLBEMoZzNsrDQupcOYwxIMBi7diRQO"
}
url="http://www.pfizer.cn/(S(14y4dla5g4pnb0vtw31wel45))/news/pfizer_press_releases_cn.aspx"
res = requests.post(url,headers=headers,data=data,verify=False)
print(res.status_code)
print(res.text)