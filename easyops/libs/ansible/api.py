#!/usr/bin/env python
# coding:utf-8

import json
import shutil

import ansible.constants as C
from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


# 这里为封装的返回信息，让我们获取返回信息更加方便进行处理
class ResultCallback(CallbackBase):
    def __init__(self, *args):
        super(ResultCallback, self).__init__(display=None)
        self.status_ok = json.dumps({}, ensure_ascii=False)
        self.status_fail = json.dumps({}, ensure_ascii=False)
        self.status_unreachable = json.dumps({}, ensure_ascii=False)
        self.status_playbook = ''
        self.status_no_hosts = False
        self.host_ok = {}
        self.host_failed = {}
        self.host_unreachable = {}

    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        self.runner_on_ok(host, result._result)
        self.host_ok[host] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, ignore_errors)
        self.host_failed[host] = result

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        self.host_unreachable[host] = result


class Task():
    def __init__(self,
                 connection="smart",
                 remote_user=None,
                 remote_password=None,
                 private_key_file=None,
                 sudo=None, sudo_user=None, ask_sudo_pass=None,
                 module_path=None,
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=False, diff=False,
                 listhosts=None, listtasks=None, listtags=None,
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None):

        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            remote_password=remote_password,
            private_key_file=private_key_file,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            verbosity=verbosity,
            syntax=syntax,
            start_at_task=start_at_task
        )

        self.inventory = inventory if inventory else "localhost"

        self.loader = DataLoader()

        self.inv_obj = InventoryManager(loader=self.loader,
                                        sources=self.inventory)

        self.variable_manager = VariableManager(loader=self.loader,
                                                inventory=self.inv_obj)

        self.passwords = dict(vault_pass="secret")

        self.results_callback = ResultCallback()

    def run(self, hosts="localhost", gather_facts="no",
            module="ping", args="", task_time=0):

        play_source = dict(
            name="Ansible Ad-hoc Play",
            hosts=hosts,
            gather_facts=gather_facts,
            tasks=[
                {"action": {
                    "module": module,
                    "args": args
                },
                 "async": task_time,
                 "poll": 0
                }
            ]
        )
        play = Play().load(play_source,
                           variable_manager=self.variable_manager,
                           loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()
        # Remove ansible tmpdir
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def get_result(self, exec_hosts=None):
        # 执行任务
        result_all = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.results_callback.host_ok.items():
            result_all['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            result_all['failed'][host] = result._result

        for host, result in self.results_callback.host_unreachable.items():
            result_all['unreachable'][host] = result._result
        return result_all


if __name__ == '__main__':
    res = Task(inventory="/Users/CarltonXu/workspace/codes/flask/easyops/inventory.py")
    res.run("192.168.10.68", module='setup', args='')
    print(res.get_result())