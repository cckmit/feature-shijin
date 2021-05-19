package main.java.com.pharmcube.news;
import com.pharmcube.server.newsearch.entity.query.Query;
import com.pharmcube.server.newsearch.entity.query.QueryType;
import com.pharmcube.server.newsearch.service.ESService;
import main.java.com.pharmcube.downloader.ProxyHttpClientDownloaderABuYun;
import main.java.com.pharmcube.utils.*;
import main.java.com.pharmcube.utils.es.DubboESOpreation;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import org.apache.commons.lang.StringUtils;
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
 *  港交所新上市公告：https://www1.hkexnews.hk/app/appindex.html?lang=zh
 *  科创板申报情况：http://kcb.sse.com.cn/disclosure/#
 *      项目基本信息: http://query.sse.com.cn/commonSoaQuery.do?isPagination=true&sqlId=SH_XM_LB&stockAuditNum=9
 *      根据公司名称检索：http://kcb.sse.com.cn/renewal/
 *
 */
public class IPONews implements PageProcessor {
    private static String send_email_content = "";
    private static JedisCluster jedis = RedisUtils.connectionRedis();
    private static ESService service = DubboESOpreation.service();
    private static Logger logger = LoggerFactory.getLogger( IPONews.class);
    private static String hk_es_index = "news"; // 港交所新上市公告
    private static String ckb_es_index = "stib"; // 科创板申报情况
    private static Set<String> approval_status_set = new HashSet<>();//记录科创版审核状态发生变更
    private Site site = Site.me().setCycleRetryTimes(6).setSleepTime(600).setTimeOut(10000)
            .setCharset("utf-8")
            .addHeader("Referer", "http://kcb.sse.com.cn/disclosure")
            .addHeader("collectionName","yes" )
            .setJedisCluster(jedis)
            .setUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36");

    @Override
    public void process(Page page) {
        String url = page.getUrl().toString();
        if(url.endsWith("baidu.com")){
            page.addTargetRequest("https://www1.hkexnews.hk/ncms/json/eds/appactive_app_sehk_c.json");
            page.addTargetRequest("https://www1.hkexnews.hk/ncms/json/eds/appactive_appphip_sehk_c.json");
            for(int i=1;i<6;i++)
                page.addTargetRequest("https://www1.hkexnews.hk/ncms/json/eds/lcisehk7relsdc_"+i+".json");
            for(int i=1;i<4;i++)
                page.addTargetRequest("http://query.sse.com.cn/commonSoaQuery.do?isPagination=true&sqlId=GP_GPZCZ_SHXXPL&pageHelp.pageSize=20&fileType=30%2C5%2C6&pageHelp.pageNo="+i);
            // 监控 科创板数据是否发生变更
            List<Map<String, Object>> list = service.getList(ckb_es_index, null, null, null, -1, "spider_url", "company_name");
            for(Map<String, Object> map :list){
                if(!map.containsKey("spider_url"))
                    continue;
                String spider_url_detail = map.get("spider_url").toString();
                String stock_audit_num = spider_url_detail.substring(spider_url_detail.lastIndexOf("=") ).replace("=", "");
               String spider_url_title = "http://query.sse.com.cn/commonSoaQuery.do?isPagination=true&sqlId=SH_XM_LB&stockAuditNum="+stock_audit_num;
               addCKBSpiderURL(spider_url_detail,map,page);
               addCKBSpiderURL(spider_url_title,map,page);
            }
            // 公司公告 http://www.sse.com.cn/star/disclosure/listannouncement/
            List<Query> query_list = new ArrayList<>();
            query_list.add(new Query(QueryType.EQ, "company_type", "医药企业"));
            List<Map<String, Object>> es_list = service.getList(ckb_es_index, null, null, null, -1, "stock_code");
            for(Map<String, Object> map :es_list){
                String stock_code = String.valueOf(map.get("stock_code"));
                if(StringUtils.isBlank(stock_code) || "null".equals(stock_code))
                    continue;
                long spider_wormtime = System.currentTimeMillis();
                long before_time = Long.valueOf(spider_wormtime) - Long.valueOf(86400*1000L*30);
                String begin_date = DateUtils.tampConvertUS(before_time);
                String end_date = DateUtils.tampConvertUS(spider_wormtime);
                page.addTargetRequest("http://query.sse.com.cn/security/stock/queryCompanyBulletin.do?jsonCallBack=jsonpCallback46399&" +
                        "securityType=120100%2C020100&reportType=ALL&beginDate="+begin_date+"&endDate="+end_date+"&productId="+stock_code);
            }
        }

        if(url.contains("sse.com.cn")){
            String results = page.getRawText();
            if(results.contains("({"))
                results = results.substring(results.indexOf("({")+1,results.lastIndexOf(")"));
            page.setRawText(results);
        }

        if(url.contains("query.sse.com.cn") && url.contains("beginDate=")){ // 科创板公司公告
            String stock_code = url.substring(url.lastIndexOf("=")).replace("=", "");
            String content = page.getRawText();
            content = content.substring(content.indexOf("{"),content.lastIndexOf(")"));
            JSONObject obj = JSONObject.fromObject(content);
            JSONArray data_arr = JSONArray.fromObject(JSONObject.fromObject(obj.get("pageHelp")).get("data"));
            String file_path = "/home/zengxiangxu/";
            for(int i=0;i<data_arr.size();i++){
                JSONObject data_obj = JSONObject.fromObject(data_arr.get(i));
                String title = data_obj.get("TITLE").toString();
                String pdf_url = "http://www.sse.com.cn"+data_obj.get("URL").toString().replace("\\","" );
                String spider_publish_time_str = data_obj.get("SSEDATE").toString();
                String esid = MD5Utils.getMD5(stock_code+pdf_url);
                Map<String, Object> es_map = service.getOne("news", esid, "title");
                if(es_map != null && es_map.size() == 2){
                    logger.info("------- 当前科创板公司公告已经采集，被过滤 -------- "+stock_code+"\t"+title);
                    continue;
                }
                Long spider_publish_time = DateUtils.transForMilliByTim(spider_publish_time_str, "yyyy-MM-dd");
                String md5 = MD5Utils.getMD5(pdf_url)+".pdf";
                if(FileDownloadUtils.downloadFromUrl(pdf_url,file_path,md5).equals("successful")) {
                    String qinniu_file_url = QiniuUtil.uploadQNFile(file_path + md5, false);
                    Map map = new HashMap<>();
                    map.put("title",title);
                    map.put("wechat_official_accounts",stock_code);
                    map.put("spider_publish_time",spider_publish_time);
                    map.put("spider_publish_time_str",spider_publish_time_str);
                    map.put("content",qinniu_file_url);
                    map.put("url",qinniu_file_url);
                    map.put("state","新增");
                    map.put("is_delete","否");
                    map.put("source","科创板");
                    map.put("channel_name","科创板");
                    map.put("spider_wormtime",System.currentTimeMillis());
                    logger.info("------- 存储科创板公司公告 ------- "+esid+"\t"+title);
                    service.insertOrUpdateFields("news", esid, map);
                }
            }
        }

        if(url.contains("pageNo=") && url.contains("query.sse.com.cn")) // 科创板申报情况—列表页
            parseTechnologicalInnovationTitle(page);

        if(!url.contains("pageNo=") && url.contains("query.sse.com.cn")) // 科创板申报情况—详情页
            parseCKBDetail(url,page);

        if(url.endsWith(".json") && !url.contains("lcisehk7relsdc")) // 港交所新上市公告_列表页
            parseHKListData(page);

        if(url.contains("lcisehk7relsdc")){ // 港交所上市文件监控、存储、预警
            JSONArray news_info_arr = JSONObject.fromObject(page.getRawText()).getJSONArray("newsInfoLst");
            for(int i=0;i<news_info_arr.size();i++){
                JSONObject news_info_obj = news_info_arr.getJSONObject(i);
                String title = String.valueOf(news_info_obj.get("lTxt"));
                String type = String.valueOf(news_info_obj.get("title"));
                String spider_publish_time_str = String.valueOf(news_info_obj.get("relTime")); //发布时间
                String original_url = "https://www1.hkexnews.hk"+String.valueOf(news_info_obj.get("webPath")); //发布时间
                if(!(type.equals("全球發售") && CommonUtils.removeLabel(title, false).equals("上市文件發售以供認購")))
                    continue;
                if(type.contains("多檔案"))
                    continue;
                JSONObject stock_obj = news_info_obj.getJSONArray("stock").getJSONObject(0);
                String stock_code = String.valueOf(stock_obj.get("sc"));//股份代码
                String stock_name = String.valueOf(stock_obj.get("sn"));//股份代码
                String[] split = spider_publish_time_str.split(" ");
                long spider_publish_time = DateUtils.transForMilliByTim(split[0],"dd/MM/yyyy" );
                String esid = MD5Utils.getMD5(original_url);
                if(service.getExist(hk_es_index,esid )){
                    logger.info("当前数据已采集，被过滤："+stock_code+"\t"+title);
                    continue;
                }
                Map<String, Object> es_map = new HashMap<>();
                es_map.put("title", stock_name+"："+title);
                es_map.put("wechat_official_accounts", stock_code);
                insertHKData(original_url,spider_publish_time,spider_publish_time_str,false,es_map,esid);
            }
        }
    }

    private void insertHKData(String url, long spider_publish_time, String spider_publish_time_str,boolean is_send_email,Map<String, Object> map,String esid) {
        String new_url = QiniuUtil.replacePDFURL(url);
        if(new_url.contains("spider.pharmcube.com")){
            map.put("spider_publish_time",spider_publish_time);
            map.put("spider_publish_time_str",spider_publish_time_str);
            map.put("content",new_url);
            map.put("url",new_url);
            map.put("state","新增");
            map.put("is_delete","否");
            map.put("source","港交所");
            map.put("channel_name","上市公司");
            map.put("spider_wormtime",System.currentTimeMillis());
            if(service.insertOrUpdateFields(hk_es_index, esid,map )){
                jedis.lpush("news_list",esid);
                if(is_send_email){
                    logger.info("------- insert es data success -------"+esid);
                    send_email_content += "<tr><td>"+map.get("title")+"</td><td>"+new_url+"</td></tr>"; //发送邮件给 甘小玉
                }
            }else
                logger.info("------- insert es data error -------"+esid);
        }
    }

    private void parseCKBDetail(String url, Page page) {
        if(url.contains("sqlId=SH_XM_LB")){ // 项目基本信息
            String results = page.getRawText();
            if(results.contains("({"))
                results = results.substring(results.indexOf("({")+1,results.lastIndexOf(")"));
            JSONObject obj = JSONObject.fromObject(JSONArray.fromObject(JSONObject.fromObject(JSONObject.fromObject(results).get("pageHelp")).get("data")).get(0));
            String company_name = "";
            if(JSONArray.fromObject(obj.get("stockIssuer")).size()>0)
                company_name = JSONObject.fromObject(JSONArray.fromObject(obj.get("stockIssuer")).get(0)).get("s_issueCompanyFullName").toString();
            else
                company_name = String.valueOf(obj.get("stockAuditName")).replace("首次公开发行股票并在科创板上市", ""); // 公司全称
            if(StringUtils.isBlank(company_name) || "null".equals(company_name)){
                logger.info("------- 当前采集页面无效，被过滤 ------- "+company_name+"\t"+url);
                return;
            }
            String company_abbreviation = String.valueOf(JSONObject.fromObject(JSONArray.fromObject(obj.get("stockIssuer")).get(0)).get("s_issueCompanyAbbrName")); // 公司简称
            String accept_date_str = obj.get("auditApplyDate").toString();
            String approval_status = String.valueOf(obj.get("currStatus"));//审核状态
            String registe_result = String.valueOf(obj.get("registeResult"));
            approval_status = standardSatus(approval_status,registe_result,obj);
            float financing_amount = Float.valueOf(obj.get("planIssueCapital").toString()); //融资金额(亿元)
            String sponsor_institution = "";
            sponsor_institution = parseJSONData(obj,sponsor_institution,"1"); //保荐机构
            String accounting_firm = "";
            accounting_firm = parseJSONData(obj,accounting_firm,"2"); //会计师事务所
            String law_office = "";
            law_office = parseJSONData(obj,law_office,"3"); //律师事务所
            String assessment_agency = "";
            assessment_agency = parseJSONData(obj,assessment_agency,"4"); //评估机构
            long spider_wormtime = System.currentTimeMillis();
            company_name = CommonUtils.standardCompanyNameEN(company_name);
            Long spider_update_date = convertDate(obj.get("updateDate").toString());
            String esid = "";
            String stock_audit_num = url.substring(url.lastIndexOf("=")+1);
            List<Query> query_list = new ArrayList<>();
            query_list.add(new Query(QueryType.EQ, "stock_audit_num",stock_audit_num));
            Map<String, Object> es_map = service.getOne(ckb_es_index, query_list, "spider_update_date", "approval_status");
            if(null != es_map)
                esid = es_map.get("esid").toString();
            else
                esid = MD5Utils.getMD5(url);
            checkFiledsESData(esid,ckb_es_index,"approval_status",approval_status,company_name);
            Map<String, Object> map = new HashMap<>();
            map.put("company_name", company_name);
            map.put("company_abbreviation", company_abbreviation);
            map.put("accept_date_str", accept_date_str);
            map.put("accept_date",  convertDate(accept_date_str));
            map.put("spider_update_date",  spider_update_date);
            map.put("approval_status", approval_status);
            map.put("financing_amount", financing_amount);
            map.put("sponsor_institution", sponsor_institution);
            map.put("accounting_firm", accounting_firm);
            map.put("law_office", law_office);
            map.put("stock_audit_num", stock_audit_num);
            map.put("assessment_agency", assessment_agency);
            map.put("spider_wormtime", spider_wormtime);
            if(service.insertOrUpdateFields(ckb_es_index, esid, map)){
                logger.info("------- insert es data success -------- "+esid+"\t"+company_name);
                if(null != es_map){
                    String approval_status_es = String.valueOf(es_map.get("approval_status"));
                    Long spider_update_date_es = Long.valueOf(String.valueOf(es_map.get("spider_update_date")));
                    if(spider_update_date_es.longValue() != spider_update_date.longValue() || !approval_status_es.equals(approval_status))
                        jedis.lpush("data_clean_stib",esid);
                }
            }else
                logger.info("------- insert es data error -------- "+esid+"\t"+company_name);
            Request request = new Request("http://query.sse.com.cn/commonSoaQuery.do?isPagination=false&sqlId=GP_GPZCZ_SHXXPL&stockAuditNum="+obj.get("stockAuditNum"));
            request.putExtra("esid", esid);
            request.putExtra("company_name", company_name);
            page.addTargetRequest(request);
        }

        if(url.contains("sqlId=GP_GPZCZ_SHXXPL")){
            String esid = page.getRequest().getExtra("esid").toString();
            String company_name = page.getRequest().getExtra("company_name").toString();
            JSONArray reveal_info = new JSONArray(); // 信息披露
            JSONArray inquiry = new JSONArray(); //  问询与回复
            JSONArray data_arr = JSONArray.fromObject(JSONObject.fromObject(JSONObject.fromObject(page.getRawText()).get("pageHelp")).get("data"));
            for(int i=0;i<data_arr.size();i++){
                JSONObject data_obj = JSONObject.fromObject(data_arr.get(i));
                String file_type = data_obj.get("fileType").toString();
                JSONObject object = new JSONObject();
                if(file_type.equals("30")){// 招股说明书 -- 申报稿
                    jsonData(data_obj,object,"declare_repprt_name","declare_repprt_url","招股说明书");
                    reveal_info.add(object);
                } else if(file_type.equals("36")) { // 发行保荐书 -- 申报稿
                    jsonData(data_obj,object,"declare_repprt_name","declare_repprt_url","发行保荐书");
                    reveal_info.add(object);
                } else if(file_type.equals("37")) { // 上市保荐书 -- 申报稿
                    jsonData(data_obj,object,"declare_repprt_name","declare_repprt_url","上市保荐书");
                    reveal_info.add(object);
                } else if(file_type.equals("32")){ // 审计报告 -- 申报稿
                    jsonData(data_obj,object,"declare_repprt_name","declare_repprt_url","审计报告");
                    reveal_info.add(object);
                }else if(file_type.equals("33")){ // 法律意见书
                    jsonData(data_obj,object,"declare_repprt_name","declare_repprt_url","法律意见书");
                    reveal_info.add(object);
                }else if(file_type.equals("6")){ // 问询与回复
                    jsonData(data_obj,object,"file_name","file_name_url","");
                    inquiry.add(object);
                }
            }
            checkFiledsESData(esid,ckb_es_index,"reveal_info",String.valueOf(reveal_info),company_name);
            String md5 =  MD5Utils.getMD5(String.valueOf(inquiry)+String.valueOf(reveal_info));
            Map<String, Object> es_map = service.getOne(ckb_es_index, esid, "md5");
            if(!String.valueOf(es_map.get("md5")).equals(md5)){
                Map<String, Object> map = new HashMap<>();
                map = mapData("inquiry",inquiry,map);
                map = mapData("reveal_info",reveal_info,map);
                map.put("md5", md5);
                map.put("spider_url", url);
                if(service.insertOrUpdateFields(ckb_es_index, esid, map)){
                    jedis.lpush("data_clean_stib",esid);
                    logger.info("------- insert es data success -------- "+esid+"\t"+company_name);
                } else
                    logger.info("------- insert es data error -------- "+esid+"\t"+company_name);
            }else
                logger.info("------- 监测数据未发生变化，被过滤 -------- "+esid+"\t"+company_name);
        }
    }

    private void checkFiledsESData(String esid, String ckb_es_index, String filed,String filed_value,String company_name) {
        //审核状态发生变更，用于后面发送邮件
        Map<String, Object> approval_status_map = service.getOne(ckb_es_index, esid, filed);
        if(null != approval_status_map && approval_status_map.containsKey(filed)){
            String approval_status_es = String.valueOf(approval_status_map.get(filed));
            if(!filed_value.equals(approval_status_es)){
                if(filed.equals("approval_status")){
                    logger.info("------- 科创版公司 '审核状态' 发生变更 -------- "+esid+"\t"+filed_value+"\t"+approval_status_es);
                    approval_status_set.add(company_name);
                }
            }
        }
    }

    private long convertDate(String date) {
        String accept_date_str = date.substring(0, 8); //受理日期
        return DateUtils.customizeConversionDate(accept_date_str,"yyyyMMdd");
    }

    public static void send_email(){
        ckbSendEmail(approval_status_set);
    }

    private static void ckbSendEmail(Set<String> set) {
        String send_email_content = "";
        for(String company_name : set)
            send_email_content += "<tr><td>"+company_name+"</td></tr>";
        if(StringUtils.isNotEmpty(send_email_content)){
            logger.info("------- 发送邮件给全佳 -------");
            String content = "<table border=\"1\"><tr><th>公司名称</th>"+send_email_content+"</tr></table>";
            List<String> send_email_list = new ArrayList<>();
            send_email_list.add("quanjia@pharmcube.com");
            send_email_list.add("lvmi@pharmcube.com");
            SendEmail.sendEmail(content,"科创版审核状态变更",null,false,send_email_list);
        }
    }

    private void addCKBSpiderURL(String spider_url, Map<String, Object> map, Page page) {
        Request request = new Request(spider_url);
        request.putExtra("esid", map.get("esid"));
        request.putExtra("company_name", map.get("company_name"));
        page.addTargetRequest(request);
    }

    private Map<String, Object> mapData(String key ,JSONArray prospectus, Map<String, Object> map) {
        if(prospectus.size()>0)
            map.put(key, prospectus);
        return map;
    }

    private void jsonData(JSONObject data_obj, JSONObject object, String declare_repprt_name, String declare_repprt_url,String reveal_file_type) {
        String file_url = "http://static.sse.com.cn/stock"+data_obj.get("filePath").toString().replace("\\", "");
        if(StringUtils.isNotEmpty(reveal_file_type))
            object.put("reveal_file_type", reveal_file_type);
        object.put(declare_repprt_name, data_obj.get("fileTitle").toString());
        object.put("update_date", DateUtils.convertTamp(data_obj.get("publishDate").toString()));
        object.put(declare_repprt_url, file_url);
    }

    private String parseJSONData(JSONObject obj, String data, String param_num) {
        JSONArray intermediary_arr = JSONArray.fromObject(obj.get("intermediary"));
        for(int i=0;i<intermediary_arr.size();i++){
            JSONObject object = JSONObject.fromObject(intermediary_arr.get(i));
            String intermediary_type = String.valueOf(object.get("i_intermediaryType"));
            if(intermediary_type.equals(param_num)){
                if(StringUtils.isNotEmpty(data))
                    data = data + ";"+object.get("i_intermediaryName");
                else
                    data = object.get("i_intermediaryName")+"";
            }
        }
        return data;
    }

    private String standardSatus(String status,String registe_result,JSONObject obj) {
        if(status.equals("1"))
            return "已受理";
        else if(status.equals("2"))
            return "已问询";
        else if(status.equals("3")){
            String subStatus = String.valueOf(obj.get("commitiResult"));
            if(subStatus.equals("1") )
                return "上市委会议通过";
            else if(subStatus.equals("2") )
                return "有条件通过";
            else if(subStatus.equals("3"))
                return "上市委会议未通过";
            else if(subStatus.equals("6"))
                return "暂缓审议";
            return "上市委会议";
        }else if(status.equals("4"))
            return "提交注册";
        else if(status.equals("5")){
            if(registe_result.equals( "1"))
                return "注册生效";
            else if(registe_result.equals("2"))
                return "不予注册";
            else if(registe_result.equals("3"))
                return "终止注册";
            return "注册结果";
        }else if(status.equals("6"))
            return "已发行";
        else if(status.equals("7"))
            return "中止";
        else if(status.equals("8"))
            return "终止";
        else
            return "-";
    }

    private void parseTechnologicalInnovationTitle(Page page) {
        JSONObject obj = JSONObject.fromObject(page.getRawText());
        JSONArray data_arr = JSONArray.fromObject(JSONObject.fromObject(obj.get("pageHelp")).get("data"));
        for(int i=0;i<data_arr.size();i++){
            JSONObject data_obj = JSONObject.fromObject(data_arr.get(i));
            page.addTargetRequest("http://query.sse.com.cn/commonSoaQuery.do?isPagination=true&sqlId=SH_XM_LB&stockAuditNum="+data_obj.get("stockAuditNum"));
        }
    }

    private void parseHKListData(Page page) {
        JSONObject obj = JSONObject.fromObject(page.getRawText());
        JSONArray app_arr = JSONArray.fromObject(obj.get("app"));
        for(int i=0;i<app_arr.size();i++){
            JSONObject app_obj = JSONObject.fromObject(app_arr.get(i));
            String company_name = app_obj.get("a").toString();
            String title = company_name;
            JSONObject ls_obj = JSONObject.fromObject(JSONArray.fromObject(app_obj.get("ls")).get(0));
            title += "_"+ls_obj.get("nF").toString();
            title += "（"+ls_obj.get("nS1").toString()+"）";
            String spider_publish_time_str = app_obj.get("d").toString();
            long spider_publish_time = DateUtils.transForMilliByTim(spider_publish_time_str,"dd/MM/yyyy" );
            spider_publish_time_str = DateUtils.tampConvertUS(spider_publish_time);
            String esid = MD5Utils.getMD5(spider_publish_time_str+company_name);
            Map<String, Object> es_map = service.getOne(hk_es_index, esid, "title");
            if(null != es_map)
                logger.info("------- 该数据已经采集过了，过滤中 -------"+esid+"\t"+company_name);
            else {
                String href = ls_obj.getString("u1");
                if(!href.startsWith("http"))
                    href = "https://www1.hkexnews.hk/app/"+href;
                Map map = new HashMap<>();
                map.put("title",title);
                insertHKData(href,spider_publish_time,spider_publish_time_str,true,map,esid);
            }
        }
        if(StringUtils.isNotEmpty(send_email_content)){
            logger.info("------- 发送邮件给甘小玉 -------");
            String content = "<table border=\"1\"><tr><th>标题</th><th>链接</th>"+send_email_content+"</tr></table>";
            List<String> send_email_list = new ArrayList<>();
            send_email_list.add("ganxiaoyu@pharmcube.com");
            send_email_list.add("quanjia@pharmcube.com");
            send_email_list.add("lvmi@pharmcube.com");
            send_email_list.add("dushu@pharmcube.com");
            SendEmail.sendEmail(content,"港交所资讯",null,false,send_email_list);
        }
    }

    @Override
    public Site getSite() {
        return site;
    }

    //public static void main(String[] args) {
    public static void execute() {
        convertPDFLinks();//转换pdf链接
        String url = "https://www.baidu.com";
        Spider.create(new IPONews()).addUrl(url).setDownloader(new ProxyHttpClientDownloaderABuYun()).thread(3).start();
    }

    private static void convertPDFLinks() {
        List<Query> query_list = new ArrayList<>();
        query_list.add(new Query(QueryType.EQ, "company_type", "医药企业"));
        List<Map<String, Object>> list = service.getList(ckb_es_index, query_list, null, null, -1, "reveal_info", "inquiry");
        for(Map<String, Object> map : list){
            JSONArray reveal_info_arr = new JSONArray();
            JSONArray inquiry_arr = new JSONArray();
            if(map.containsKey("reveal_info"))
                reveal_info_arr = replaceCKBPDFURL("reveal_info","declare_repprt_url",map,reveal_info_arr);
            if(map.containsKey("inquiry"))
                inquiry_arr = replaceCKBPDFURL("inquiry","file_name_url",map,inquiry_arr);
            Map<String, Object> map_es = new HashMap<>();
            String esid = map.get("esid").toString();
            if(reveal_info_arr.size()>0)
                map_es.put("reveal_info", reveal_info_arr);
            if(inquiry_arr.size()>0)
                map_es.put("inquiry", inquiry_arr);
            if(map_es.size()>0){
                logger.info("------- 替换PDF链接为七牛云链接 -------"+esid);
                if(service.insertOrUpdateFields(ckb_es_index, esid,map_es)){
                    logger.info("------- insert es data success -------"+esid);
                }else
                    logger.info("------- insert es data error -------"+esid);
            }
        }
    }

    private static JSONArray replaceCKBPDFURL(String reveal_info, String declare_repprt_url_str,Map<String, Object> map,JSONArray reveal_info_arr) {
        JSONArray reveal_info_arr_es = JSONArray.fromObject(map.get(reveal_info));
        for(int i=0;i<reveal_info_arr_es.size();i++){
            JSONObject obj = JSONObject.fromObject(reveal_info_arr_es.get(i));
            String declare_repprt_url = String.valueOf(obj.get(declare_repprt_url_str));
            if(declare_repprt_url.contains("spider.pharmcube.com") || !declare_repprt_url.startsWith("http"))//防止为空 或 null 情况
                continue;
            String new_pdf_url = QiniuUtil.replacePDFURL(declare_repprt_url);
            obj.put(declare_repprt_url_str, new_pdf_url);
            reveal_info_arr.add(obj);
        }
        return reveal_info_arr;
    }
}
