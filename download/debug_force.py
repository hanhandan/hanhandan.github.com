import json
import os,sys
import urllib
import urllib2
import httplib
import thread
import threading
import time
import logging
import readline
import string

UPGRADE_VER='V1.0.1211'

#mnt set_logconf '{"file":"/thunder/etc/ubus_app_log_debug.conf"}'
#"mnt", "set_logconf", {"file": "/thunder/etc/ubus_app_log_debug.conf "}]}'
# 127585636 CCe4e_qo0187   liuguantao's miner
# 14926049  XJJueVAI0074   tangxinfa's miner
# 405832680 FaHbUNwY1871   yangxiaohu's miner
# 408948711 fffVy8Bp0001   xuhuilin's miner
# 18917075 1VVBeNEq0051    zhangzhigang's miner
# 466025491 SlYKB38a0034   xiefucai's miner
# 22522481 45c_2nva1929 gaoyi's miner
# 336450136  3NdDR_h_0292  max's miner
# 360364648 62L_f3UN0018   explore's miner

# 6393397 IhdBgq001373   adingzai's  miner  qq(150505237)
# 416046785 YWvDFyQA0167   iJeremy_0170's miner QQ iJeremy_0170(469057659)
# 19786223  sByZH8wu1368	hzzsn520's miner 1
# 19786223  Qws1dU980936	hzzsn520's miner 2
# 346188756 q4_8-9xe0009	QQ 284366481
# 346188756  TuK_B3Zc0103	QQ 284366481
# 24055171 8POWaiua0755      sn==0



url="http://kjapi.peiluyou.com:5171/ubus?account_id=306554937&session_id=47722FA5B69688B11391D2639F5E4D1DCC4681FD0F616965B61500AB98BD2AEE5CE2242378ABCDFF9D456144732034B32F984A7A95A3118349E8E3891464E992"

CHECK_VERSION_STAT=0;
CFG_OPKG_STAT=1;
RESTART_UPGRADE=2;
CHECK_STAT=3;
UPGRADE_START_STAT=4;
UPGRADE_SUCCESS=5;
UPGRADE_FAILED=6;

INPUT_COMMAND='date'

#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "dcdn", "get_status_detail", {"input": "date 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "dcdn", "get_status_detail", {"input": "date 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "upnp_client", "set", {"enable": false}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "get_profile", {"input": "ls /tmp/dcdn_base/dcdn_client_0 -l 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "sh /thunder/bin/run_explore_node.sh "}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input":'+'"'+INPUT_COMMAND+'"'+'}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "dcdn_client_0", "init", {"":'+'"'+INPUT_COMMAND+'"'+'}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "opkg-cl install /tmp/t1.ipk 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "ls -l /tmp/t.ipk 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "upgrade", "check", {"input": "ps  2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "wget http://10.10.226.122/packages/miner/1105/thunder-miner-app_V1.0.1105_arm.ipk -O /tmp/t1.ipk 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "get_profile", {"input": "sync 2>&1"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "upgrade", "check", {"file": "/thunder/etc/ubus_app_log_debug.conf"}]}'
cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "mnt", "set_logconf", {"file": "/thunder/etc/ubus_app_log_debug.conf"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "dcdn", "set_resolve", {"hostname":"hub5pn.wap.sandai.net","addresses":["119.189.1.10","180.97.177.38"]}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "dcdn", "set_resolve", {"hostname":"hub5pn.wap.sandai.net","addresses":["",""]}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "dcdn", "set_resolve", {"hostname":"hub5pn.wap.sandai.net","addresses":["180.97.177.38","119.189.1.10"]}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input":"wget www.ask-han.org/download/run_explore_node.sh -O /thunder/bin/run_explore_node.sh;(nohup /bin/sh /thunder/bin/run_explore_node.sh >/dev/null 2>&1) &"}]}'
#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input":"(nohup /bin/sh /thunder/bin/run_explore_node.sh >/dev/null 2>&1) &"}]}'

#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input":"(nohup wget http://update.peiluyou.com/conf/miner/packages/thunder-miner-app_V1.0.1064_arm.ipk  -O /tmp/t.ipk  >/dev/null  2>&1) &"}]}'

#cmd_test = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input":'+'"'+'(nohup '+INPUT_COMMAND+' >/dev/null   2>&1) &'+'"'+'}]}'

cmd_server = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "server", "get_devices", {"input":'+'"'+INPUT_COMMAND+'"'+'}]}'


cmd_check_version = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "get_profile", {"input": "date"}]}'
cmd_check_cmd = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "upgrade", "check", {"input": "date"}]}'
cmd_cfg_conf_data = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "wget http://update.peiluyou.com/conf/miner_beta/opkg.conf -O /etc/opkg/opkg.conf 2>&1;killall opkg-cl "}]}'
cmd_restart_upgrade = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "killall  upgrade 2>&1"}]}'
cmd_upgrade_start = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "upgrade", "start", {"input": "date"}]}'
cmd_check_data = '{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input": "date"}]}'
upgrade_command=[cmd_check_version,cmd_cfg_conf_data,cmd_restart_upgrade,cmd_check_cmd,cmd_upgrade_start,cmd_check_data];
upgrade_stat_discript=["check_version","config opkg server","restart upgrade","check upgradable","start upgrade","upgrade successful","upgrade failed"]

threads=[]
account_id_list=[]

def toSize(s):
    k = string.atof(s)
    if k < 1024 :
        return bytes(k)+'B'
    elif k < 1024 * 1024 :
        return bytes(k / 1024) + 'KB'
    elif k < 1024 * 1024 * 1024 :
        return bytes(k / 1024 / 1024) + 'MB'
    elif k < 1024 * 1024 * 1024 * 1024 :
        return bytes(k / 1024 / 1024 / 1024) + 'GB'
    else :
        return bytes(k / 1024 / 1024 / 1024 / 1024) + 'TB'

def check_upgrade_state(stat,json_resp):
    if stat == CHECK_STAT:
        app_ver=json_resp[1]["app"];
        if str.strip(str(app_ver)) == '' :
            print 'can not detect download ipk file'
            return 1
        print "app_version"+"["+app_ver+"]"
    if stat == CHECK_VERSION_STAT:
        sys_ver=json_resp[1]["system_version"];
        cmp_ret=cmp(str(sys_ver),UPGRADE_VER)
        print 'compare result '+'['+str(cmp_ret)+']'
        if cmp_ret == -1 :
            print 'app_ver is '+str(sys_ver)
            return 0
        if cmp_ret == 0:
            return 2
        if cmp_ret == 1:
            return 0
    return 0;

def command_miner(account_id,device_id,device_sn):
    URL_POST=url+"&"+"as_account_id="+str(account_id)+"&"+"device_id="+str(device_id)
    cmd_data=cmd_test
    req=urllib2.Request(url=URL_POST,data=cmd_data)
    req.add_header('Connection','Keep-Alive')
    req.add_header('Content-Type','application/json')
    logging.debug("device_sn:[%s] device_id[%s] start open url" % (device_sn,device_id));
    try:
        resp = urllib2.urlopen(req,timeout=30);
    except:
        print "url open timeout"
        return
    resp_data=json.loads(resp.read())
    try:
        result_ret=resp_data["result"]
        result_flag=1
    except:
        result_ret=resp_data["error"]
        result_flag=0

    try:
        message = json.dumps(result_ret[1]["output"])
    except:
        message = json.dumps(result_ret)
    print message.decode('unicode_escape')
    return

def command_miner_linux(account_id,device_id,device_sn):
    URL_POST=url+"&"+"as_account_id="+str(account_id)+"&"+"device_id="+str(device_id)
    stat=CHECK_VERSION_STAT
    global INPUT_COMMAND
    while True :
        logging.debug("device_sn:[%s] device_id[%s] entry while" % (device_sn,device_id));
        INPUT_COMMAND=raw_input("input command: \33[37m")
        print "\33[0m"
        if cmp(INPUT_COMMAND,'quit') == 0:
            print 'quit from debug tools'
            break;
        cmd_data='{"jsonrpc":"2.0","id": 1,"method":"call","params":["", "remote", "shell", {"input":'+'"'+INPUT_COMMAND+' 2>&1  "'+'}]}'
        req=urllib2.Request(url=URL_POST,data=cmd_data)
        req.add_header('Connection','Keep-Alive')
        req.add_header('Content-Type','application/json')
        logging.debug("device_sn:[%s] device_id[%s] start open url" % (device_sn,device_id));
        try:
            resp = urllib2.urlopen(req,timeout=30);
        except:
            print "url open timeout"
            continue
        logging.debug("device_sn:[%s] device_id[%s] end open url" % (device_sn,device_id));
        resp_data=json.loads(resp.read())
        try:
            result_ret=resp_data["result"]
            result_flag=1
        except:
            result_ret=resp_data["error"]
            result_flag=0
            stat=UPGRADE_FAILED
        try:
            message = json.dumps(result_ret[1]["output"])
        except:
            message = json.dumps(result_ret)
        print "\33[33m"
        print message.decode('unicode_escape')
        print "\33[0m"
    return

def get_extern_ip_isp(extern_ip):
    URL_POST='http://ip.taobao.com/service/getIpInfo.php?ip='+str(extern_ip)
    req=urllib2.Request(url=URL_POST)
    try:
        resp=urllib2.urlopen(req,timeout=60)
    except:
        return (0,0)
    resp_data=json.loads(resp.read())

    try:
        data=resp_data["data"]
    except:
        return (0,0)
    try:
        city=data["city"]
    except:
        city=0
    try:
        isp=data["isp"]
    except:
        isp=0
    return (city,isp)

def get_miner_deviceid(account_id):
    global device_id
    global device_sn
    device_id=0
    device_sn=0
    URL_POST=url+"&"+"as_account_id="+str(account_id)
    cmd_data=cmd_server;
    req=urllib2.Request(url=URL_POST,data=cmd_data)
    req.add_header('Connection','Keep-Alive')
    req.add_header('Content-Type','application/json')
    try:
        resp = urllib2.urlopen(req,timeout=60);
    except:
        loggint.debug("url open timeout");
    resp_data=json.loads(resp.read())
    result_ret=resp_data["result"]
    message = json.dumps(result_ret)
    #print type(resp_data)
    #print type(result_ret)
    #print type(message)
    #print message.decode('unicode_escape')
    count=len(result_ret[1]['devices'])
    print 'The user id has '+str(count)+' miner box'
    if count == 0 :
        quit()
        return (0, 0, 0)
    # account_id device_id device_sn extern_ip system_version
    myList = [([0] * 5) for i in range(count)]
    for i in range(0,count):
        #print 'loop start\n'
        device_info=result_ret[1]['devices'][i]
        device_print_info=json.dumps(result_ret[1]['devices'][i])
        #print device_print_info.decode('unicode_escape')
        #print type(device_info)
        device_id=device_info["device_id"]
        device_sn=device_info["device_sn"]
        extern_ip=device_info["ip"]
        system_version=device_info["system_version"]
        status=device_info['status']
        print "index: \33[33m%s\33[0m \t device_name: \33[33m%s\33[0m(%s) \tsn: \33[33m%s\33[0m \tdcdn_id: \33[33m%s\33[0m"%(i,device_info['device_name'],status,device_sn,device_info['dcdn_id'])
        print "\t\t upload_speed: \33[33m%s/s\33[0m \t download_speed: \33[33m%s/s\33[0m"%(toSize(device_info['dcdn_upload_speed']),toSize(device_info['dcdn_download_speed']))
        print "\t\t exception_name: \33[33m%s\33[0m \t exception_message: \33[33m%s\33[0m"%(device_info['exception_name'],device_info['exception_message'])
        print "\t\t dcdn_upnp_status: \33[33m%s\33[0m \t dcdn_upnp_message: \33[33m%s\33[0m"%(device_info['dcdn_upnp_status'],device_info['dcdn_upnp_message'])

        if len(device_info['dcdn_clients']) > 0 :
            print "\t\t disk_quota: \33[33m%s\33[0m \t space_used: \33[33m%s\33[0m"%(toSize(device_info['disk_quota']),toSize(device_info['dcdn_clients'][0]['space_used']))

        print ("\33[0m")
        myList[i][0]=account_id
        myList[i][1]=device_id
        myList[i][2]=device_sn
        myList[i][3]=extern_ip
        myList[i][4]=system_version
    if count > 1 :
        print 'Please input the miner index:'
        n=input("input:")
        if len(str(n)) > 1 :
            print 'error input  index ,return '
            return (0,0,0)
        else :
            (city,isp)=get_extern_ip_isp(myList[n][3])
            print 'SystemVersion: '+myList[n][4]+' extern_ip  '+myList[n][3]+' '+city+' '+isp
            return(myList[n][0],myList[n][1],myList[n][2])
    else:
        (city,isp)=get_extern_ip_isp(myList[0][3])
        print 'SystemVersion: '+myList[0][4]+' extern_ip  '+myList[0][3]+' '+city+' '+isp
        return(myList[0][0],myList[0][1],myList[0][2])



def upgrade_miner(account_id,device_id,device_sn):
    check_count=0
    URL_POST=url+"&"+"as_account_id="+str(account_id)+"&"+"device_id="+str(device_id)
    stat=CHECK_VERSION_STAT
    while True :
        print upgrade_stat_discript[stat]
        if check_count > 30:
            logging.debug("device_sn:[%s] device_id[%s] account_id[%s] stat[%s]" % (device_sn,device_id,str(account_id),upgrade_stat_discript[stat]))
            stat = UPGRADE_FAILED
        if stat == UPGRADE_SUCCESS or stat == UPGRADE_FAILED:
            print device_sn+'   upgrade stat   '+upgrade_stat_discript[stat]
            logging.debug("device_id [%s] upgrade [%s]" % (str(device_id),upgrade_stat_discript[stat]))
            if stat == UPGRADE_FAILED:
                logging.debug("device_sn [%s];device_id [%s] account_id[%s] error info  [%s] " % (str(device_sn),str(device_id),str(account_id),json.dumps(result_ret).decode('unicode_escape')));
            break
        time.sleep(10)
        cmd_data=upgrade_command[stat];
        req=urllib2.Request(url=URL_POST,data=cmd_data)
        req.add_header('Connection','Keep-Alive')
        req.add_header('Content-Type','application/json')
        try:
            resp = urllib2.urlopen(req,timeout=60);
        except:
            logging.debug("device_sn [%s];device_id [%s] account_id[%s] error info  [urlopen timeout]" % (str(device_sn),str(device_id),str(account_id)));
            stat=UPGRADE_FAILED
            continue

        resp_data=json.loads(resp.read())
        try:
            result_ret=resp_data["result"]
            result_flag=1
        except:
            result_ret=resp_data["error"]
            result_flag=0
            stat=UPGRADE_FAILED
            print result_ret

        if result_flag == 1:
            ret_stat=check_upgrade_state(stat,result_ret)
            if ret_stat == 0:
                stat=stat+1
                continue
            if ret_stat == 1:
                time.sleep(1)
                check_count=check_count+1
                continue
            if ret_stat == 2:
                stat = UPGRADE_SUCCESS
                continue
        print str(account_id)
        print json.dumps(result_ret).decode('unicode_escape')

def main_from_dump_json():
	logfile='log'+'_'+time.strftime("%Y-%m-%d_%H_%M_%S")
	logging.basicConfig(filename=logfile,filemode='w',level=logging.DEBUG)
	f=file("dump.json")
	s=json.load(f)
	count=1
	#len(s)
	for i in range(0,count):
		print i
		j = json.dumps(s[i])
		jctx=json.loads(j)
		DEVICE_SN=jctx["device_sn"]
		ACCOUNT_ID=297752445#jctx["account_id"]
		DEVICE_ID='Q2A1wbPl0010'#jctx["device_id"]
		upgrade_miner(ACCOUNT_ID,DEVICE_ID,DEVICE_SN)

def command_one_miner():
    count=len(sys.argv)
    ACCOUNT_ID=sys.argv[1]
    (ACCOUNT_ID,DEVICE_ID,DEVICE_SN)=get_miner_deviceid(ACCOUNT_ID);
    command_miner_linux(ACCOUNT_ID,DEVICE_ID,DEVICE_SN)
#command_miner(ACCOUNT_ID,DEVICE_ID,DEVICE_SN)
    return
    #command_miner(ACCOUNT_ID,DEVICE_ID,DEVICE_SN)

def command_all():
	logfile='log'+'_command_'+time.strftime("%Y-%m-%d_%H_%M_%S")
	logging.basicConfig(filename=logfile,filemode='w',level=logging.DEBUG)
	f=file("dump_test.json")
	s=json.load(f)
	count=len(s)
	for i in range(0,count):
		j = json.dumps(s[i])
		jctx=json.loads(j)
		ACCOUNT_ID=jctx["account_id"]
		cmp_ret=cmp(str(ACCOUNT_ID),"0")
		if cmp_ret == 0:
			continue
        if ACCOUNT_ID  in account_id_list:
            print ACCOUNT_ID+' has been added in list'
        else:
            t=threading.Thread(target=get_miner_deviceid,args=(ACCOUNT_ID,))
            threads.append(t)
            account_id_list.append(ACCOUNT_ID)
	for t in threads:
		t.start();
	for t in threads:
		t.join();


if __name__ == '__main__':
	command_one_miner()
