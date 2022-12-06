import logging

from easyops import db
from easyops.models.models import AnsibleHosts

class HostsManager():
    def __init__(self, user_id=None, ipaddress=None):
        self.user_id = user_id
        self.ipaddress = ipaddress
        self.get_hosts()

    def get_hosts(self):
        try:
            if self.user_id is not None and self.ipaddress is not None:
                self.hosts = AnsibleHosts.query.filter_by(user_id=self.user_id, ipaddress=self.ipaddress).all()
            elif self.user_id is not None:
                self.hosts = AnsibleHosts.query.filter_by(user_id=self.user_id).all()
            else:
                self.hosts = AnsibleHosts.query.all()
        except Exception as err:
            logging.error("Failed to get hosts %s" % err)
    
    def add_host(self, **kwargs):
        try:
            kwargs["user_id"] = self.user_id
            host = AnsibleHosts(**kwargs)
            db.session.add(host)
            db.session.commit()
        except Exception as err:
            logging.error(err)

            return False

        return True
    
    def delete_host(self, ipaddress=None):
        if ipaddress is not None:
            self.ipaddress = ipaddress
            self.__init__(user_id=self.user_id, ipaddress=self.ipaddress)
        try:
           db.session.delete(self.hosts[0])
           db.session.commit()
        except Exception as err:
            logging.error(err)
            return False

        return self.ipaddress

    def update_host(self, **kwargs):
        try:
            AnsibleHosts.query.filter_by(
                user_id=self.user_id,
                ipaddress=self.ipaddress).update(kwargs)
            db.session.commit()
        except Exception as err:
            logging.error(err)

            return False

        return self.ipaddress

    def check_host_exists(self, ipaddress=None):
        if ipaddress is not None:
            self.ipaddress = ipaddress
        for host in self.hosts:
            if self.ipaddress != host.ipaddress:
                continue
            else:
                return self.ipaddress
        return False