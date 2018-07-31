#coding:utf-8
import time
from sys import argv
from zabbix_client import ZabbixServerProxy
nowtime=int(time.time())
endtime=nowtime+100000000
class Zabbix():
    def __init__(self):
        self.zb = ZabbixServerProxy("http://192.168.203.91")
        self.zb.user.login(user="admin", password="zabbix_king")
     ####dddd########## 查询组所有组获取组id ###############
    def get_hostgroup(self):
        data = {
           "output":['groupid','name']
         }
        ret = self.zb.hostgroup.get(**data)
        return ret

########### 通过组id获取相关组内的所有主机 ###############
    def get_hostid(self,groupids=2):
        data = {
        "output": ["hostid", "name"],
        "groupids": groupids
        }
        ret = self.zb.host.get(**data)
        return ret
     ########## 通过获取的hostid查找相关监控想itemid ###################
    def item_get(self, hostids="10115"):
        data = {
       "output":["itemids","key_"],
       "hostids": hostids,
        }
        ret = self.zb.item.get(**data)
        return ret
  ######### 通过itemid（传入itemid和i0表示flast类型）获取相关监控项的历史数据 ###########
    def history_get(self, itemid, i ,limit=10):
        data = { "output": "extend",
          "history": i,
          "itemids": [itemid], 
          "limit": limit 
          }
        ret = self.zb.history.get(**data)
        return ret
   
   ###############添加主机并且指定到组（传入主机名，IP地址和组ID）#####################
    def add_zabbix_host(self,hostname="test_zabbix",ip="192.168.10.100",groupid="2"):
        data = {
         "host": hostname,
         "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
         ],
         "groups": [
             {
                "groupid": groupid
             }
         ]
        }
        ret = self.zb.host.create(data)
        return ret
    #####################查看现有模板，绑定主机到模板#######################
    def get_template(self,hostid=10129):
        datalist = []
        datadict={}
        data = {
           "hostid": hostid,
           "output":["templateid","name"]
        }
        ret =  self.zb.template.get(data)
        for i in ret:
            datadict[i['name']] = i['templateid']
            datalist.append(datadict)
        return datalist 
     
     #################### 关联主机到模板##################################
    def link_template(self, hostid=10156, templateids=10001):
        data = {
            "hostid":hostid,
             "templates":templateids
        }      
   
        ret = self.zb.host.update(data)
        return ret
    
    ###################  添加维护周期，，######################################
  
    def create_maintenance(self,name="test",groupids=2,time=2):
        data =  {
            "name": name,
            "active_since": 1504233442,
            "active_till": 1504633442,
#            "hostids": [
            "groupids": [
                groupids
            ],
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": 3600
                }
            ]
        }
        ret = self.zb.maintenance.create(data)
#        self.host_status(hostids, 1)
        return ret
    ################获取维护周期，，#########################
    def get_maintenance(self):
        data = {
            "output": "extend",
            "selectGroups": "extend",
            "selectTimeperiods": "extend"
        }
        ret = self.zb.maintenance.get(data)
        return ret
    ##############获取维护周期之后，通过传入maintenanceid删除维护周期###########
    def del_maintenance(self,maintenanceids):
        return self.zb.maintenance.delete(maintenanceids) 
    #########################添加维护周期时候需要吧zabbix_host设置成非监控状态##################
    def host_status(self, hostid, status):
        data = {
            "hostid":hostid,
            "status":status
        }
        return self.zb.host.update(data)
    ###########通过hostids删除主机id,顺带也删除模板#########
     
    def host_del(self,hostids=10155):
        return self.zb.host.delete(hostids)

    def create_maintenance_for_group(self,name="test",groupids=8,time=7200):
        data =  {
            "name": name,
            "active_since": nowtime,
            "active_till": endtime,
            "groupids": [
                groupids
            ],
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": time
                }
            ]
        }
        ret = self.zb.maintenance.create(data)
        return ret

    def create_maintenance_for_host(self,name="test",host_list=[1,2,3],time=7200):
        data =  {
            "name": name,
            "active_since": nowtime,
            "active_till": endtime,
            "hostids":
                host_list,
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": time
                }
            ]
        }
        ret = self.zb.maintenance.create(data)
        return ret

    def del_maintenance_for_name(self,maintenance_name):
        maintenance_info_list = self.get_maintenance()
        for i in maintenance_info_list:
                if i.get('name') == maintenance_name:
                        maintenanceids = i['maintenanceid']
        return self.zb.maintenance.delete(maintenanceids)

    def get_groupid(self,group_name):
        groupid = None
        hostgroup = zabbix_server.get_hostgroup()
        for group in hostgroup:
            if group.get('name') == group_name:
                groupid = group.get('groupid')
        if groupid is None:
            print("{group_name} group not found in zabbix-server".format(group_name = group_name))
            exit(1)
        return groupid

    def get_hostid_list(self,group_name,host_list):
        hostid_list = []
        groupid = zabbix_server.get_groupid(group_name)
        hosts = zabbix_server.get_hostid(groupid)
        for host in hosts:
            if host.get('name') in host_list:
                hostid_list.append(host.get('hostid'))
        if len(hostid_list) == 0:
            print("{host_list} group not found in zabbix-server".format(host_list=host_list))
            exit(1)
        return hostid_list


if __name__ == "__main__":
    def usage():
        print 'usage:python {scripts_name} [create|delete] [hadoop|mongodb41|mongodb48|es_A|es_B]'.format(scripts_name=argv[0])
        exit(1)
    def maintenance_host_action(cluster_name,action,hostid_list):
        if action == 'create':
            zabbix_server.create_maintenance_for_host('{cluster_name} maintenance'.format(cluster_name=cluster_name),hostid_list,'72000000')
        elif action == 'delete':
            zabbix_server.del_maintenance_for_name('{cluster_name} maintenance'.format(cluster_name=cluster_name))
    def maintenance_group_action(cluster_name,action,groupid):
        if action == 'create':
            zabbix_server.create_maintenance_for_group('{cluster_name} maintenance'.format(cluster_name=cluster_name), groupid, '72000')
        elif action == 'delete':
            zabbix_server.del_maintenance_for_name('{cluster_name} maintenance'.format(cluster_name=cluster_name))
    def mongodb41(cluster_name,action):
        group_name = 'mongodb'
        host_list = ['mongo41','mongo42','mongo43']
        hostid_list = zabbix_server.get_hostid_list(group_name, host_list)
        maintenance_host_action(cluster_name,action,hostid_list)
    def mongodb48(cluster_name,action):
        group_name = 'mongodb'
        host_list = ['mongo48', 'mongo49', 'mongo50']
        hostid_list = zabbix_server.get_hostid_list(group_name, host_list)
        maintenance_host_action(cluster_name, action, hostid_list)
    def hadoop(cluster_name,action):
        group_name = 'Hadoop'
        groupid = zabbix_server.get_groupid(group_name)
        maintenance_group_action(cluster_name, action, groupid)
    def es_A(cluster_name,action):
        group_name = '4.0-es'
        host_list = ['es_75', 'es_76', 'es_77']
        hostid_list = zabbix_server.get_hostid_list(group_name, host_list)
        maintenance_host_action(cluster_name, action, hostid_list)
    def es_B(cluster_name,action):
        group_name = '4.0-es'
        host_list = ['es_72', 'es_73', 'es_74']
        hostid_list = zabbix_server.get_hostid_list(group_name, host_list)
        maintenance_host_action(cluster_name, action, hostid_list)
    zabbix_server = Zabbix()
    try:
        if len(argv) != 3:
            usage()
        else:
            action = argv[1]
            cluster_name = argv[2]
        if cluster_name in ['hadoop','mongodb41','mongodb48','es_A','es_B'] and action in ['create','delete']:
            zabbix_server = Zabbix()
            eval(cluster_name)(cluster_name,action)
        else:
            usage()
    except Exception,msg:
        print msg