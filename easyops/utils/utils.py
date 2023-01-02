#!/usr/bin/env python
# coding: utf-8

import os
import time
import logging
import re
import psutil
import xlrd

def check_ip(ipAddr):
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True    
    else:    
        return False

def setup_logging(log_path="/var/log/easyops/easyops.log",
                  debug=False,
                  verbose=False,
                  log_name="easyops"):
    """Set up global logs

    By default, script will create a log directory in the same path
    with the script. Or you can specify the directory yourself.

    To use logging in this code in anywhere, just import logging.

    """

    if log_path is None:
        log_path = os.path.join(current_dir(), "log")

    if not os.path.exists(log_path):
        mkdir_p(log_path)

    # Default log settings
    log_format = "%(asctime)s %(process)s %(levelname)s [-] %(message)s"
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG
        log_file = os.path.join(log_path, "%s.debug.log" % log_name)
    else:
        log_file = os.path.join(log_path, "%s.log" % log_name)

    if verbose:
        logging.basicConfig(
            format=log_format,
            level=log_level)
    else:
        logging.basicConfig(
            format=log_format,
            level=log_level,
            filename=log_file)

def sort_directory_list(a, b):

    if a['is_dir'] != b['is_dir']:
        if a['is_dir']:
            return -1
        else:
            return 1
    if a['name'] > b['name']:
        return 1
    elif a['name'] < b['name']:
        return -1
    return 0

def insertServersFromExcel(excelPath):
    hosts = {}
    book = xlrd.open_workbook(excelPath)
    sheet = book.sheet_by_index(0)
    if sheet.name != "servers":
        return False
    rowsnumber = sheet.nrows
    colsnumber = sheet.ncols
    num = 0
    for i in range(0, rowsnumber):
        value = []
        for j in range(0, colsnumber):
            value.append(sheet.cell(i, j).value)
        if i != 0:
            hosts[num] = value
            num += 1

    return hosts

def get_host_details(ip, exec_rets):
    data = {}
    interfaces = {}
    mounts = {}
    disks = {}
    ansible_facts = exec_rets.get("success").get(ip).get("ansible_facts")
    hostname = ansible_facts.get('ansible_hostname')

    description = ansible_facts.get('ansible_distribution')
    distribution_version = ansible_facts.get('ansible_distribution_version')
    distribution_release = ansible_facts.get('ansible_distribution_release')
    sysinfo = '%s Linux release %s (%s)' % (description, distribution_version, distribution_release)

    os_kernel = ansible_facts.get('ansible_kernel')
    os_family = ansible_facts.get('ansible_os_family')

    cpu_processor = ansible_facts.get('ansible_processor')[2]
    cpu_count = ansible_facts.get('ansible_processor_count')
    cpu_cores = ansible_facts.get('ansible_processor_cores')
    processor_vcpus = ansible_facts.get('ansible_processor_vcpus')
    memory_totalmb = ansible_facts.get('ansible_memtotal_mb')
    memory_freemb = ansible_facts.get('ansible_memfree_mb')

    # Get interfaces info from ansible facts.
    interface_list = [ x for x in ansible_facts.get("ansible_interfaces") if x.startswith("ens") or x.startswith("eth") or x.startswith("eno") ]
    for net in interface_list:
        interfaces[net] = {}
        interface_obj_name = "ansible_" + net
        interface_obj = ansible_facts.get(interface_obj_name)
        if interface_obj.get("ipv4"):
            interfaces[net]["address"] = interface_obj.get("ipv4")["address"]
            interfaces[net]["netmask"] = interface_obj.get("ipv4")["netmask"]
        else:
            interfaces[net]["address"] = "Not ipaddress"
            interfaces[net]["netmask"] = "Not netmask"

        interfaces[net]["macaddress"] = interface_obj.get("macaddress")
        if interface_obj.get("active"):
            interfaces[net]["active"] = "Up"
        else:
            interfaces[net]["active"] = "Down"
        interfaces[net]["module"] = interface_obj.get("module")
        interfaces[net]["mtu"] = interface_obj.get("mtu")
        interfaces[net]["speed"] = interface_obj.get("speed")
        interfaces[net]["type"] = interface_obj.get("type")
    
    for part in ansible_facts.get("ansible_mounts"):
        if "bind" in part.get("options").split(","):
            continue
        device_name = part.get("device")
        mounts[device_name] = {}
        mounts[device_name]["device"] = part.get("device")
        mounts[device_name]["fstype"] = part.get("fstype")
        mounts[device_name]["mount"] = part.get("mount")
        mounts[device_name]["size_available"] = round(part.get("size_available") / 1024 / 1024 / 1024)
        mounts[device_name]["size_total"] = round(part.get("size_total") / 1024 / 1024 / 1024)
        mounts[device_name]["size_usage"] = int(((mounts[device_name]["size_total"] - mounts[device_name]["size_available"]) / mounts[device_name]["size_total"]) * 100)
    
    for disk in ansible_facts.get("ansible_devices").keys():
        if disk.startswith("sr") or disk.startswith("fd"):
            continue
        disks[disk] = {}
        disk_obj = ansible_facts.get("ansible_devices")[disk]
        disks[disk]["size"] = disk_obj.get("size")
        disks[disk]["vendor"] = disk_obj.get("vendor")
        if disk_obj.get("model"):
            disks[disk]["model"] = disk_obj.get("model")
        else:
            disks[disk]["model"] = "NO"
        disks[disk]["virtual"] = disk_obj.get("virtual")

    product_name = ansible_facts.get('ansible_product_name')
    system_vendor = ansible_facts.get('ansible_system_vendor')
    architecture = ansible_facts.get('ansible_architecture')
    os_uptime_hours = int(ansible_facts.get('ansible_uptime_seconds') / 3600)

    # print sysinfo
    data['sysinfo'] = sysinfo
    data['cpu_processor'] = cpu_processor
    data['cpu_count'] = cpu_count
    data['cpu_cores'] = cpu_cores
    data['cpu_processor_vcpus'] = processor_vcpus
    data['memory_totalmb'] = memory_totalmb
    data['memory_freemb'] = memory_freemb
    data['memory_usage'] = int(((memory_totalmb - memory_freemb) / memory_totalmb) * 100)
    data['interfaces'] = interfaces
    data['mounts'] = mounts
    data['disks'] = disks
    data['os_kernel'] = os_kernel
    data['os_family'] = os_family
    data['hostname'] = hostname
    data['product_name'] = product_name
    data['system_vendor'] = system_vendor
    data['architecture'] = architecture
    data['os_uptime_hours'] = os_uptime_hours

    return data

def get_local_usages():
    # 获取cpu占用率（百分比）
    cpu_percent = psutil.cpu_percent()
    # 获取CPU负载（1、5、15分钟的平均负载）
    cpu_load_avg = psutil.getloadavg()
    # 获取内存占用信息
    memory = psutil.virtual_memory()
    # 内存总量（单位：字节）
    memory_total = memory.total
    # 已使用内存量（单位：字节）
    memory_used = memory.used
    # 内存占用率（百分比）
    memory_percent = memory.percent

    cpu_load_avg = f"{cpu_load_avg[0]:.2f}, {cpu_load_avg[1]:.2f}, {cpu_load_avg[2]:.2f}"

    return {
        "cpu": {
            "percent": cpu_percent,
            "load_avg": cpu_load_avg,
        },
        "memory": {
            "total": int(memory_total / 1000 / 1000 / 1000),
            "used": int(memory_used),
            "percent": memory_percent
        }
    }

def get_network_speed():
    net_devices, first_recv, first_sent = get_network_devices()
    time.sleep(1)
    net_devices, second_recv, second_sent = get_network_devices()

    data = []
    for device in net_devices:
        data.append({
            "name": device,
            "rx_rate": float('%.2f' %((second_recv.get(device) - first_recv.get(device)) / 1000)),
            "tx_rate": float('%.2f' %((second_sent.get(device) - first_sent.get(device)) / 1000)) 
        })
    
    return data

def get_network_devices():
    net_devices = psutil.net_io_counters(pernic=True)
    devices = []
    recv = {}
    sent = {}

    for device, info in net_devices.items():
        if device[:2] not in ["en", "et", "pp"]:
            continue
        devices.append(device)
        recv.setdefault(device, info.bytes_recv)
        sent.setdefault(device, info.bytes_sent)

    return devices, recv, sent