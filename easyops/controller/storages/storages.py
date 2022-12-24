import argparse
import logging

from flask import jsonify
from easyops import db
from easyops.models.models import Storages

class StoragesManager:
    def __init__(self, user_id=None, storage_name=None, access_key_id=None):
        self.user_id = user_id
        self.storage_name = storage_name
        self.access_key_id = access_key_id
        self.get_storages()

    def get_storages(self):
        try:
            if self.user_id is not None and self.storage_name is not None:
                self.storages = Storages.query.filter_by(user_id=self.user_id, name=self.storage_name).all()
            else:
                self.storages = Storages.query.filter_by(user_id=self.user_id).all()
        except Exception as err:
            logging.error(err)

        return self.storages


    def create_storage(self, **kwargs):
        result = {
            "success": [],
            "fail": [] 
        }
        try:
            if not self.exists_storage():
                # 更新存储属性
                storage = Storages(**kwargs)
                db.session.add(storage)
                db.session.commit()
                result["success"] = storage
            else:
                result["fail"] = kwargs.name
        except Exception as err:
            logging.error(err)
        return result

    def exists_storage(self):
        try:
            if self.access_key_id is not None:
                self.exist_storage = Storages.query.filter_by(
                                       user_id=self.user_id,
                                       name=self.storage_name,
                                      access_key_id=self.access_key_id).first()
            else:
                self.exist_storage = Storages.query.filter_by(
                                       user_id=self.user_id,
                                       name=self.storage_name).first()
        except Exception as err:
            logging.error(err)

        return self.exist_storage

    def delete_storage(self):
        try:
            if self.exists_storage():
                db.session.delete(self.exist_storage)
                db.session.commit()
            msg = None
        except Exception as err:
            logging.error(err)
            msg = err
        return {"code": 0, "msg": msg }


    def update_storage(self, **kwargs):

        result = {
            "success": [],
            "fail": []
        }

        try:
            if self.exists_storage():
                # 定义存储属性和数据库字段的映射
                mapping = self.get_mapping()
                # 更新存储属性
                for k, v in kwargs.items():
                    if k in mapping:
                        setattr(self.exist_storage, mapping[k], v)

                # 提交到数据库
                db.session.commit()
                result["success"].append(kwargs.name)
            else:
                result["fail"].append(kwargs.name)
        except Exception as err:
            logging.error(err)
        return result
    
    def get_mapping(self):
        # 定义存储属性和数据库字段的映射函数,可以作为公共调用,更新等操作时
        return {
            "name": "name",
            "type": "type",
            "provider": "provider",
            "region": "region",
            "access_key_id": "access_key_id",
            "secret_access_key": "secret_access_key",
            "endpoint": "endpoint",
            "acl": "acl",
            "storclass": "storclass",
            "upload_cutoff": "upload_cutoff",
            "chunk_size": "chunk_size",
            "upload_checksum": "upload_checksum",
            "user_id": self.user_id
        }
