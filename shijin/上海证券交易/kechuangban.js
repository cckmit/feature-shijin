//审核状态转义 - 无超链接
var status_transfer=function(data){
    var status = data.currStatus;
    if(status == undefined) status = data.AUDIT_STATUS;
    var subStatus = data.commitiResult;
    var registeResult = data.registeResult;
    var sqlid = data.sqlId;
    if(!('collectType' in data)){
       return status_transfers(data);
    }else if(sqlid == 'GP_ZRZ_XMLB' || sqlid == 'GP_ZRZ_GGJG'){
     var suspendStatus = data.suspendStatus || '';
      if(status == "1"){
        return "已受理"
      }else if(status == "2"){
        return "已问询"
      }else if(status == "3"){
        return "已回复"
      }else if(status == "4"){
        return "通过"
      }else if(status == "5"){
        return "暂缓审议"
      }else if(status == "6"){
        return "未通过"
      }else if(status == "45"){
        return "提交注册"
      }else if(status == "46"){
        return "补充审核已问询"
      }else if(status == "47"){
        return "补充审核已回复"
      }else if(status == "50"){
        if(registeResult == "1"){
          return "注册生效"
        }else if(registeResult == "2"){
          return "不予注册"
        }else if(registeResult == "3"){
          return "终止注册"
        }else{
          return "注册结果";
        }
      }else if(status == "55"){
        if(suspendStatus == '1'){
          return "中止<p>（财报更新）</p>"
        }else if(suspendStatus == '2'){
          return "中止<p>（其他事项）</p>"
        }else{
          return "中止及<p>财报更新</p>";
        }
      }else if(status == "60"){
        return "终止"
      }else {
        return "-"
      }
    }else{
        if(status=="1"){
            return "已受理";
        }else if(status=="2"){
            return "已问询";
        }else if(status=="3"){
            if(subStatus == "1"){
                return "上市委会议<p>通过</p>";
            }else if(subStatus == "2"){
                return "有条件通过";
            }else if(subStatus == "3"){
                return "上市委会议<p>未通过</p>";
            }else if(subStatus == "6"){
                return "暂缓审议";
            }
            return "上市委会议";
        }else if(status=="4"){
            return "提交注册";
        }else if(status=="5"){
            if(registeResult == "1"){
                return "注册生效";
            }else if(registeResult == "2"){
                return "不予注册";
            }else if(registeResult == "3"){
            return "终止注册";
            }
            return "注册结果";
        }else if(status=="6"){
            return "已发行";
        }else if(status=="7"){
            var suspendStatus = data.suspendStatus || '';
            if(suspendStatus == "1"){
                return "中止<p>（财报更新）</p>"
            }else if(suspendStatus == "2"){
                return "中止<p>（其他事项）</p>"
            }else{
                return "中止<p>及财报更新</p>";
            }
        }else if(status=="8"){
            return "终止";
        }else if(status=="9"){
            if(subStatus == "4"){
                return "复审委会议<p>通过</p>";
            }else if(subStatus == "5"){
                return "复审委会议<p>未通过</p>";
            }
            return "复审委会议";
        }else if(status == "10"){
            return "补充审核";
        }else{return "-";}
    }
  }
  function status_transfers(data) {
    var status = data.currStatus;
    if(status == undefined) status = data.AUDIT_STATUS;
    var registeResult = data.registeResult;
    if(status=="1"){
        return "已受理";
    }else if(status=="2"){
        return "已问询";
    }else if(status=="3"){
        return "已回复";
    }else if(status=="4"){
        return "通过";
    }else if(status=="5"){
        return "-";
    }else if(status=="6"){
        return "未通过";
    }else if(status=="45"){
        return "提交注册";
    }else if(status == "46"){
        return "补充审核已问询"
    }else if(status == "47"){
        return "补充审核已回复"
    }else if(status=="50"){
        if(registeResult == "1"){
            return "注册生效"
        }else if(registeResult == "2"){
            return "不予注册"
        }else if(registeResult == "3"){
            return "终止注册"
        }
        return "注册结果";
    }else if(status=="55"){
        return "中止";
    }else if(status == "60"){
        return "终止";
    }else{return "-";}
  }
  //审核状态转义 - 有超链接   
  var status_transfer_link = function(data){
    var type = data.s_companyCode ? 1:0;
    var result = status_transfer(data);
    if(result == "-"){
        return result;
    }
    if(type == 0){
        return '<a href="/renewal/xmxq/index.shtml?auditId=' + data.stockAuditNum + '&anchor_type='+ type + '" target="_blank">' + result + '</a>';
    }else{
        return result;
    }
  }
  
  var area_transfer = function(data) {
    var area = data.stockIssuer[0].s_province;
    var type = data.s_companyCode ? 1:0;
    var areaStr = "";
    areaStr += '<a href="/renewal/xmxq/index.shtml?auditId=' + data.stockAuditNum + '&anchor_type='+ type + '" target="_blank">' + area + '</a>';
    return areaStr;
  }
  
  var csrc_transfer = function(data) {
    var csrc = data.stockIssuer[0].s_csrcCodeDesc;
    var type = data.s_companyCode ? 1:0;
    var csrcStr = "";
    var len = csrc.length;
    var showName = csrc;
    if((len % 6) >= 1 && (len % 6) <= 2){
        if(/制造业$/.test(csrc) || /制品业$/.test(csrc) || /加工业$/.test(csrc) || /服务业$/.test(csrc) || /建筑业$/.test(csrc)){
            showName = csrc.substring(0, len - 3) + "<br/>" + csrc.substring(len - 3);
        }else if(/发展$/.test(csrc)){
            showName = csrc.substring(0, len - 2) + "<br/>" + csrc.substring(len - 2);
        }
    }
    csrcStr += '<a href="/renewal/xmxq/index.shtml?auditId=' + data.stockAuditNum+ '&anchor_type='+ type  + '" target="_blank">' + showName + '</a>'; 
    return csrcStr;
  }
  
  var csrc_transfer_normal = function(data) {
    var csrc = data.stockIssuer[0].s_csrcCodeDesc;
    var csrcStr = "";
    var len = csrc.length;
    var showName = csrc;
    if((len % 6) >= 1 && (len % 6) <= 2){
        if(/制造业$/.test(csrc) || /制品业$/.test(csrc) || /加工业$/.test(csrc) || /服务业$/.test(csrc) || /建筑业$/.test(csrc)){
            showName = csrc.substring(0, len - 3) + "<br/>" + csrc.substring(len - 3);
        }else if(/发展$/.test(csrc)){
            showName = csrc.substring(0, len - 2) + "<br/>" + csrc.substring(len - 2);
        }
    }
    return showName;
  }
  
  var date_transfer = function(data) {
    var date = data.fileUpdateTime||data.fileUpdTime;
    if(date)
        return date.substring(0,4) + "-" + date.substring(4,6) + "-" + date.substring(6,8);
    else
        return '';
  }
  
  var date_transfer_sub = function(data) {
    var date = data.fileUpdTime;
    var pldate = date.substring(0,4) + "-" + date.substring(4,6) + "-" + date.substring(6,8);
    return pldate;
  }
  
  //融资类型1
  var stock_type_transfer=function(data){
    var type = data.collectType;
    if(type == undefined) type = data.STOCK_TYPE;
    if(type=="1"){
        return "首发";
    }else if(type=="2"){
        return "配股";
    }else if(type=="3"){
        return "增发";
    }else if(type=="4"){
        return "可转债";
    }else if(type=="5"){
        return "优先股";
    }else if(type=="6"){
        return "非公开";
    }else if(type=="7"){
        return "其他";
    }else{
        return "-";
    }
  }
  
  
  //融资类型2
  var stock_type_transfer1=function(data){
    var stockType = data.collectType;
    if(stockType == undefined) stockType = data.STOCK_TYPE;
  
    var offerType = data.offerType;
    if(offerType == undefined) offerType = data.OFFER_TYPE;
  
    if(offerType=="1"){     
        return "首发";
    }else if(offerType=="2"){
  
        if(stockType=="1"){
            return "再融资(首发)";
        }else if(stockType=="2"){
            return "再融资(配股)";
        }else if(stockType=="3"){
            return "再融资(增发)";    
        }else if(stockType=="4"){
            return "再融资(可转债)";
        }else if(stockType=="5"){
            return "再融资(优先股)";
        }else if(stockType=="6"){
            return "再融资(非公开)";
        }else if(stockType=="7"){
            return "再融资(其他)";
        }
    }else{
        return "-";
    }
  }
  
  var  market_type_transfer=function(data){
    var marketType = data.issueMarketType;
    if(marketType == undefined) marketType = data.MARKET_TYPE;
    if(marketType == "3"){
        return "科创板";
    }else{
        return "-";
    }
  }
  
  var publics = {};
  publics.BJType = "1"; //保荐机构
  publics.personType = {"1":["22","23"],"2":["32","33","34","35"],"3":["42","43","44","45"],"4":["52","53","54"]};
  
  //中介机构公司名称拼接和加链接  type-中介机构类型   nameType-全称还是简称  separator-分隔符
  publics.companyLink = function(oldtype,nameType,separator,obj){
    var type;
    var contentLink = function(data){
        if((data.businessSubType != undefined && obj && typeof obj === 'object') || ((data.sqlId == 'GP_ZRZ_GGJG' || data.sqlId == 'GP_ZRZ_XMLB') && obj && typeof obj === 'object')){
            type = obj.type;
            nameType = obj.nameType;
        }else{
            type = oldtype;
        }
        var baseUrl = '';
        var kind = '';
        if(data.sqlId == 'GP_BGCZ_XMLB' || data.sqlId == 'GP_BGCZ_SSWHYGGJG' || obj == 'bgcz'){
            baseUrl = '/renewal/bjjg/index_bgcz.shtml';
            kind = 1;
        }else if(data.sqlId == 'SH_XM_LB' || data.sqlId == 'GP_GPZCZ_SHXXPL' || data.sqlId == 'GP_GPZCZ_SSWHYGGJG' || obj == 'fxss'){
            baseUrl = '/renewal/bjjg/index.shtml';
            kind = 0;
        }else if(data.sqlId == 'GP_ZRZ_XMLB' || data.sqlId == 'GP_ZRZ_GGJG' || obj == 'refund'){
            baseUrl = '/renewal/bjjg/index_refund.shtml';
        }
        var companies = data.intermediary;
        if(companies == undefined || companies == null || companies.length == 0) return "-";
        var flag = false;
        var htmlArr = new Array();
        var companyIds = new Array();
        for(var i = 0; i < companies.length; i++){
            if($.inArray(companies[i].i_intermediaryId,companyIds) > -1) continue;
            companyIds.push(companies[i].i_intermediaryId);
  
            if(companies[i].i_intermediaryType == type){
                flag = true;
                var showName = companies[i].i_intermediaryAbbrName;
                if(nameType == "2") showName = companies[i].i_intermediaryName;
                if(nameType == "3"){
                    showName = companies[i].i_intermediaryName;
                    if(showName != null && showName != ""){
                        if(type == publics.BJType){ // type==1 "保荐机构"
                            var showHtml = showName;
                            if(showName.length <= 12){
                                showHtml = showName;
                            }else if(12<showName.length && showName.length<=18 && /股份有限公司$/.test(showName)){
                                groupName = showName.substring(0,showName.length-6);
                                suffix = showName.substring(showName.length-6,showName.length);
                                showHtml = groupName + "<br/>" + suffix;
                            }else if(12<showName.length && showName.length<=18 && /有限责任公司$/.test(showName)){
                                groupName = showName.substring(0,showName.length-6);
                                suffix = showName.substring(showName.length-6,showName.length);
                                showHtml = groupName + "<br/>" + suffix;
                            }else if(12<showName.length && showName.length<=16 && /有限公司$/.test(showName)){
                                groupName = showName.substring(0,showName.length-4);
                                suffix = showName.substring(showName.length-4,showName.length);
                                showHtml = groupName + "<br/>" + suffix;
                            }else if(12<showName.length && showName.length<=24){
                                groupName = showName.substring(0,showName.length/2);
                                suffix = showName.substring(showName.length/2,showName.length);
                                showHtml = groupName + "<br/>" + suffix;
                            }else{
                                showHtml = showName;
                            }
                            htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName +'&anchor_type=' + kind + '" target="_blank" style="text-decoration:underline;">' + showHtml + '</a>');
                        }else{
                            if(type=="2" && 10<showName.length && showName.length<=18 && /（特殊普通合伙）$/.test(showName)){ // "（特殊普通合伙）"换行展示
                                groupName = showName.substring(0,showName.length-8);
                                suffix = showName.substring(showName.length-8,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName +'&anchor_type=' + kind + '&interType=' + type + '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type=="2" && 10<showName.length && showName.length<=16 && /会计师事务所$/.test(showName)){
                                groupName = showName.substring(0,showName.length-6);
                                suffix = showName.substring(showName.length-6,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type=="3" && 10<=showName.length && showName.length<=16 && /会计师事务所$/.test(showName) && obj === 'bgcz'){
                                groupName = showName.substring(0,showName.length-6);
                                suffix = showName.substring(showName.length-6,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type=="3" && 8<showName.length && showName.length<=11 && /事务所$/.test(showName) && !/律师事务所$/.test(showName) && obj !== 'bgcz'){
                                groupName = showName.substring(0,showName.length-3);
                                suffix = showName.substring(showName.length-3,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type=="3" && 8<showName.length && showName.length<=13 && /律师事务所$/.test(showName)){
                                groupName = showName.substring(0,showName.length-5);
                                suffix = showName.substring(showName.length-5,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type=="2" && 8<showName.length && showName.length<=13 && /律师事务所$/.test(showName)){
                                groupName = showName.substring(0,showName.length-5);
                                suffix = showName.substring(showName.length-5,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type=="2" && 8<=showName.length && showName.length<=13 && /律师事务所$/.test(showName)){
                                groupName = showName.substring(0,showName.length-5);
                                suffix = showName.substring(showName.length-5,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type == "4" && 10<showName.length && showName.length<=20 && /有限责任公司$/.test(showName)){
                                groupName = showName.substring(0,showName.length - 6);
                                suffix = showName.substring(showName.length - 6,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type == "4" && 10<showName.length && showName.length<=20 && /事务所$/.test(showName)){
                                groupName = showName.substring(0,showName.length - 3);
                                suffix = showName.substring(showName.length - 3,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else if(type == "4" && 10<showName.length && showName.length<16 && /有限公司$/.test(showName)){
                                groupName = showName.substring(0,showName.length - 4);
                                suffix = showName.substring(showName.length - 4,showName.length);
                                showName = groupName + "<br/>" + suffix;
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }else{
                                htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                            }
                        }
                    }
                }else{
                    if(showName != null && showName != ""){
                        if(type == publics.BJType){
                            htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                        }else{
                            htmlArr.push('<a href="'+baseUrl+'?inter_id=' + companies[i].i_intermediaryId + '&inter_name=' + companies[i].i_intermediaryName + '&interType=' + type +'&anchor_type=' + kind+ '" target="_blank" style="text-decoration:underline;">' + showName + '</a>');
                        }
                    }  
                }
                             
            }
        }
        if(flag)  return htmlArr.join(separator);
        return "-";
    };
    return contentLink;
  };
  
  //中介机构人员名称拼接  separator--拼接分隔符
  publics.personLink = function(type,separator){
    if(separator == undefined || separator == null || separator =="") separator = " ";
    var contentLink = function(data){
        var companies = data.intermediary;
        if(companies == undefined || companies == null || companies.length == 0) return "-";
        
        var htmlArrAll = new Array();
        var companyIds = new Array();
        for(var i in companies){
            if($.inArray(companies[i].i_intermediaryId,companyIds) > -1) continue;
            companyIds.push(companies[i].i_intermediaryId);
            var htmlArr = new Array();
            var persons = companies[i].i_person;
            if(persons == undefined || persons == null || persons.length == 0) continue;
            for(var j in persons){
                if($.inArray(String(persons[j].i_p_jobType),publics.personType[type]) > -1){
                    if(String(persons[j].i_p_jobType).substring(1,2) == 2){
                        htmlArr[0] = persons[j].i_p_personName;
                    }else if(String(persons[j].i_p_jobType).substring(1,2) == 3){
                        htmlArr[1] = persons[j].i_p_personName;
                    }else if(String(persons[j].i_p_jobType).substring(1,2) == 4){
                        htmlArr[2] = persons[j].i_p_personName;
                    }else if(String(persons[j].i_p_jobType).substring(1,2) == 5){
                        htmlArr[3] = persons[j].i_p_personName;
                    }
                    //htmlArr.push(persons[j].i_p_personName);
                }
            }
            if(htmlArr.length > 0) htmlArrAll.push(htmlArr.join(separator));
        }
        var separatorC = separator;
        if(separator.indexOf("<br/>") < 0) separatorC += "<br/>";
        if(htmlArrAll.length > 0)  return htmlArrAll.join(separatorC);
        return "-";
    };
    return contentLink;
  };
  publics.personLinks = function(type, separator) {
    if (separator == undefined || separator == null || separator == "") separator = " ";
    var contentLink = function(data) {
        var companies = data.intermediary;
        if (companies == undefined || companies == null || companies.length == 0) return "-";
  
        var htmlArrAll = new Array();
        var companyIds = new Array();
        // var htmlArr = ''
        for (var i in companies) {
            if ($.inArray(companies[i].i_intermediaryId, companyIds) > -1) continue;
            companyIds.push(companies[i].i_intermediaryId);
            var htmlArr = [];
            var persons = companies[i].i_person;
            //var persons = uniqueArray(companies[i].i_person,'i_p_jobType');
            //persons.sort(compare('i_p_jobType'));
            var k = companies[i].i_intermediaryType;
            if (persons == undefined || persons == null || persons.length == 0) continue;
            for (var j in persons) {
                // if ($.inArray(String(persons[j].i_p_jobType), publics.personType[type]) > -1) {
                // i_intermediaryType
                if (k == 1 && type == 1) {
                    if (persons[j].i_p_jobType == 21) {
                        
                        htmlArr.push(persons[j].i_p_personName)
                    }
                }
                if (k == 2 && type == 2) {
                    if (persons[j].i_p_jobType == 61) {
                        htmlArr.push(persons[j].i_p_personName)
                    }
                }
                if (k == 3 && type == 3) {
                    if (persons[j].i_p_jobType == 41) {
                        htmlArr.push(persons[j].i_p_personName)
                    }
                }
                if (k == 4 && type == 4) {
                    if (persons[j].i_p_jobType == 81) {
                        htmlArr.push(persons[j].i_p_personName)
                    }
                }
  
  
  
                //htmlArr.push(persons[j].i_p_personName);
                // }
            }
            if (htmlArr.length > 0) htmlArrAll.push(htmlArr.join(separator));
        }
        var separatorC = separator;
        if (separator.indexOf("<br/>") < 0) separatorC += "<br/>";
        if (htmlArrAll.length > 0) return htmlArrAll.join(separatorC);
        return "-";
    };
    return contentLink;
  };
  publics.getBussinesType = function() {
    var type = '',
        strType = '';
    var contentLink = function(data) {
        type = data.bussinesType;
        if (type == 1) {
            strType = '发行股份<br />购买资产';
        } else if (type == 2) {
            strType = '小额快速<br>重组';
        } else if (type == 3) {
            strType = '重组上市';
        } else {
            strType = '-';
        }
        return strType;
    };
    return contentLink;
  }
  //发行人公司名称信息拼接
  publics.issuerType = function(type){
    var dataType = arguments[2];
    var contentLink = function(data){
        var kind = '',baseUrl = '';
        if(data.sqlId == 'GP_BGCZ_XMLB' || data.sqlId == 'GP_BGCZ_SSWHYGGJG' || dataType == 'bgcz'){
            baseUrl = '/renewal/xmxq/index_bgcz.shtml';
            kind = 1;
        }else if(data.sqlId == 'SH_XM_LB' || data.sqlId == 'GP_GPZCZ_SHXXPL' || data.sqlId == 'GP_GPZCZ_SSWHYGGJG' ||dataType == 'fxss'){
            baseUrl = '/renewal/xmxq/index.shtml';
            kind = 0;
        }else if(data.sqlId == 'GP_ZRZ_XMLB' || data.sqlId == 'GP_ZRZ_GGJG' || dataType == 'refund'){
            baseUrl = '/renewal/xmxq/index_refund.shtml';
            kind = 2;
        }
        var issuers = data.stockIssuer;
        if(issuers == undefined || issuers == null || issuers.length == 0) return "-";
        var issuerIds = new Array();
        var htmlArr = new Array();
        for(var i = 0; i < issuers.length; i++){
            //发行人信息重复不做处理
            if($.inArray(issuers[i].s_stockIssueId,issuerIds) > -1) continue;
            issuerIds.push(issuers[i].s_stockIssueId);
            var bussinesType = '';
            if('bussinesType' in data){
                bussinesType = '&bussinesType=' + data.bussinesType;
            }else{
                bussinesType = '';
            }
            if(type == "0"){ //公司全称 - 无超链接
                htmlArr.push(issuers[i].s_issueCompanyFullName);
            }else if(type == "1"){ //公司全称
                htmlArr.push('<a href="/renewal/fxr/index.shtml?issuer_id=' + issuers[i].s_stockIssueId + '&issuer_name=' + issuers[i].s_issueCompanyFullName+'" target="_blank" style="text-decoration:underline;">' + issuers[i].s_issueCompanyFullName + '</a>');
            }else if(type == "2"){ //公司简称
                var issuer_sec = issuers[i].s_issueCompanyAbbrName;
                if(data.offerType == "2" && issuers[i].s_companyCode != null && issuers[i].s_companyCode != "-") issuer_sec += "<br/>(" + issuers[i].s_companyCode + ")";
                htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum +  bussinesType + '&anchor_type=' + kind + '" target="_blank">' + issuer_sec + '</a>');
            }else if(type == "3"){ //公司全称
                var issuer_sec = issuers[i].s_issueCompanyFullName;
                if(data.offerType == "2" && issuers[i].s_companyCode != null && issuers[i].s_companyCode != "-") issuer_sec += "<br/>(" + issuers[i].s_companyCode + ")";
                htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum +  bussinesType + '&anchor_type=' + kind + '" target="_blank">' + issuer_sec + '</a>');
            }else if(type == "4"){ //公司全称折行
                var issuer_sec = issuers[i].s_issueCompanyFullName;
                if(15<issuer_sec.length && issuer_sec.length<=21 && /股份有限公司$/.test(issuer_sec)){
                    groupName = issuer_sec.substring(0,issuer_sec.length-6);
                    if(data.offerType == "2" && issuers[i].s_companyCode != null && issuers[i].s_companyCode != "-") issuer_sec += "<br/>(" + issuers[i].s_companyCode + ")";
                    htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum + '&anchor_type=' + kind + '" target="_blank">' + groupName + '<br/>股份有限公司</a>');
                }else if(15<issuer_sec.length && issuer_sec.length<=21 && /科技股份公司$/.test(issuer_sec)){
                    groupName = issuer_sec.substring(0,issuer_sec.length-6);
                    if(data.offerType == "2" && issuers[i].s_companyCode != null && issuers[i].s_companyCode != "-") issuer_sec += "<br/>(" + issuers[i].s_companyCode + ")";
                    htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum + '&anchor_type=' + kind + '" target="_blank">' + groupName + '<br/>科技股份公司</a>');
                }else if(15<issuer_sec.length && issuer_sec.length<=30){
                    groupName = issuer_sec.substring(0,issuer_sec.length/2);
                    groupSubName = issuer_sec.substring(issuer_sec.length/2,issuer_sec.length);
                    if(data.offerType == "2" && issuers[i].s_companyCode != null && issuers[i].s_companyCode != "-") issuer_sec += "<br/>(" + issuers[i].s_companyCode + ")";
                    htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum + '&anchor_type=' + kind + '" target="_blank">' + groupName + '<br/>' + groupSubName + '</a>');
                }else{
                    if(data.offerType == "2" && issuers[i].s_companyCode != null && issuers[i].s_companyCode != "-") issuer_sec += "<br/>(" + issuers[i].s_companyCode + ")";
                    htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum + '&anchor_type=' + kind + '" target="_blank">' + issuer_sec + '</a>');
                }
            }else if (type == "5") { //公司代码
                //htmlArr.push('<a href="/renewal/fxr/index.shtml?issuer_id=' + issuers[i].s_stockIssueId + '" target="_blank" style="text-decoration:underline;">' + issuers[i].s_companyCode + '</a>');
            } else if (type == "6") { //公司代码   新需求修改
                htmlArr.push('<a href="'+baseUrl+'?auditId=' + data.stockAuditNum + '&anchor_type=' + kind  + bussinesType + '" target="_blank" style="text-decoration:underline;">' + issuers[i].s_companyCode + '</a>');
            }
        }
  
        if(htmlArr.length > 0) return htmlArr.join("<br/>");
        return "-";
    }
    return contentLink;
  }
  
  //发行日期格式化
  publics.dateTrans = function(codeName,len){
    var contentLink = function(data){
        var date = data[codeName];
        if(date == undefined || date == null || date == "" || date == "-") return "-";
        return date.substring(0,4) + "-" + date.substring(4,6) + "-" + date.substring(6,8);
    }
    return contentLink;
  }
  
