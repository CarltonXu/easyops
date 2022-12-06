import logging
import json

from easyops import db
from easyops.models.models import Users, UsersLoginHistory

class UsersManager():
    def __init__(self, username=None, user_id=None):
        self.user_id = user_id
        self.username = username
        self.get_user()

    def get_user(self):
        try:
            if self.username is not None:
                self.user = Users.query.filter_by(username=self.username).first()
                self.user_id = self.user.id
            else:
                self.user = Users.query.filter_by(id=self.user_id).first()
        except Exception as err:
            logging.error(err)

    def create_user(self, username, password, register_time, avatar_path):
        try:
            user = Users(username=username,
                             register_time=register_time,
                             avatar=avatar_path)
            user.set_password = password
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            logging.error(err)

    def update_user_info(self, params):
        if self.check_user_exsits().get("user_id"):
            try:
                Users.query.filter_by(id=self.user_id).update(params)
                db.session.commit()
            except Exception as err:
                logging.error(err)
        else:
            return {
                "response_code": 3001,
                "errormsg": self.check_user_exsits().get("errormsg")
            }

    def set_user_login_state(self, state):
        self.user.is_login = state
        db.session.add(self.user)
        db.session.commit()

    def verify_login_code(self, session, verify_code_string):
        errormsg = None
        if session.get("image") is not None:
            if session.get('image').lower() != verify_code_string:
                errormsg = "验证码失败"
                res_code = 4001
            else:
                errormsg = "验证成功"
                res_code = 1006
        else:
            errormsg = "获取验证码错误"
            res_code = 4002
    
        return {
            "response_code": res_code,
            "errormsg": errormsg
        }

    def set_user_avatar(self, avatar_path):
        self.user.avatar = avatar_path
        db.session.commit()

    def set_user_password(self, password):
        self.user.set_password = password
        db.session.add(self.user)
        db.session.commit()

    def get_user_avatar_path(self):
        errormsg = None
        if self.user is None:
            errormsg = "用户不存在"
            res_code = 3002
        else:
            res_code = 1001
            user_avatar_path = self.user.avatar
    
        return {
            "response_code": res_code,
            "errormsg": errormsg,
            "user_avatar_path": user_avatar_path
        }
    
    def check_user_exsits(self):
        errormsg = None
        if self.user is None:
            errormsg = "用户不存在, 请注册后再登陆使用"
            res_code = 3002
            user_id = None
        else:
            res_code = 1001
            user_id = self.user_id
    
        return {
            "response_code": res_code,
            "errormsg": errormsg,
            "user_id": user_id,
        }
    
    def check_user_password(self, password):
        errormsg = None
        if not self.user.check_password(password):
            errormsg = "密码不正确"
            res_code = 3003
        else:
            res_code = 1002
        
        return {
            "response_code": res_code,
            "errormsg": errormsg
        }
    
    def check_user_login(self):
        errormsg = None
        if not self.user.is_login:
            errormsg = "用户未登录"
            res_code = 3004
        else:
            res_code = 1003
    
        return {
            "response_code": res_code,
            "errormsg": errormsg
        }
    
    def set_user_login_history(self, login_time, login_ipaddress, login_region):
        errormsg = None
        try:
            user_login_info = UsersLoginHistory(
                login_time=login_time,
                login_ipaddress=login_ipaddress,
                login_region=login_region,
                user_id=self.user_id, 
            )
            if self.check_user_login()["response_code"] == 3004:
                self.user.is_login = True
            db.session.add(user_login_info, self.user)
            db.session.commit()
        except Exception as err:
            errormsg = "操作数据库失败，请检查数据库."
            res_code = 3001
        else:
            res_code = 1004
        
        return {
            "response_code": res_code,
            "errormsg": errormsg
        }

    def get_user_login_history(self):
        errormsg = None
        try:
            users_login_info = UsersLoginHistory.query.filter_by(
                user_id=self.user_id).order_by(UsersLoginHistory.id.desc()).all()
        except Exception as err:
            errormsg = "操作数据库失败，请检查数据库."
            res_code = 3001
        else:
            res_code = 1005
    
        return {
            "response_code": res_code,
            "errormsg": errormsg,
            "user_history": users_login_info
        }
    
    def get_user_last_login_history(self):
        errormsg = None
        try:
            user_info = UsersLoginHistory.query.filter_by(
                user_id=self.user_id).order_by(UsersLoginHistory.id.desc()).offset(1).first()
        except Exception as err:
            errormsg = "操作数据库失败，请检查数据库."
            res_code = 3001
        else:
            res_code = 1005
        
        if user_info:
            user_history = {
                "last_login_time": user_info.login_time,
                "last_login_ipaddress": user_info.login_ipaddress,
                "last_login_region": user_info.login_region
            }
        else:
            user_history = {
                "last_login_time": "初次登陆",
                "last_login_ipaddress": "初次登陆",
                "last_login_region": "初次登陆"
            }
    
        return {
            "response_code": res_code,
            "errormsg": errormsg,
            "user_history": user_history
        }