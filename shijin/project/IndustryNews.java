package main.java.com.pharmcube.news;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import com.pharmcube.commons.utils.StringUtils;
import com.pharmcube.server.newsearch.service.ESService;
import main.java.com.pharmcube.downloader.ProxyHttpClientDownloader;
import main.java.com.pharmcube.downloader.ProxyHttpClientDownloaderABuYun;
import main.java.com.pharmcube.utils.*;
import main.java.com.pharmcube.utils.es.DubboESOpreation;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.JedisCluster;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Request;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.Spider;
import us.codecraft.webmagic.processor.PageProcessor;

import java.util.*;

/**
 * 全佳 采集指定网站的快讯：
 */
public class IndustryNews implements PageProcessor {
    private static String es_index = "industry_news";
    private static String base_channel = "base_channel"; //正文匹配的标签
    private static ESService service = DubboESOpreation.service();
    private static JedisCluster jedis = RedisUtils.connectionRedis();
    private static List<String> content_keywords_list = new ArrayList<>();
    private static Map<String, List<String>> get_type_map = new HashMap<>();
    private static Set<String> invalid_data_set = new HashSet<>();
    private static Logger logger = LoggerFactory.getLogger(IndustryNews.class);
    private static String content_type_coll_name = "industry_news_type"; //正文内容匹配数据
    private static String spider_params_coll_name = "industry_news_spider_params"; //待采集的URL
    private Site site = Site.me().setCycleRetryTimes(8).setSleepTime(1000).setTimeOut(30000)
            .setCharset("UTF-8")
            .setUserAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4209.400");

    @Override
    public void process(Page page) {
        String url = page.getUrl().toString();
        Document doc = Jsoup.parse(page.getRawText());
        Request spider_request = page.getRequest();
        String spider_type = String.valueOf(spider_request.getExtra("spider_type"));
        String source = String.valueOf(spider_request.getExtra("source"));
        String spider_location = String.valueOf(spider_request.getExtra("spider_location"));

        if(url.endsWith("baidu.com")){
            List<DBObject> industry_news_all = MongoDBUtils.queryAll(es_index);
            for(DBObject db : industry_news_all){
                String esid = String.valueOf(db.get("esid"));
                invalid_data_set.add(esid);
            }

            List<DBObject> base_channel_all = MongoDBUtils.queryAll(base_channel);
            for( DBObject db : base_channel_all ){
                String keyword = String.valueOf(db.get("keyword"));
                content_keywords_list.add(keyword);
            }
            List<DBObject> all = MongoDBUtils.queryAll(content_type_coll_name);
            for( DBObject db : all ){
                String type = String.valueOf(db.get("type"));
                List<String> keywords_list = (List<String>) db.get("keywords");
                get_type_map.put(type, keywords_list);
            }
            List<DBObject> spider_url_params = MongoDBUtils.queryAll(spider_params_coll_name);
            for( DBObject db : spider_url_params ) {
                db.removeField("_id");
                JSONObject mongo_obj = JSONObject.fromObject(db);
                Request request = new Request(db.get("url").toString());
                for(Object key : mongo_obj.keySet())
                    request.putExtra(String.valueOf(key),mongo_obj.get(key) );
                page.addTargetRequest(request);
            }
        }

        if("title".equals(spider_type))
            parseTitlePage(doc,page,url,source,spider_location);

        if("detail".equals(spider_type))
            parseDetailPage(doc,spider_request,url,source,spider_location);

    }

    private void parseDetailPage(Document doc, Request spider_request, String url, String source, String spider_location) {
        if(url.contains("gelonghui.com")){
            String date_str = doc.select("span.date").text();
            String spider_publish_date = "";
            if(date_str.contains("前"))
                spider_publish_date = DateUtils.tampConvertUS(DateUtils.convertTamp(doc.select("span.date").text()));
            else
                spider_publish_date = doc.select("span.date").text();
            parseDetailPage(url,source,spider_location,spider_request,doc,"h1.title",spider_publish_date,"article.main-news");
        }else if(url.contains("zhitongcaijing.com")){
            String spider_publish_date = String.valueOf(DateUtils.getDateStr(doc.select("div.line-h-30").text()).toArray()[0]);
            doc.select("a.type").remove();
            doc.select("div.line-h-30").remove();
            doc.select("p").select("strong").remove();
            doc.select("span[id=author_external]").remove();
            parseDetailPage(url,source,spider_location,spider_request,doc,"h1",spider_publish_date,"article");
        }else if(url.contains("jiemian.com")){
            String spider_publish_date = String.valueOf(DateUtils.getDateStr(doc.select("span.date").text()).toArray()[0]);
            parseDetailPage(url,source,spider_location,spider_request,doc,"h1",spider_publish_date,"div.article-content");
        }else if(url.contains("eastmoney.com")){
            String spider_publish_date = String.valueOf(DateUtils.getDateStr(doc.select("div.time").text()).toArray()[0]);
            parseDetailPage(url,source,spider_location,spider_request,doc,"h1",spider_publish_date,"div.b-review");
        }else if(url.contains("sina.com.cn")){
            doc.select("div.appendQr_normal").remove();
            doc.select("div.appendQr_normal_txt").remove();
            doc.select("p.article-editor").remove();
            Elements meta_elements = doc.select("meta");
            String spider_publish_date = "";
            for(Element meta_element : meta_elements){
                String name = meta_element.attr("name");
                if(name.contains("article:create_at")){
                    spider_publish_date = String.valueOf(DateUtils.getDateStr(meta_element.attr("content")).toArray()[0]);
                    break;
                }
            }
            parseDetailPage(url,source,spider_location,spider_request,doc,"h1.main-title",spider_publish_date,"div.article");
        }else if(url.contains("bioon.com")){
            String spider_publish_date = String.valueOf(DateUtils.getDateStr(doc.select("div.title5").select("p").first().text()).toArray()[0]);
            spider_publish_date = spider_publish_date.split(" ")[0];
            parseDetailPage(url,source,spider_location,spider_request,doc,"h1",spider_publish_date,"div.text3");
        }
    }

    private void parseDetailPage(String url,String source,String spider_location,Request spider_request, Document doc, String title_rule, String spider_publish_date, String content_rule) {
        String esid = String.valueOf(spider_request.getExtra("esid"));
        String title = doc.select(title_rule).text();
        Long publish_date = DateUtils.convertTamp(spider_publish_date);
        Elements article_elements = doc.select(content_rule);
        String context = article_elements.toString();
        context = CommonUtils.removeAttr(context);
        String context_nolabel = article_elements.text();
        String summary = "";
        if(article_elements.select("p").size()>0)
            summary = article_elements.select("p").first().text();
        if(StringUtils.isBlank(summary))
            summary = article_elements.select("div").first().text();
        if(url.contains("bioon.com")){
            if(article_elements.select("div").size()>2)
                summary = article_elements.select("div").get(2).text();
            else
                summary = article_elements.select("p").get(2).text();
        }

        if(summary.contains("丨")){ //移除标识
            String remove_value = summary.split("丨")[0];
            summary = summary.replace(remove_value+"丨", "").trim();
            context = context.replace(remove_value+"丨", "").trim();
            context_nolabel = context_nolabel.replace(remove_value+"丨", "").trim();
        }
        boolean is_contains_keyword = false;
        for(String keyword : content_keywords_list){
            if(context_nolabel.contains(keyword)){
                is_contains_keyword = true;
                break;
            }
        }
        if(!is_contains_keyword){
            logger.info("当前文章未包含指定关键词，被过滤："+title);
            JSONObject mongo_obj = new JSONObject();
            mongo_obj.put("url", url);
            mongo_obj.put("title", title);
            mongo_obj.put("spider_wormtime", System.currentTimeMillis());
            MongoDBUtils.append(es_index,new BasicDBObject("esid", esid),new BasicDBObject(mongo_obj) );
            return;
        }
        String type = "其他"; //文章分类
        for(String key : get_type_map.keySet()){
            List<String> get_type_list = get_type_map.get(key);
            for(String params : get_type_list){
                if(context_nolabel.contains(params)){
                    type = key;
                    break;
                }
            }
        }
        insertESData(type,esid,url,spider_location,source,title,spider_publish_date,publish_date,context,context_nolabel,summary);
    }

    private void insertESData(String type, String esid, String url, String spider_location, String source, String title,
                              String spider_publish_date, Long publish_date, String context, String context_nolabel,String summary) {
        long spider_wormtime = System.currentTimeMillis();
        Map<String, Object> es_map = new HashMap<>();
        es_map.put("url",url );
        es_map.put("type",type );
        es_map.put("title",title );
        es_map.put("source",source );
        es_map.put("context",context );
        es_map.put("summary",summary );
        es_map.put("publish_date",publish_date );
        es_map.put("spider_location",spider_location );
        es_map.put("context_nolabel",context_nolabel );
        es_map.put("spider_publish_date",spider_publish_date );
        es_map.put("spider_wormtime",spider_wormtime );
        logger.info("------- insert es data -------"+esid+"\t"+title);
        jedis.del("industry_news_index");
        service.insertOrUpdateFields(es_index,esid ,es_map);
    }

    private void parseTitlePage(Document doc, Page page,String url,String source,String spider_location) {
        if(url.contains("gelonghui.com"))
            parseTitlePage("https://www.gelonghui.com",doc,page ,url ,source ,spider_location,"section.detail-right" );
        else if(url.contains("zhitongcaijing.com"))
            parseTitlePage("https://www.zhitongcaijing.com",doc,page ,url ,source ,spider_location,"div.list-art|dl" );
        else if(url.contains("jiemian.com"))
            parseTitlePage("",doc,page ,url ,source ,spider_location,"div.item-news" );
        else if(url.contains("eastmoney.com")){
            JSONObject results_obj = JSONObject.fromObject(page.getRawText().replace("var ajaxResult=", ""));
            JSONArray lives_list = results_obj.getJSONArray("LivesList");
            for(int i=0;i<lives_list.size();i++){
                JSONObject lives_list_obj = lives_list.getJSONObject(i);
                String detail_url = lives_list_obj.getString("url_unique");
                addSpiderDetailURL(page,detail_url,source,spider_location);
            }
        }else if(url.contains("sina.com.cn"))
            parseTitlePage("",doc,page ,url ,source ,spider_location,"ul.list_009" );
        else if(url.contains("bioon.com"))
            parseTitlePage("",doc,page ,url ,source ,spider_location,"ul[id=cms_list]|li" );

    }

    private void parseTitlePage(String url_prefix, Document doc, Page page, String url, String source, String spider_location, String label) {
        Elements select_elements = null;
        String[] splits = label.split("\\|");
        for(int i=0;i<splits.length;i++){
            if (i == 0)
                select_elements = doc.select(splits[0]);
            else
                select_elements = select_elements.select(splits[i]);
        }
        for(Element select_element : select_elements){
            String detail_url = url_prefix+select_element.select("a").attr("href").trim();
            addSpiderDetailURL(page,detail_url,source,spider_location);
        }
    }

    private void addSpiderDetailURL(Page page, String detail_url, String source, String spider_location) {
        String esid = MD5Utils.getMD5(detail_url);
        if(!invalid_data_set.add(esid)){
            logger.info("当前数据已采集，被过滤："+esid);
            return;
        }
        if(service.getExist(es_index, esid)){
            logger.info("当前快讯已经存在，被过滤："+esid);
            return;
        }
        Request request = new Request(detail_url);
        request.putExtra("esid", esid);
        request.putExtra("source", source);
        request.putExtra("spider_type", "detail");
        request.putExtra("spider_location", spider_location);
        page.addTargetRequest(request);
    }

    @Override
    public Site getSite() {
        return site;
    }

   // public static void main(String[] args) {
    public static void execute() {
        String url = "https://www.baidu.com";
        Spider.create(new IndustryNews()).setDownloader(new ProxyHttpClientDownloaderABuYun()).addUrl(url).run();
    }
}
