# coding=utf-8
import scrapy
import psycopg2
import pymongo
import xlrd
import os
import time
import datetime
from time import strftime
from flash_news.utils import es_utils
from flash_news.utils.md5_utils import MD5Utils
from flash_news import const
from flash_news.const import ESIndex
from flash_news.utils.es_utils import Query, QueryType

# 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['spider_py']
table_name = mdb['nct']

conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5433")
cur=conn.cursor()

class Doctor(scrapy.Spider):
    md5_utils = MD5Utils()
    name = 'global_clinic'
    connection = psycopg2.connect(database="aact",user="yunheqin", password="wap18317129867",host="aact-db.ctti-clinicaltrials.org", port="5432")
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    cursor4 = connection.cursor()
    cursor5 = connection.cursor()
    cursor6 = connection.cursor()
    cursor7 = connection.cursor()
    cursor8 = connection.cursor()
    cursor9 = connection.cursor()
    cursor10 = connection.cursor()
    cursor11 = connection.cursor()
    cursor12 = connection.cursor()
    cursor13 = connection.cursor()
    cursor14 = connection.cursor()
    cursor15 = connection.cursor()
    cursor16 = connection.cursor()
    cursor17 = connection.cursor()
    cursor18 = connection.cursor()
    cursor19 = connection.cursor()
    cursor20 = connection.cursor()
    cursor21 = connection.cursor()
    cursor22 = connection.cursor()
    cursor23 = connection.cursor()
    cursor24 = connection.cursor()
    cursor25 = connection.cursor()
    cursor26 = connection.cursor()
    cursor27 = connection.cursor()
    cursor28 = connection.cursor()
    cursor29 = connection.cursor()
    cursor30 = connection.cursor()
    cursor31 = connection.cursor()
    cursor32 = connection.cursor()
    cursor33 = connection.cursor()
    cursor34 = connection.cursor()
    cursor35 = connection.cursor()
    cursor36 = connection.cursor()
    cursor37 = connection.cursor()
    cursor38 = connection.cursor()
    cursor39 = connection.cursor()
    cursor40 = connection.cursor()
    cursor41 = connection.cursor()
    cursor42 = connection.cursor()
    cursor43 = connection.cursor()
    cursor44 = connection.cursor()
    cursor45 = connection.cursor()
    cursor46 = connection.cursor()

    # 打开文件
    data = xlrd.open_workbook("D:\software\百度下载\全球临床.xlsx")
    # 查看工作表
    data.sheet_names()
    # 通过文件名获得工作表,获取工作表1
    table = data.sheet_by_name('Sheet1')
    nct_id_ll = table.col_values(0)

    for nct_id in nct_id_ll:
        if len(nct_id) == 0:
            break
        ## 执行SQL语句1
        cursor1.execute("SELECT * FROM documents where nct_id ='%s'"%nct_id)
        data = cursor1.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['document_id'] = i[2]
            dd['document_type'] = i[3]
            dd['url'] = i[4]
            dd['comment'] = i[5]
            d.setdefault('documents', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        # es_utils.insert_or_replace('nct', d=all_dict)
        table_name.insert(all_dict)
        print(all_dict)

        ## 执行SQL语句2
        cursor2.execute("SELECT * FROM categories where nct_id ='%s'"%nct_id)
        data = cursor2.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['name'] = i[2]
            dd['created_at'] = i[3]
            dd['updated_at'] = i[4]
            dd['grouping'] = i[5]
            dd['study_search_id'] = i[6]
            d.setdefault('categories', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句3
        cursor3.execute("SELECT * FROM study_references where nct_id ='%s'" % nct_id)
        data = cursor3.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['pmid'] = i[2]
            dd['reference_type'] = i[3]
            dd['citation'] = i[4]
            d.setdefault('study_references', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句4
        cursor4.execute("SELECT * FROM studies where nct_id ='%s'" % nct_id)
        data = cursor4.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['nlm_download_date_description'] = i[1]
            if i[2] != None:
                dd['study_first_submitted_date'] =i[2].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[3] != None:
                dd['results_first_submitted_date'] = i[3].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[4] != None:
                dd['disposition_first_submitted_date'] = i[4].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[5] != None:
                dd['last_update_submitted_date'] = i[5].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[6] != None:
                dd['study_first_submitted_qc_date'] = i[6].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[7] != None:
                dd['study_first_posted_date'] = i[7].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['study_first_posted_date_type'] = i[8]
            if i[9] != None:
                dd['results_first_submitted_qc_date'] = i[9].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[10] != None:
                dd['results_first_posted_date'] = i[10].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['results_first_posted_date_type'] = i[11]
            if i[12] != None:
                dd['disposition_first_submitted_qc_date'] = i[12].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[13] != None:
                dd['disposition_first_posted_date'] = i[13].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['disposition_first_posted_date_type'] = i[14]
            if i[15] != None:
                dd['last_update_submitted_qc_date'] = i[15].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[16] != None:
                dd['last_update_posted_date'] = i[16].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['last_update_posted_date_type'] = i[17]
            dd['start_month_year'] = i[18]
            dd['start_date_type'] = i[19]
            if i[20] != None:
                dd['start_date'] = i[20].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['verification_month_year'] = i[21]
            if i[22] != None:
                dd['verification_date'] = i[22].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['completion_month_year'] = i[23]
            dd['completion_date_type'] = i[24]
            if i[25] != None:
                dd['completion_date'] = i[25].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['primary_completion_month_year'] = i[26]
            dd['primary_completion_date_type'] = i[27]
            if i[28] != None:
                dd['primary_completion_date'] = i[28].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['target_duration'] = i[29]
            dd['study_type'] = i[30]
            dd['acronym'] = i[31]
            dd['baseline_population'] = i[32]
            dd['brief_title'] = i[33]
            dd['official_title'] = i[34]
            dd['overall_status'] = i[35]
            dd['last_known_status'] = i[36]
            dd['phase'] = i[37]
            dd['enrollment'] = i[38]
            dd['enrollment_type'] = i[39]
            dd['source'] = i[40]
            dd['limitations_and_caveats'] = i[41]
            dd['number_of_arms'] = i[42]
            dd['number_of_groups'] = i[43]
            dd['why_stopped'] = i[44]
            dd['has_expanded_access'] = i[45]
            dd['expanded_access_type_individual'] = i[46]
            dd['expanded_access_type_intermediate'] = i[47]
            dd['expanded_access_type_treatment'] = i[48]
            dd['has_dmc'] = i[49]
            dd['is_fda_regulated_drug'] = i[50]
            dd['is_fda_regulated_device'] = i[51]
            dd['is_unapproved_device'] = i[52]
            dd['is_ppsd'] = i[53]
            dd['is_us_export'] = i[54]
            dd['biospec_retention'] = i[55]
            dd['biospec_description'] = i[56]
            dd['ipd_time_frame'] = i[57]
            dd['ipd_access_criteria'] = i[58]
            dd['ipd_url'] = i[59]
            dd['plan_to_share_ipd'] = i[60]
            dd['plan_to_share_ipd_description'] = i[61]
            if i[62] != None:
                dd['created_at'] = i[62].strftime('%Y-%m-%d %H:%M:%S')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            if i[63] != None:
                dd['updated_at'] = i[63].strftime('%Y-%m-%d %H:%M:%S')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            d.setdefault('studies', []).append(dd)

        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)

        # sql = 'insert into nct(nct_id,table_content)values(%s,%s)'
        # cur.execute(sql,(nct_id,d))
        # conn.commit()
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句5
        cursor5.execute("SELECT * FROM sponsors where nct_id ='%s'" % nct_id)
        data = cursor5.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['agency_class'] = i[2]
            dd['lead_or_collaborator'] = i[3]
            dd['name'] = i[4]
            d.setdefault('sponsors', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句6
        cursor6.execute("SELECT * FROM result_groups where nct_id ='%s'" % nct_id)
        data = cursor6.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['ctgov_group_code'] = i[2]
            dd['result_type'] = i[3]
            dd['title'] = i[4]
            dd['description'] = i[5]
            d.setdefault('result_groups', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句7
        cursor7.execute("SELECT * FROM result_contacts where nct_id ='%s'" % nct_id)
        data = cursor7.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['organization'] = i[2]
            dd['name'] = i[3]
            dd['phone'] = i[4]
            dd['email'] = i[5]
            d.setdefault('result_contacts', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句8
        cursor8.execute("SELECT * FROM result_agreements where nct_id ='%s'" % nct_id)
        data = cursor8.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['pi_employee'] = i[2]
            dd['agreement'] = i[3]
            dd['restriction_type'] = i[4]
            dd['other_details'] = i[5]
            dd['restrictive_agreement'] = i[6]
            d.setdefault('result_agreements', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句9
        cursor9.execute("SELECT * FROM responsible_parties where nct_id ='%s'" % nct_id)
        data = cursor9.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['responsible_party_type'] = i[2]
            dd['name'] = i[3]
            dd['title'] = i[4]
            dd['organization'] = i[5]
            dd['affiliation'] = i[6]
            d.setdefault('responsible_parties', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句10
        cursor10.execute("SELECT * FROM reported_events where nct_id ='%s'" % nct_id)
        data = cursor10.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['result_group_id'] = i[2]
            dd['ctgov_group_code'] = i[3]
            dd['time_frame'] = i[4]
            dd['event_type'] = i[5]
            dd['default_vocab'] = i[6]
            dd['default_assessment'] = i[7]
            dd['subjects_affected'] = i[8]
            dd['subjects_at_risk'] = i[9]
            dd['description'] = i[10]
            dd['event_count'] = i[11]
            dd['organ_system'] = i[12]
            dd['adverse_event_term'] = i[13]
            dd['frequency_threshold'] = i[14]
            dd['vocab'] = i[15]
            dd['assessment'] = i[16]
            d.setdefault('reported_events', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句11
        cursor11.execute("SELECT * FROM reported_event_totals where nct_id ='%s'" % nct_id)
        data = cursor11.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['ctgov_group_code'] = i[2]
            dd['event_type'] = i[3]
            dd['classification'] = i[4]
            dd['subjects_affected'] = i[5]
            dd['subjects_at_risk'] = i[6]
            dd['created_at'] = i[7]
            dd['updated_at'] = i[8]
            d.setdefault('reported_events_totals', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句12
        cursor12.execute("SELECT * FROM provided_documents where nct_id ='%s'" % nct_id)
        data = cursor12.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['document_type'] = i[2]
            dd['has_protocol'] = i[3]
            dd['has_icf'] = i[4]
            dd['has_sap'] = i[5]
            if i[6] != None:
                dd['document_date'] = i[6].strftime('%Y-%m-%d')
                d.setdefault('provided_documents',[]).append(dd)
            else:
                pass
            dd['url'] = i[7]
            d.setdefault('provided_documents', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句13
        cursor13.execute("SELECT * FROM pending_results where nct_id ='%s'" % nct_id)
        data = cursor13.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['event'] = i[2]
            dd['event_date_description'] = i[3]
            dd['event_date'] = i[4]
            d.setdefault('pending_results', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句14
        cursor14.execute("SELECT * FROM participant_flows where nct_id ='%s'" % nct_id)
        data = cursor14.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['recruitment_details'] = i[2]
            dd['pre_assignment_details'] = i[3]
            d.setdefault('participant_flows', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句15
        cursor15.execute("SELECT * FROM overall_officials where nct_id ='%s'" % nct_id)
        data = cursor15.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['role'] = i[2]
            dd['name'] = i[3]
            dd['affiliation'] = i[4]
            d.setdefault('overall_officials', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句16
        cursor16.execute("SELECT * FROM outcomes where nct_id ='%s'" % nct_id)
        data = cursor16.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['outcome_type'] = i[2]
            dd['title'] = i[3]
            dd['description'] = i[4]
            dd['time_frame'] = i[5]
            dd['population'] = i[6]
            dd['anticipated_posting_date'] = i[7]
            dd['anticipated_posting_month_year'] = i[8]
            dd['units'] = i[9]
            dd['units_analyzed'] = i[10]
            dd['dispersion_type'] = i[11]
            dd['param_type'] = i[12]
            d.setdefault('outcomes', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句17
        cursor17.execute("SELECT * FROM outcome_measurements where nct_id ='%s'" % nct_id)
        data = cursor17.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['outcome_id'] = i[2]
            dd['result_group_id'] = i[3]
            dd['ctgov_group_code'] = i[4]
            dd['classification'] = i[5]
            dd['category'] = i[6]
            dd['title'] = i[7]
            dd['description'] = i[8]
            dd['units'] = i[9]
            dd['param_type'] = i[10]
            if i[11] != None:
                dd['param_value'] = float(i[11])
                d.setdefault('outcome_measurements',[]).append(dd)
            else:
                pass
            if i[12] != None:
                dd['param_value_num'] = float(i[12])
                d.setdefault('outcome_measurements',[]).append(dd)
            else:
                pass
            dd['dispersion_type'] = i[13]
            if i[14] != None:
                dd['dispersion_value'] = float(i[14])
                d.setdefault('outcome_measurements', []).append(dd)
            else:
                pass
            if i[15] != None:
                dd['dispersion_value_num'] = float(i[15])
                d.setdefault('outcome_measurements', []).append(dd)
            else:
                pass
            if i[16] != None:
                dd['dispersion_lower_limit'] = float(i[16])
                d.setdefault('outcome_measurements',[]).append(dd)
            else:
                pass
            if i[17] != None:
                dd['dispersion_upper_limit'] = float(i[17])
                d.setdefault('outcome_measurements',[]).append(dd)
            else:
                pass
            dd['explanation_of_na'] = i[18]
            d.setdefault('outcome_measurements', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句18
        cursor18.execute("SELECT * FROM outcome_counts where nct_id ='%s'" % nct_id)
        data = cursor18.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['outcome_id'] = i[2]
            dd['result_group_id'] = i[3]
            dd['ctgov_group_code'] = i[4]
            dd['scope'] = i[5]
            dd['units'] = i[6]
            dd['count'] = i[7]
            d.setdefault('outcome_counts', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句19
        cursor19.execute("SELECT * FROM outcome_analysis_groups where nct_id ='%s'" % nct_id)
        data = cursor19.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['outcome_analysis_id'] = i[2]
            dd['result_group_id'] = i[3]
            dd['ctgov_group_code'] = i[4]
            d.setdefault('outcome_analysis_groups', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句20
        cursor20.execute("SELECT * FROM outcome_analyses where nct_id ='%s'" % nct_id)
        data = cursor20.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['outcome_id'] = i[2]
            dd['non_inferiority_type'] = i[3]
            dd['non_inferiority_description'] = i[4]
            dd['param_type'] = i[5]
            if i[6] != None:
                dd['param_value'] = float(i[6])
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            dd['dispersion_type'] = i[7]
            if i[8] != None:
                dd['dispersion_value'] = float(i[8])
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            dd['p_value_modifier'] = i[9]
            if i[10] != None:
                dd['p_value'] = float(i[10])
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            if i[11] != None:
                dd['ci_n_sides'] = i[11]
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            if i[12] != None:
                dd['ci_percent'] = float(i[12])
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            if i[13] != None:
                dd['ci_lower_limit'] = float(i[13])
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            if i[14] != None:
                dd['ci_upper_limit'] = float(i[14])
                d.setdefault('outcome_analyses',[]).append(dd)
            else:
                pass
            dd['ci_upper_limit_na_comment'] = i[15]
            dd['p_value_description'] = i[16]
            dd['method'] = i[17]
            dd['method_description'] = i[18]
            dd['estimate_description'] = i[19]
            dd['groups_description'] = i[20]
            dd['other_analysis_description'] = i[21]
            d.setdefault('outcome_analyses', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句21
        cursor21.execute("SELECT * FROM milestones where nct_id ='%s'" % nct_id)
        data = cursor21.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['result_group_id'] = i[2]
            dd['ctgov_group_code'] = i[3]
            dd['title'] = i[4]
            dd['period'] = i[5]
            dd['description'] = i[6]
            dd['count'] = i[7]
            d.setdefault('milestones', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句22
        cursor22.execute("SELECT * FROM links where nct_id ='%s'" % nct_id)
        data = cursor22.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['url'] = i[2]
            dd['description'] = i[3]
            d.setdefault('links', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句23
        cursor23.execute("SELECT * FROM keywords where nct_id ='%s'" % nct_id)
        data = cursor23.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['name'] = i[2]
            dd['downcase_name'] = i[3]
            d.setdefault('keywords', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句24
        cursor24.execute("SELECT * FROM ipd_information_types where nct_id ='%s'" % nct_id)
        data = cursor24.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['name'] = i[2]
            d.setdefault('ipd_information_types', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句25
        cursor25.execute("SELECT * FROM interventions where nct_id ='%s'" % nct_id)
        data = cursor25.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['intervention_type'] = i[2]
            dd['name'] = i[3]
            dd['description'] = i[4]
            d.setdefault('interventions', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句26
        cursor26.execute("SELECT * FROM intervention_other_names where nct_id ='%s'" % nct_id)
        data = cursor26.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['intervention_id'] = i[2]
            dd['name'] = i[3]
            d.setdefault('intervention_other_names', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句27
        cursor27.execute("SELECT * FROM id_information where nct_id ='%s'" % nct_id)
        data = cursor27.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['id_type'] = i[2]
            dd['id_value'] = i[3]
            d.setdefault('id_information', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句28
        cursor28.execute("SELECT * FROM facility_investigators where nct_id ='%s'" % nct_id)
        data = cursor28.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['facility_id'] = i[2]
            dd['role'] = i[3]
            dd['name'] = i[4]
            d.setdefault('facility_investigators', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句29
        cursor29.execute("SELECT * FROM facility_contacts where nct_id ='%s'" % nct_id)
        data = cursor29.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['facility_id'] = i[2]
            dd['contact_type'] = i[3]
            dd['name'] = i[4]
            dd['email'] = i[5]
            dd['phone'] = i[6]
            d.setdefault('facility_contacts', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句30
        cursor30.execute("SELECT * FROM facilities where nct_id ='%s'" % nct_id)
        data = cursor30.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['status'] = i[2]
            dd['name'] = i[3]
            dd['city'] = i[4]
            dd['state'] = i[5]
            dd['zip'] = i[6]
            dd['country'] = i[7]
            d.setdefault('facilities', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句31
        cursor31.execute("SELECT * FROM eligibilities where nct_id ='%s'" % nct_id)
        data = cursor31.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['sampling_method'] = i[2]
            dd['gender'] = i[3]
            dd['minimum_age'] = i[4]
            dd['maximum_age'] = i[5]
            dd['healthy_volunteers'] = i[6]
            dd['population'] = i[7]
            dd['criteria'] = i[8]
            dd['gender_description'] = i[9]
            dd['gender_based'] = i[10]
            d.setdefault('eligibilities', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句32
        cursor32.execute("SELECT * FROM drop_withdrawals where nct_id ='%s'" % nct_id)
        data = cursor32.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['result_group_id'] = i[2]
            dd['ctgov_group_code'] = i[3]
            dd['period'] = i[4]
            dd['reason'] = i[5]
            dd['count'] = i[6]
            d.setdefault('drop_withdrawals', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句33
        cursor33.execute("SELECT * FROM detailed_descriptions where nct_id ='%s'" % nct_id)
        data = cursor33.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['description'] = i[2]
            d.setdefault('detailed_descriptions', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句34
        cursor34.execute("SELECT * FROM designs where nct_id ='%s'" % nct_id)
        data = cursor34.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['allocation'] = i[2]
            dd['intervention_model'] = i[3]
            dd['observational_model'] = i[4]
            dd['primary_purpose'] = i[5]
            dd['time_perspective'] = i[6]
            dd['masking'] = i[7]
            dd['masking_description'] = i[8]
            dd['intervention_model_description'] = i[9]
            dd['subject_masked'] = i[10]
            dd['caregiver_masked'] = i[11]
            dd['investigator_masked'] = i[12]
            dd['outcomes_assessor_masked'] = i[13]
            d.setdefault('designs', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句35
        cursor35.execute("SELECT * FROM design_outcomes where nct_id ='%s'" % nct_id)
        data = cursor35.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['outcome_type'] = i[2]
            dd['measure'] = i[3]
            dd['time_frame'] = i[4]
            dd['population'] = i[5]
            dd['description'] = i[6]
            d.setdefault('design_outcomes', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句36
        cursor36.execute("SELECT * FROM design_groups where nct_id ='%s'" % nct_id)
        data = cursor36.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['group_type'] = i[2]
            dd['title'] = i[3]
            dd['description'] = i[4]
            d.setdefault('design_groups', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句37
        cursor37.execute("SELECT * FROM design_group_interventions where nct_id ='%s'" % nct_id)
        data = cursor37.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['design_group_id'] = i[2]
            dd['intervention_id'] = i[3]
            d.setdefault('design_group_interventions', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句38
        cursor38.execute("SELECT * FROM countries where nct_id ='%s'" % nct_id)
        data = cursor38.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['name'] = i[2]
            dd['removed'] = i[3]
            d.setdefault('countries', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句39
        cursor39.execute("SELECT * FROM conditions where nct_id ='%s'" % nct_id)
        data = cursor39.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['name'] = i[2]
            dd['downcase_name'] = i[3]
            d.setdefault('conditions', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句40
        cursor40.execute("SELECT * FROM central_contacts where nct_id ='%s'" % nct_id)
        data = cursor40.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['contact_type'] = i[2]
            dd['name'] = i[3]
            dd['phone'] = i[4]
            dd['email'] = i[5]
            d.setdefault('central_contacts', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)


        ## 执行SQL语句41
        cursor41.execute("SELECT * FROM calculated_values where nct_id ='%s'" % nct_id)
        data = cursor41.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['number_of_facilities'] = i[2]
            dd['number_of_nsae_subjects'] = i[3]
            dd['number_of_sae_subjects'] = i[4]
            dd['registered_in_calendar_year'] = i[5]
            if i[6] != None:
                dd['nlm_download_date'] = i[6].strftime('%Y-%m-%d')
                d.setdefault('studies', []).append(dd)
            else:
                pass
            dd['actual_duration'] = i[7]
            dd['were_results_reported'] = i[8]
            dd['months_to_report_results'] = i[9]
            dd['has_us_facility'] = i[10]
            dd['has_single_facility'] = i[11]
            dd['minimum_age_num'] = i[12]
            dd['maximum_age_num'] = i[13]
            dd['minimum_age_unit'] = i[14]
            dd['maximum_age_unit'] = i[15]
            dd['number_of_primary_outcomes_to_measure'] = i[16]
            dd['number_of_secondary_outcomes_to_measure'] = i[17]
            dd['number_of_other_outcomes_to_measure'] = i[18]
            d.setdefault('calculated_values', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句42
        cursor42.execute("SELECT * FROM browse_interventions where nct_id ='%s'" % nct_id)
        data = cursor42.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['mesh_term'] = i[2]
            dd['downcase_mesh_term'] = i[3]
            d.setdefault('browse_interventions', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句43
        cursor43.execute("SELECT * FROM browse_conditions where nct_id ='%s'" % nct_id)
        data = cursor43.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['mesh_term'] = i[2]
            dd['downcase_mesh_term'] = i[3]
            d.setdefault('browse_conditions', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句44
        cursor44.execute("SELECT * FROM brief_summaries where nct_id ='%s'" % nct_id)
        data = cursor44.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['description'] = i[2]
            d.setdefault('brief_summaries', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句45
        cursor45.execute("SELECT * FROM baseline_measurements where nct_id ='%s'" % nct_id)
        data = cursor45.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['result_group_id'] = i[2]
            dd['ctgov_group_code'] = i[3]
            dd['classification'] = i[4]
            dd['category'] = i[5]
            dd['title'] = i[6]
            dd['description'] = i[7]
            dd['units'] = i[8]
            dd['param_type'] = i[9]
            if i[10] != None:
                dd['param_value'] = float(i[10])
                d.setdefault('baseline_measurements',[]).append(dd)
            else:
                pass
            if i[11] != None:
                dd['param_value_num'] = float(i[11])
                d.setdefault('baseline_measurements',[]).append(dd)
            else:
                pass
            dd['dispersion_type'] = i[12]
            if i[13] != None:
                dd['dispersion_value'] = float(i[13])
                d.setdefault('baseline_measurements', []).append(dd)
            else:
                pass
            if i[14] != None:
                dd['dispersion_value_num'] = float(i[14])
                d.setdefault('baseline_measurements', []).append(dd)
            else:
                pass
            if i[15] != None:
                dd['dispersion_lower_limit'] = float(i[15])
                d.setdefault('baseline_measurements', []).append(dd)
            else:
                pass
            if i[16] != None:
                dd['dispersion_upper_limit'] = float(i[16])
                d.setdefault('baseline_measurements', []).append(dd)
            else:
                pass
            dd['explanation_of_na'] = i[17]
            d.setdefault('baseline_measurements', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)

        ## 执行SQL语句46
        cursor46.execute("SELECT * FROM baseline_counts where nct_id ='%s'" % nct_id)
        data = cursor46.fetchall()
        d = {}
        for i in data:
            dd = {}
            dd['id'] = i[0]
            dd['result_group_id'] = i[2]
            dd['ctgov_group_code'] = i[3]
            dd['units'] = i[4]
            dd['scope'] = i[5]
            dd['count'] = i[6]
            d.setdefault('baseline_counts', []).append(dd)
        esid = md5_utils.lstrip_zero_get_md5(data=nct_id)
        all_dict = {}
        # all_dict["esid"] = esid
        all_dict["nct_id"] = nct_id
        all_dict["table_content"] = d
        table_name.insert(all_dict)
        # es_utils.insert_or_replace('nct', d=all_dict)
        print(all_dict)






    # 获取数据
    # n = 0
    # dic = {}
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         print(i)
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['document_id'] = i[2]
    #         dd['document_type'] = i[3]
    #         dd['url'] = i[4]
    #         dd['comment'] = i[5]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    # print(dic)
    # print(len(dic))

    # cursor1.execute("SELECT * FROM categories")
    # while True:
    #     data = cursor1.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['name'] = i[2]
    #         dd['created_at'] = i[3]
    #         dd['updated_at'] = i[4]
    #         dd['grouping'] = i[5]
    #         dd['study_search_id'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    # print(dic)
    # print(len(dic))
    #
    # cursor.execute("SELECT * FROM study_references")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['pmid'] = i[2]
    #         dd['reference_type'] = i[3]
    #         dd['citation'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM studies")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[0]
    #         dd = {}
    #         dd['nlm_download_date_description'] = i[1]
    #         dd['study_first_submitted_date'] = i[2]
    #         dd['results_first_submitted_date'] = i[3]
    #         dd['disposition_first_submitted_date'] = i[4]
    #         dd['last_update_submitted_date'] = i[5]
    #         dd['study_first_submitted_qc_date'] = i[6]
    #         dd['study_first_posted_date'] = i[7]
    #         dd['study_first_posted_date_type'] = i[8]
    #         dd['results_first_submitted_qc_date'] = i[9]
    #         dd['results_first_posted_date'] = i[10]
    #         dd['results_first_posted_date_type'] = i[11]
    #         dd['disposition_first_submitted_qc_date'] = i[12]
    #         dd['disposition_first_posted_date'] = i[13]
    #         dd['disposition_first_posted_date_type'] = i[14]
    #         dd['last_update_submitted_qc_date'] = i[15]
    #         dd['last_update_posted_date'] = i[16]
    #         dd['last_update_posted_date_type'] = i[17]
    #         dd['start_month_year'] = i[18]
    #         dd['start_date_type'] = i[19]
    #         dd['start_date'] = i[20]
    #         dd['verification_month_year'] = i[21]
    #         dd['verification_date'] = i[22]
    #         dd['completion_month_year'] = i[23]
    #         dd['completion_date_type'] = i[24]
    #         dd['completion_date'] = i[25]
    #         dd['primary_completion_month_year'] = i[26]
    #         dd['primary_completion_date_type'] = i[27]
    #         dd['primary_completion_date'] = i[28]
    #         dd['target_duration'] = i[29]
    #         dd['study_type'] = i[30]
    #         dd['acronym'] = i[31]
    #         dd['baseline_population'] = i[32]
    #         dd['brief_title'] = i[33]
    #         dd['official_title'] = i[34]
    #         dd['overall_status'] = i[35]
    #         dd['last_known_status'] = i[36]
    #         dd['phase'] = i[37]
    #         dd['enrollment'] = i[38]
    #         dd['enrollment_type'] = i[39]
    #         dd['source'] = i[40]
    #         dd['limitations_and_caveats'] = i[41]
    #         dd['number_of_arms'] = i[42]
    #         dd['number_of_groups'] = i[43]
    #         dd['why_stopped'] = i[44]
    #         dd['has_expanded_access'] = i[45]
    #         dd['expanded_access_type_individual'] = i[46]
    #         dd['expanded_access_type_intermediate'] = i[47]
    #         dd['expanded_access_type_treatment'] = i[48]
    #         dd['has_dmc'] = i[49]
    #         dd['is_fda_regulated_drug'] = i[50]
    #         dd['is_fda_regulated_device'] = i[51]
    #         dd['is_unapproved_device'] = i[52]
    #         dd['is_ppsd'] = i[53]
    #         dd['is_us_export'] = i[54]
    #         dd['biospec_retention'] = i[55]
    #         dd['biospec_description'] = i[56]
    #         dd['ipd_time_frame'] = i[57]
    #         dd['ipd_access_criteria'] = i[58]
    #         dd['ipd_url'] = i[59]
    #         dd['plan_to_share_ipd'] = i[60]
    #         dd['plan_to_share_ipd_description'] = i[61]
    #         dd['created_at'] = i[62]
    #         dd['updated_at'] = i[63]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM sponsors")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['agency_class'] = i[2]
    #         dd['lead_or_collaborator'] = i[3]
    #         dd['name'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM result_groups")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['ctgov_group_code'] = i[2]
    #         dd['result_type'] = i[3]
    #         dd['title'] = i[4]
    #         dd['description'] = i[5]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM result_agreements")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['pi_employee'] = i[2]
    #         dd['agreement'] = i[3]
    #         dd['restriction_type'] = i[4]
    #         dd['other_details'] = i[5]
    #         dd['restrictive_agreement'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM responsible_parties")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['responsible_party_type'] = i[2]
    #         dd['name'] = i[3]
    #         dd['title'] = i[4]
    #         dd['organization'] = i[5]
    #         dd['affiliation'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM reported_events")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['result_group_id'] = i[2]
    #         dd['ctgov_group_code'] = i[3]
    #         dd['time_frame'] = i[4]
    #         dd['event_type'] = i[5]
    #         dd['default_vocab'] = i[6]
    #         dd['default_assessment'] = i[7]
    #         dd['subjects_affected'] = i[8]
    #         dd['subjects_at_risk'] = i[9]
    #         dd['description'] = i[10]
    #         dd['event_count'] = i[11]
    #         dd['organ_system'] = i[12]
    #         dd['adverse_event_term'] = i[13]
    #         dd['frequency_threshold'] = i[14]
    #         dd['vocab'] = i[15]
    #         dd['assessment'] = i[16]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM reported_events_totals")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['ctgov_group_code'] = i[2]
    #         dd['event_type'] = i[3]
    #         dd['classification'] = i[4]
    #         dd['subjects_affected'] = i[5]
    #         dd['subjects_at_risk'] = i[6]
    #         dd['created_at'] = i[7]
    #         dd['updated_at'] = i[8]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM provided_documents")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['document_type'] = i[2]
    #         dd['has_protocol'] = i[3]
    #         dd['has_icf'] = i[4]
    #         dd['has_sap'] = i[5]
    #         dd['document_date'] = i[6]
    #         dd['url'] = i[7]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM pending_results")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['event'] = i[2]
    #         dd['event_date_description'] = i[3]
    #         dd['event_date'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM participant_flows")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['recruitment_details'] = i[2]
    #         dd['pre_assignment_details'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM overall_officials")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['role'] = i[2]
    #         dd['name'] = i[3]
    #         dd['affiliation'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM outcomes")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['outcome_type'] = i[2]
    #         dd['title'] = i[3]
    #         dd['description'] = i[4]
    #         dd['time_frame'] = i[5]
    #         dd['population'] = i[6]
    #         dd['anticipated_posting_date'] = i[7]
    #         dd['anticipated_posting_month_year'] = i[8]
    #         dd['units'] = i[9]
    #         dd['units_analyzed'] = i[10]
    #         dd['dispersion_type'] = i[11]
    #         dd['param_type'] = i[12]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM outcome_measurements")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['outcome_id'] = i[2]
    #         dd['result_group_id'] = i[3]
    #         dd['ctgov_group_code'] = i[4]
    #         dd['classification'] = i[5]
    #         dd['category'] = i[6]
    #         dd['title'] = i[7]
    #         dd['description'] = i[8]
    #         dd['units'] = i[9]
    #         dd['param_type'] = i[10]
    #         dd['param_value'] = i[11]
    #         dd['param_value_num'] = i[12]
    #         dd['dispersion_type'] = i[13]
    #         dd['dispersion_value'] = i[14]
    #         dd['dispersion_value_num'] = i[15]
    #         dd['dispersion_lower_limit'] = i[16]
    #         dd['dispersion_upper_limit'] = i[17]
    #         dd['explanation_of_na'] = i[18]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM outcome_counts")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['outcome_id'] = i[2]
    #         dd['result_group_id'] = i[3]
    #         dd['ctgov_group_code'] = i[4]
    #         dd['scope'] = i[5]
    #         dd['units'] = i[6]
    #         dd['count'] = i[7]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM outcome_analysis_groups")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['outcome_analysis_id'] = i[2]
    #         dd['result_group_id'] = i[3]
    #         dd['ctgov_group_code'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM outcome_analyses")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['outcome_id'] = i[2]
    #         dd['non_inferiority_type'] = i[3]
    #         dd['non_inferiority_description'] = i[4]
    #         dd['param_type'] = i[5]
    #         dd['param_value'] = i[6]
    #         dd['dispersion_type'] = i[7]
    #         dd['dispersion_value'] = i[8]
    #         dd['p_value_modifier'] = i[9]
    #         dd['p_value'] = i[10]
    #         dd['ci_n_sides'] = i[11]
    #         dd['ci_percent'] = i[12]
    #         dd['ci_lower_limit'] = i[13]
    #         dd['ci_upper_limit'] = i[14]
    #         dd['ci_upper_limit_na_comment'] = i[15]
    #         dd['p_value_description'] = i[16]
    #         dd['method'] = i[17]
    #         dd['method_description'] = i[18]
    #         dd['estimate_description'] = i[19]
    #         dd['groups_description'] = i[20]
    #         dd['other_analysis_description'] = i[21]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM milestones")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['result_group_id'] = i[2]
    #         dd['ctgov_group_code'] = i[3]
    #         dd['title'] = i[4]
    #         dd['period'] = i[5]
    #         dd['description'] = i[6]
    #         dd['count'] = i[7]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM links")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['url'] = i[2]
    #         dd['description'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM keywords")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['name'] = i[2]
    #         dd['downcase_name'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM ipd_information_types")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['name'] = i[2]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM interventions")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['intervention_type'] = i[2]
    #         dd['name'] = i[3]
    #         dd['description'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM intervention_other_names")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['intervention_id'] = i[2]
    #         dd['name'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM id_information")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['id_type'] = i[2]
    #         dd['id_value'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM facility_investigators")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['facility_id'] = i[2]
    #         dd['role'] = i[3]
    #         dd['name'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM facility_contacts")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['facility_id'] = i[2]
    #         dd['contact_type'] = i[3]
    #         dd['name'] = i[4]
    #         dd['email'] = i[5]
    #         dd['phone'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM facilities")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['status'] = i[2]
    #         dd['name'] = i[3]
    #         dd['city'] = i[4]
    #         dd['state'] = i[5]
    #         dd['zip'] = i[6]
    #         dd['country'] = i[7]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM eligibilities")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['sampling_method'] = i[2]
    #         dd['gender'] = i[3]
    #         dd['minimum_age'] = i[4]
    #         dd['maximum_age'] = i[5]
    #         dd['healthy_volunteers'] = i[6]
    #         dd['population'] = i[7]
    #         dd['criteria'] = i[8]
    #         dd['gender_description'] = i[9]
    #         dd['gender_based'] = i[10]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM drop_withdrawals")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['result_group_id'] = i[2]
    #         dd['ctgov_group_code'] = i[3]
    #         dd['period'] = i[4]
    #         dd['reason'] = i[5]
    #         dd['count'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM documents")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['document_id'] = i[2]
    #         dd['document_type'] = i[3]
    #         dd['url'] = i[4]
    #         dd['comment'] = i[5]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM detailed_descriptions")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['description'] = i[2]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM designs")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['allocation'] = i[2]
    #         dd['intervention_model'] = i[3]
    #         dd['observational_model'] = i[4]
    #         dd['primary_purpose'] = i[5]
    #         dd['time_perspective'] = i[6]
    #         dd['masking'] = i[7]
    #         dd['masking_description'] = i[8]
    #         dd['intervention_model_description'] = i[9]
    #         dd['subject_masked'] = i[10]
    #         dd['caregiver_masked'] = i[11]
    #         dd['investigator_masked'] = i[12]
    #         dd['outcomes_assessor_masked'] = i[13]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM design_outcomes")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['outcome_type'] = i[2]
    #         dd['measure'] = i[3]
    #         dd['time_frame'] = i[4]
    #         dd['population'] = i[5]
    #         dd['description'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM design_groups")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['group_type'] = i[2]
    #         dd['title'] = i[3]
    #         dd['description'] = i[4]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM design_group_interventions")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['design_group_id'] = i[2]
    #         dd['intervention_id'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM countries")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['name'] = i[2]
    #         dd['removed'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM conditions")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['name'] = i[2]
    #         dd['downcase_name'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM central_contacts")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['contact_type'] = i[2]
    #         dd['name'] = i[3]
    #         dd['phone'] = i[4]
    #         dd['email'] = i[5]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM categories")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['name'] = i[2]
    #         dd['created_at'] = i[3]
    #         dd['updated_at'] = i[4]
    #         dd['grouping'] = i[5]
    #         dd['study_search_id'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM calculated_values")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['number_of_facilities'] = i[2]
    #         dd['number_of_nsae_subjects'] = i[3]
    #         dd['number_of_sae_subjects'] = i[4]
    #         dd['registered_in_calendar_year'] = i[5]
    #         dd['nlm_download_date'] = i[6]
    #         dd['actual_duration'] = i[7]
    #         dd['were_results_reported'] = i[8]
    #         dd['months_to_report_results'] = i[9]
    #         dd['has_us_facility'] = i[10]
    #         dd['has_single_facility'] = i[11]
    #         dd['minimum_age_num'] = i[12]
    #         dd['maximum_age_num'] = i[13]
    #         dd['minimum_age_unit'] = i[14]
    #         dd['maximum_age_unit'] = i[15]
    #         dd['number_of_primary_outcomes_to_measure'] = i[16]
    #         dd['number_of_secondary_outcomes_to_measure'] = i[17]
    #         dd['number_of_other_outcomes_to_measure'] = i[18]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM browse_interventions")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['mesh_term'] = i[2]
    #         dd['downcase_mesh_term'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM browse_conditions")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['mesh_term'] = i[2]
    #         dd['downcase_mesh_term'] = i[3]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM brief_summaries")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['description'] = i[2]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM baseline_measurements")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['result_group_id'] = i[2]
    #         dd['ctgov_group_code'] = i[3]
    #         dd['classification'] = i[4]
    #         dd['category'] = i[5]
    #         dd['title'] = i[6]
    #         dd['description'] = i[7]
    #         dd['units'] = i[8]
    #         dd['param_type'] = i[9]
    #         dd['has_us_facility'] = i[10]
    #         dd['param_value_num'] = i[11]
    #         dd['dispersion_type'] = i[12]
    #         dd['dispersion_value'] = i[13]
    #         dd['dispersion_value_num'] = i[14]
    #         dd['dispersion_lower_limit'] = i[15]
    #         dd['dispersion_upper_limit'] = i[16]
    #         dd['explanation_of_na'] = i[17]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break
    #
    # cursor.execute("SELECT * FROM baseline_counts")
    # while True:
    #     data = cursor.fetchmany(1000)
    #     d = {}
    #     for i in data:
    #         nct_id = i[1]
    #         dd = {}
    #         dd['id'] = i[0]
    #         dd['result_group_id'] = i[2]
    #         dd['ctgov_group_code'] = i[3]
    #         dd['units'] = i[4]
    #         dd['scope'] = i[5]
    #         dd['count'] = i[6]
    #         d.setdefault(nct_id, []).append(dd)
    #     dic.update(d)
    #     if data == []:
    #         break

    # 提交事务
    connection.commit()
    # 关闭连接
    cursor1.close()
    connection.close()