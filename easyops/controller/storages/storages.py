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
        try:
            self.storage = Storages(
                name=kwargs["name"],
                type=kwargs["type"],
                provider=kwargs["provider"],
                region=kwargs["region"],
                access_key_id=kwargs["access_key_id"],
                secret_access_key=kwargs["secret_access_key"],
                endpoint=kwargs["endpoint"],
                acl=kwargs["acl"],
                storclass=kwargs["storclass"],
                upload_cutoff=kwargs["upload_cutoff"],
                chunk_size=kwargs["chunk_size"],
                upload_checksum=kwargs["upload_checksum"],
                user_id=kwargs["user_id"]
                )

            db.session.add(self.storage)
            db.session.commit()
        except Exception as err:
            logging.error(err)
        return self.storage

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
        except Exception as err:
            logging.error(err)
        return {"code": 0}