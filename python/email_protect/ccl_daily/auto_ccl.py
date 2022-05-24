#!/usr/bin/env python3
from genericpath import exists
import json
import argparse
from posixpath import realpath, relpath
import pprint
import sys
import time
import os
import shutil
import fcntl
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
import smtplib
import logging
from jinja2 import Environment, BaseLoader
import requests
from bs4 import BeautifulSoup
import logging.handlers
import hashlib
import datetime
mail_html_body="""
<html>
        <head></head>
        <body>
            <b>Hello, Test email</b><p>
            <i>Hello, Test email</i>
        </body>
    </html>
"""
cmd_args =  None
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', '--cfg', dest= "cfg", type=str, help='Runtime config json file')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help='Show current config')
parser.add_argument('--cleanup', dest='cleanup', action="store_true", help='Cleanup old tests')
parser.add_argument('--check_new_deploy', dest='check_new_deploy', action="store_true", help='Check the latest deploy test')
parser.add_argument('--get_test_result', dest='get_test_result', action="store_true", help='Check the latest deploy test')
parser.add_argument('--test_dir', dest='test_dir', type=str, action="store", help='Use this dir to do the full regression')
parser.add_argument('--check_lock', dest='check_lock', action="store_true", help='Check single instance status')
parser.add_argument('--email_report_test', dest='email_report_test', action="store", help='Send A test report email to some one')
parser.add_argument('--email_send_test', dest='email_send_test', action="store", help='Send A test email to some one')
parser.add_argument('--render_test', dest='render_test', action="store", help='Send A email_template ')
parser.add_argument('--skip_test', dest='skip_test', action="store_true", help='skip test regression ')
parser.add_argument('--ignore_flag', dest='ignore_flag', action="store_true", help='ignore done/abort/interrupt flag ')
parser.add_argument('--query_portal_email', dest='query_portal_email', action="store_true", help='Get Email list from diag portal ')
parser.add_argument('--update_email_library', dest='update_email_library', action="store_true", help='Update common email library')

class ResultParserBase:
    def __init__(self) -> None:
        pass
    def GetTestResult(result_file) -> None:
        pass

class ResultParserVCN(ResultParserBase):
    def __init__(self) -> None:
         super().__init__()
    def GetTestResult(self, result_file):
        result = {"Status": "",
                "PassCases" : [],
                "PassCasesSecond" : [],
                "FailCases" : [],
                "PendingCases" : [],
                "UnSortedCases" : [],
                "UnRunCases" : []
        }
        #print("open result file ", result_file)
        if os.path.exists(result_file) == False:
            return result
        line_max = 99999
        line_index = 0
        try:

            with open(result_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line_index = line_index + 1
                    if line_index > line_max:
                        break
                    line_split = line.split()
                    line_split_num = len(line_split)
                    case_msg = ""
                    case_id = ""
                    #print("parse line : %d %s"%(line_index, line))
                    if line_split_num < 4 :
                        if line_split_num == 3 and line_split[1][0] == "#":
                            case_id = line_split[2].split("_")[-1]
                            case_msg = line
                            result["UnRunCases"].append([case_id, case_msg])
                        else :
                            #print("skip line : ", line)
                            pass
                        continue
                    case_id = line_split[3].split("_")[-1]
                    #print("parse line : ", line_split_num, line)
                    if line_split_num == 4 and line_split[0][0] =="*":
                        case_id = line_split[3].split("_")[-1]
                        case_msg = line
                        result["UnRunCases"].append([case_id, case_msg])
                        continue


                    case_msg = line
                    #print("parse line -->", line)
                    if line_split_num == 5:
                        if line_split[4] == "Passed" :
                            result["PassCases"].append([case_id, case_msg])
                    elif line_split_num >= 6:
                        if line_split[6] == "Passed":
                            result["PassCasesSecond"].append([case_id, case_msg])
                        elif line_split[6] == "Failed":
                            result["FailCases"].append([case_id, case_msg])
                        elif line_split[6] == "Hang":
                            result["PendingCases"].append([case_id, case_msg])
                        else:
                            result["UnSortedCases"].append([case_id, case_msg])

        except Exception as ex:
            result["error"] = "read result file exception: %s index: %d"%(ex, line_index)
        if len(result["UnSortedCases"]) == 0 \
            and len(result["FailCases"])  == 0 \
            and len(result["UnRunCases"])  == 0 \
            and len(result["PendingCases"])  == 0 \
            and len(result["PassCases"]) > 0  :
            result["Status"] = "Pass"
        else :
            result["Status"] = "Fail"
        return result



class AutoCcl:
    def __init__(self, cfg):
        self.cfg = cfg
        self.result = {}
        self.test_dir_override = None
        self.cur_test_dir = None
        self.InitLogger()
        self.cur_file_dir= AutoCcl.GetFileDir()
        logging.debug("script dir -> %s"%self.cur_file_dir)
        self.mail_template_path = None
        if os.path.exists(self.cfg["mail"]["template"]):
            self.mail_template_path = self.cfg["mail"]["template"]
        else:
            real_path  =  self.cur_file_dir + "/" + self.cfg["mail"]["template"]
            if os.path.exists(real_path) :
                self.mail_template_path = real_path
        if self.mail_template_path == None:
            raise Exception("email template can not be found")
    @staticmethod
    def GetFileDir():
        return os.path.dirname( os.path.realpath(__file__) )


    def SendInterruptReport(self, interrupt_test_dir):
        print("Send Interupt report: -> ",interrupt_test_dir )
        pass

    def CheckSingleInstance(self):
        file_name=os.path.basename(__file__)
        print("file name -> ", file_name)
        lock_file_name = "/var/run/{file_name}.pid"
        self.instance_fd = open(lock_file_name, "w")
        try:
            fcntl.flock(self.instance_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.instance_fd.writelines(str(os.getpid()))
            self.instance_fd.flush()
        except Exception as ex:
            print("Another instance is already runing")
            return False
        return True
    def GetLatestDeployDir(self):
        diag_dir = self.cfg["diag_dir"]
        logging.debug("Will get the latest Deplay Dir ->%s"%diag_dir)
        cmd = "ls -ltc "+ diag_dir

        lines = os.popen(cmd).readlines()
        print(lines)
        for line in lines:
            line_split= line.split()
            if len(line_split) < 3:
                continue
            path = diag_dir + "/" + line_split[-1]
            #print("check path->",path,"<-")
            #print(os.stat(path)) mtime last modify time
            if os.path.isdir(path) == False:
                continue
            if self.IsDeployDone(path):
                logging.debug("the latest dir is %s"%path)
                return path
            else:
                logging.debug("Test may not be deployed correctly: %s"%path)
        return None
    def GetLastDeployDir(self):
        diag_dir = self.cfg["diag_dir"] + "/" + self.cfg["current_job_file"]
        try:
            with open(diag_dir) as f:
                lines = f.readlines()
                return lines[-1].replace("\n","")
        except Exception as ex:
            return None
    def SetCurrentJobDir(self, dir):
        print("set current job dir: ", dir)
        diag_dir = self.cfg["diag_dir"] + "/" + self.cfg["current_job_file"]
        with open(diag_dir, "w+") as f:
            lines = f.readlines()
            lines.append(dir+"\n")
            f.writelines(lines)
    def IsDeployDone(self, test_dir):
        deploy_done_path = test_dir + "/" + self.cfg["deploy_done_flag_file"]
        return os.path.exists(deploy_done_path)




    def ExistedDoneFlag(self,test_dir):
        path = test_dir + "/" + self.cfg["done_flag_file"]
        return os.path.exists(path)
    def ExistedAbortFlag(self,test_dir):
        path = test_dir + "/" + self.cfg["abort_flag_file"]
        return os.path.exists(path)
    def ExistedInterruptFlag(self,test_dir):
        path = test_dir + "/" + self.cfg["interrupt_flag_file"]
        return os.path.exists(path)
    def AddDoneFlag(self,test_dir):
        path = test_dir + "/" + self.cfg["done_flag_file"]
        with open(path,"w") as fd:
            fd.write(test_dir)
        logging.debug("add Done Flag : %s"%path)
        if os.path.exists(path) == False:
            print("Add flag file fail : ", path)
    def AddAbortFlag(self,test_dir):
        path = test_dir + "/" + self.cfg["abort_flag_file"]
        with open(path,"w") as fd:
            fd.write(test_dir)
        if os.path.exists(path) == False:
            print("Add flag file fail : ", path)
    def AddInterruptFlag(self,test_dir):
        path = test_dir + "/" + self.cfg["interrupt_flag_file"]
        with open(path,"w") as fd:
            fd.write(test_dir)
        if os.path.exists(path) == False:
            print("Add flag file fail : ", path)

    def SetTestDir(self, dir):
        self.test_dir_override = dir
        self.cur_test_dir = dir
    def GetTestDir(self):
        if self.test_dir_override:
            return self.test_dir_override
        return self.cur_test_dir

    def SendReportEmail(self, test_dir, result):
        logging.debug("Send Report Email from template %s"%self.mail_template_path)
        #print("Pre info", self.sys_info_pre_run)
        #print("After info", self.sys_info_pre_run)
        body = auto_ccl_inst.EmailBodyRender(self.mail_template_path, result)

        logging.debug("reader done")
        attach_list = auto_ccl_inst.GetResultFileList()
        email_receiver_list = []

        if cmd_args.email_report_test:
            email_receiver_list = cmd_args.email_report_test.split(",")
        else :
            if self.cfg["mail"]["diag_portal_mail_first"]:
                email_list = self.QueryDiagPortalEmail()
                if len(email_list) > 0 :
                    email_receiver_list = email_list
        auto_ccl_inst.SendEmail(email_receiver_list, body, attach_list)

    def CollectTestInfo(self, test_dir):
        result = {
            "Board": "",
            "Project" : "",
            "Hostname" : "",
            "ClkStatus" : "",
            "BuildTime" : "",
            "BiosVersion" : "",
            "CollectTs" :time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        buf  = os.popen("hostname").readlines()
        if len(buf) > 0:
            result["Hostname"] = buf[0].replace("\n", "")
        buf  = os.popen("dmidecode -s bios-version").readlines()
        if len(buf) > 0:
            result["BiosVersion"] = buf[0].replace("\n", "")
        tserver_path = test_dir + "/" + "tserverlite" + " 2>&1"
        buf = os.popen(tserver_path).readlines()
        if len(buf) > 3:
            #print("BUF------->", buf)
            #for i in range(0,3):
            #    print("line ", i, buf[i])
            result["Project"] = buf[0].split()[2]
            result["BuildTime"] = buf[1].split()[3]
            result["GitVersion"] = buf[2].split()[3]
        atitool_path = test_dir + "/" + "atitool  -clkstatus"
        buf = os.popen(atitool_path).read()
        if len(buf) > 100 :
            result["ClkStatus"] = buf
            pass

        return result
    def SetFlagFile(self,file):
        pass
    def LoadCfg(self, file):
        return None
    def CleanUpOldTest(self):
        print("will clean up old test", self.cfg["diag_dir"])
        print("cleanup threshold : ", self.cfg["clean_up_days"], " days")
        dir_list = os.listdir(self.cfg["diag_dir"])
        cur_ts = int(time.time() )
        for dir in dir_list:
            dir_path = self.cfg["diag_dir"] + "/" + dir
            if os.path.isdir(dir_path) == False:
                continue
            dir_mtime = int(os.stat(dir_path).st_mtime)
            msg = "%s mk_ts:%d cur:%d"%(dir_path, dir_mtime, cur_ts)
            threshold_second =  self.cfg["clean_up_days"] * 24 * 60 * 60
            if cur_ts - dir_mtime > threshold_second :
                logging.debug("Clean Up Old test  ->%s"%dir_path)
                shutil.rmtree(dir)
            else :
                print(msg, "  ->fine")

        pass
    def ShowCfg():
        pass
    def SendAbortReport(self, job_dir):
        pass
    def StartRegression(self, job_dir):
        self.PrepreRunEnv(job_dir);
        pwd = os.getcwd()
        os.chdir(job_dir)
        logging.debug("start regression %s %s"%(pwd, job_dir))
        for module  in self.cfg["modules"]:
            #print("Paser result from :", k, v)
            name = module["name"]
            cmd = module["cmd"]
            logging.debug("Run Regression cmd :%s "%cmd)
            logging.debug("start regression %s %s %s %s"%(pwd, job_dir, name, cmd))
            #print("Run module: ", k, cmd)

            try:
                os.system(cmd)
                logging.debug("Regression Done %s %s %s %s"%(pwd, job_dir, name, cmd))
            except Exception as ex:
                error_msg = "%s run exception %s"%(name, ex)
                return (False, error_msg)
        os.chdir(pwd)
        return (True, None)

    def GetRegressionResult(self, job_dir):
        result = {
            "StatusAll": "Pass",
            "AbortedModule": [],
            "FailedModules": [],
            "PassedModules" : [],
            "UnFinishedModules" : [],
            "Detail": {}
        }

        for module in self.cfg["modules"]:
            #print("Paser result from :", k, v)
            name = module["name"]
            parser_module = module["parser"]
            parser = eval(parser_module+ "()")
            module_result = parser.GetTestResult(job_dir + "/" + module["result_file"])

            #print(module_result)
            result["Detail"][name] = module_result
        status_all = ""
        for k,v  in result["Detail"].items():
            logging.debug("Regression: %s  Pass: %d SecPass: %d Fail: %d Pend: %d UnSort: %d"%(k, len(v["PassCases"]), len(v["PassCasesSecond"]),len(v["FailCases"]),len(v["PendingCases"]), len(v["UnSortedCases"]), ))
            threshold = module["fail_threshold"]
            if threshold == -1:
                continue
            failed_cases_num = len(v["FailCases"]) + len(v["PendingCases"]) + len(v["UnSortedCases"])

            if failed_cases_num > threshold:
                result["StatusAll"] = "Fail"
                result["AbortedModule"].append(k)
                result["FailedModules"].append(k)
            elif failed_cases_num > 0:
                result["FailedModules"].append(k)
            elif len(v["UnRunCases"]) > 0 :
                result["UnFinishedModules"].append(k)
            else:
                result["PassedModules"].append(k)
        logging.debug("Regression Status: %s Pass: %s Fail: %s Abort: %s UnRun: %s"%(result["StatusAll"], ",".join(result["PassedModules"]),",".join(result["FailedModules"]), ",".join(result["AbortedModule"]),",".join(result["UnFinishedModules"])   ))
        #pprint.pprint(result)
        return result
    def PrepreRunEnv(self, job_dir):
        pass
    def Run(self):
        #check single instance
        if self.CheckSingleInstance() == False:
            return
        latest_test_dir = None
        current_job_test_dir = None
        self.test_dir = None

        if self.test_dir_override != None :
            self.cur_test_dir = self.test_dir_override
        else :
            latest_test_dir = auto_ccl_inst.GetLatestDeployDir()
            current_job_test_dir = auto_ccl_inst.GetLastDeployDir()
            self.cur_test_dir = current_job_test_dir
            print("Latest Deploy  -> ", latest_test_dir, "<-")
            print("Last Runing Job-> ", current_job_test_dir,"<-")
            if current_job_test_dir == None:
                if latest_test_dir == None:
                    logging.debug("no new deploy to run")
                    return
                self.SetCurrentJobDir(latest_test_dir)
                self.cur_test_dir = latest_test_dir
            elif current_job_test_dir != latest_test_dir:
                print("Last Test is not match the current job in flag file")
                #Send Interrupt mail
                self.SendInterruptReport(current_job_test_dir)
                self.AddInterruptFlag(current_job_test_dir)
                self.SetCurrentJobDir(latest_test_dir)
                self.cur_test_dir = latest_test_dir
            else :
                print("last test dir is same with the last test job")
                logging.debug("last test dir is same with the last test job -> %s"%current_job_test_dir)
                pass
        #print("Will start regression on -> ", self.cur_test_dir)
        logging.debug("Will start regression on -> %s"%self.cur_test_dir)
        if self.ExistedAbortFlag(self.cur_test_dir) :
            print("current job has been aborted", self.cur_test_dir)
            return
        if self.ExistedDoneFlag(self.cur_test_dir) and cmd_args.ignore_flag == False :
            print("Current job has been finished", self.cur_test_dir)
            return
        self.result = self.GetRegressionResult(self.cur_test_dir)
        #pprint.pprint(self.result)

        if len(self.result["AbortedModule"]) > 0 :
            self.AddAbortFlag(self.cur_test_dir)
            return
        #start regression
        self.sys_info_pre_run = self.CollectTestInfo(self.cur_test_dir)
        result = None
        if self.cfg["skip_regression"] or cmd_args.skip_test:
            logging.debug("Skip Regression for setting")
        else:
            try:
                result = self.StartRegression(self.cur_test_dir)
            except Exception as ex:
                logging.error("Run regression fail: %s %s"%(self.cur_test_dir, ex))
                pass
            if result[0] :
                logging.debug("Run Regresion Done");
            else:
                logging.error("Run Regression fail -> %s"%result[1])
        self.sys_info_after_run = self.CollectTestInfo(self.cur_test_dir)
        self.result = self.GetRegressionResult(self.cur_test_dir)
        self.result["post_sys_info"] = self.sys_info_after_run
        self.result["pre_sys_info"] = self.sys_info_pre_run
        self.result["test_dir"] = self.cur_test_dir
        self.result["diag_portal_job"] = self.cfg["diag_portal"]["job_url"]
        self.result["diag_portal_task"] =  "http://diag-portal/tasks/" + self.cur_test_dir.split("_")[-1]
        self.SendReportEmail(self.cur_test_dir, self.result)
        #if self.result["StatusAll"] == "Done":
        self.BackUpLogs(self.cur_test_dir)
        self.AddDoneFlag(self.cur_test_dir)
    def BackUpLogs(self, dir):
        backup_base_dir = self.cfg["backup_dir"]
        logging.debug("back up logs %s"%backup_base_dir)
        if os.path.exists(backup_base_dir) == False:
            os.mkdir(backup_base_dir)
        dir_name = dir.split("/")[-1]
        if dir[-1] == '/':
            dir_name = dir.split("/")[-2]

        cur_backup_dir =  backup_base_dir + "/" + dir_name + "_" + time.strftime("%Y_%m_%d_%H_%M", time.localtime())
        if os.path.exists(cur_backup_dir) == False:
            os.mkdir(cur_backup_dir)

        for v in self.cfg["modules"]:
            name = v["name"]
            dst_path = cur_backup_dir + "/" + name + "__" + v["result_file"].replace("/", "_")
            src_path = dir + "/" + v["result_file"]
            logging.debug("backup from %s ->%s"%(src_path, dst_path))
            try:
                shutil.copy(src_path, dst_path)
            except Exception as inst:
                logging.error("backup file error: %s --> %s", src_path, dst_path)
        pass
    def SendEmailWithExtraLibrary(self, receiver_list, subject, mail_body, attach_list):
        self.check_and_update_email_library()
        from email_utils import MailUtils
        mail= MailUtils()
        mail.SendEmail(receiver_list, subject, mail_body, attach_list)
    def SendTestEmail(self, receiver_list):
        mail_body = "test email"
        subject = "test email title"
        attach_list = []
        self.SendEmailWithExtraLibrary(receiver_list, subject, mail_body, attach_list)
    def SendEmail(self, receiver_list, mail_body, attach_list):
        logging.debug("send mail to : %s"%receiver_list)
        msg = MIMEMultipart()
        subject=self.cfg["mail"]["mail_title"] + " " + time.strftime("%Y-%m-%d %H:%M", time.localtime())
        self.SendEmailWithExtraLibrary(receiver_list, subject, mail_body, attach_list)
        return
    def GetFileAbsPath(self, path):
        logging.debug("try get file real path: %s"%path)
        result = None
        if os.path.exists(path) :
            result = path
        else:
            real_path = self.cur_file_dir + "/" + path
            print("real_path ", real_path)
            if os.path.exists(real_path) :
                result = real_path
            else:
                raise Exception("Cat not get file abs path: %s"%path)
                print("can not find the cfg file")
        return result
    def EmailBodyRender(self, tempplate_file, render_data ):
        temp_str = ""
        real_temp_path = self.GetFileAbsPath(tempplate_file)
        logging.debug("render email with template : %s : %s"%(tempplate_file, real_temp_path))
        with open (real_temp_path, "r") as fd:
            temp_str = fd.read()
        tpl = Environment(loader=BaseLoader).from_string(temp_str)
        data = tpl.render(dat=render_data)
        logging.debug("rend email content from ->%s"%tempplate_file )
        #print(data)
        return data
    def GetResultFileList(self):
        attach_list = []
        if self.test_dir_override:
            self.cur_test_dir = self.cur_test_dir
        for v  in self.cfg["modules"]:
            k = v["name"]
            file_path = self.cur_test_dir + "/" + v["result_file"]
            file_name = k + "_" + file_path.split("/")[-1]
            print("file,", k, file_path, file_name)
            if os.path.isfile(file_path) == False:
                logging.error("target result file can not be found->%s"%file_path)
                continue
            attach_list.append([file_path, file_name])
            log_dir = v["log_dir"]
            if len(log_dir) == 0:
                logging.error("please add log dir para into json, other wise the log will not uploaded")
            log_full_path =  self.cur_test_dir + "/" + log_dir
            if os.path.isdir(log_full_path) == False:
                logging.error("target log dir is not a dir->%s"%log_full_path)
                continue
            tar_file_name ="log_" +  k + ".tar.gz"
            target_tar_path = self.cur_test_dir + "/" + tar_file_name
            tar_cmd = "tar czvf " + target_tar_path + " " +  log_full_path
            os.system(tar_cmd)
            attach_list.append([target_tar_path, tar_file_name])
        logging.debug("attach file list : %s"%attach_list)
        return attach_list
    def InitLogger(self):
        logger_format = "[%(asctime)15s] [%(name)s] [%(levelname)8s] %(message)s   (%(pathname)s:%(lineno)s)"#________________
        date_format = '%Y/%m/%d %H:%M:%S' #____________________________________________
        logger_file = self.cfg["logger"]["log_file"]
        dirname = os.path.dirname(logger_file)
        print("log dir name ", dirname)
        if os.path.exists(dirname) == False:
            os.mkdir(dirname)

        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename =logger_file,

                                                  maxBytes = 1024 * 1024 * 50,

                                                  backupCount = 5)

        formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

        rotatingFileHandler.setFormatter(formatter)

        logging.getLogger("").addHandler(rotatingFileHandler)

        #define a handler whitch writes messages to sys

        console = logging.StreamHandler()

        console.setLevel(logging.NOTSET)

        #set a format which is simple for console use

        formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")

        #tell the handler to use this format

        console.setFormatter(formatter)

        #add the handler to the root logger

        logging.getLogger("").addHandler(console)

        # set initial log level
        logger = logging.getLogger("")
        logger.setLevel(logging.NOTSET)
    def QueryDiagPortalEmail(self):
        result = []
        job_url = self.cfg["diag_portal"]["job_url"]
        logging.debug("query email address from %s"%job_url)
        try:
            req = requests.get(job_url)
            status_code = req.status_code
            if status_code != 200:
                raise Exception("can not query email list from diag portal %s"%status_code)
            #print("encoding: ",req.encoding)
            #req.encoding = 'utf-8'
            html = req.text
            soup = BeautifulSoup(req.text, "html.parser")
            tr_list = soup.findAll("tr")
            for tr in tr_list:
                #print(tr)
                td_list = tr.findAll("td")
                if td_list[0].contents[0] == "emails":
                    mail_str = td_list[1].contents[0]
                    return mail_str.split(",")
        except Exception as ex:
            logging.error("get email from diag error: %s"%ex)

        #table = selector.xpath("//tbody")
        #print(table)

        #return result
    def get_file_md5(self, filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        with open(filename,'rb') as fd:
            while True:
                b = fd.read(8096)
                if not b :
                    break
                myhash.update(b)
        return myhash.hexdigest()
    def download_file(self, url, target):
        cmd = "wget " + url  + "  -O " + target
        os.system(cmd)
    def check_and_update_email_library(self):
        lib_url = self.cfg["extra_library"]["lib_url"]
        hash_url = self.cfg["extra_library"]["hash_url"]
        logging.debug("Check library update from ->%s "%self.cfg["extra_library"])
        print("lib url -> ", lib_url)
        print("hash_url-> ", hash_url)
        base_dir = AutoCcl.GetFileDir()
        hash_file = base_dir + "/md5sum.txt"
        try:
            self.download_file(hash_url, base_dir + "/md5sum.txt")
            file_list = []
            with open(hash_file)  as fd:
                file_list = fd.readlines()
                print(file_list)
            for file_info in file_list:
                hash,name = file_info.split()
                print(name)
                print(hash)
                file_target =  base_dir +"/"+  name
                url =  lib_url + name
                self.download_file(url, file_target)
                file_md5 = self.get_file_md5(file_target)
                print("cal md5 ->", file_md5)
                if file_md5 != hash:
                    return False
        except Exception as ex:
            message = "Update library fail -> %s"%(ex)
            logging.debug(message)
            return False
        logging.debug("Update library success ")
        return True



if __name__ == "__main__":
    cmd_args = parser.parse_args()
    #print(cmd_args)
    auto_ccl_inst = None
    if(cmd_args.cfg == None):
        print("please use an config setting ")
        sys.exit()
    else :
        print("use extra config file-> ", cmd_args.cfg)
        cfg_path = None
        if os.path.exists(cmd_args.cfg) :
            cfg_path = cmd_args.cfg
        else:
            real_path = AutoCcl.GetFileDir() + "/" + cmd_args.cfg
            print("real_path ", real_path)
            if os.path.exists(real_path) :
                cfg_path = real_path
            else:
                print("can not find the cfg file")
        if cfg_path == None:
            print("Please a valid cfg file path")
            sys.exit()
        with open(cfg_path) as fd:
            cfg = json.load(fd)
            auto_ccl_inst = AutoCcl(cfg)
    if cmd_args.check_lock:
        if auto_ccl_inst.CheckSingleInstance():
            time.sleep(10)
        sys.exit()
    if cmd_args.test_dir :
        auto_ccl_inst.SetTestDir(cmd_args.test_dir)
    if cmd_args.render_test:
        job_dir = auto_ccl_inst.GetTestDir()
        test_result = auto_ccl_inst.GetRegressionResult(job_dir)
        info = auto_ccl_inst.CollectTestInfo(job_dir)
        test_result["pre_sys_info"] = info
        test_result["post_sys_info"] = info
        #pprint.pprint(test_result)
        body = auto_ccl_inst.EmailBodyRender(cmd_args.render_test, test_result)

        print("reader done")

        if cmd_args.email_report_test:
            attach_list = auto_ccl_inst.GetResultFileList()
            auto_ccl_inst.SendEmail(cmd_args.email_report_test.split(","), body, attach_list)
        sys.exit()
    else:
        if cmd_args.email_report_test:
            auto_ccl_inst.SendEmail(cmd_args.email_report_test.split(","), mail_html_body, [])
            sys.exit()
    if cmd_args.email_send_test:
        auto_ccl_inst.SendTestEmail(cmd_args.email_send_test.split(","))
        sys.exit()
    if cmd_args.query_portal_email:
        email_list = auto_ccl_inst.QueryDiagPortalEmail()
        pprint.pprint(email_list)
        sys.exit()
    if cmd_args.cleanup:
        auto_ccl_inst.CleanUpOldTest()
        sys.exit()

    if cmd_args.check_new_deploy :
        latest_test_dir = auto_ccl_inst.GetLatestDeployDir()
        current_job_test_dir = auto_ccl_inst.GetLastDeployDir()
        print("Latest Deploy  -> ", latest_test_dir)
        print("Last Runing Job-> ", current_job_test_dir)
        sys.exit()
    if cmd_args.update_email_library:
        auto_ccl_inst.check_and_update_email_library()
        sys.exit(0)
    if auto_ccl_inst != None:
        auto_ccl_inst.Run()
    
    sys.exit()
