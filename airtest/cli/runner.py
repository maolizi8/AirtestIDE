# -*- coding: utf-8 -*-

import unittest
import os
import sys
import six
import re
import shutil
import traceback
import warnings
from io import open
from airtest.core.api import G, auto_setup, log
from airtest.core.settings import Settings as ST
from airtest.utils.compat import decode_path, script_dir_name, script_log_dir
from copy import copy
import airtest.report.report as report
import jinja2
from argparse import Namespace


class AirtestCase(unittest.TestCase):

    PROJECT_ROOT = "."
    SCRIPTEXT = ".air"
    TPLEXT = ".png"

    @classmethod
    def setUpClass(cls):
        cls.args = args

        setup_by_args(args)

        # setup script exec scope
        cls.scope = copy(globals())
        cls.scope["exec_script"] = cls.exec_other_script

    def setUp(self):
        if self.args.log and self.args.recording:
            for dev in G.DEVICE_LIST:
                try:
                    dev.start_recording()
                except:
                    traceback.print_exc()

    def tearDown(self):
        if self.args.log and self.args.recording:
            for k, dev in enumerate(G.DEVICE_LIST):
                try:
                    output = os.path.join(self.args.log, "recording_%d.mp4" % k)
                    dev.stop_recording(output)
                except:
                    traceback.print_exc()

    def runTest(self):
        scriptpath, pyfilename = script_dir_name(self.args.script)
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        self.scope["__file__"] = pyfilepath
        with open(pyfilepath, 'r', encoding="utf8") as f:
            code = f.read()
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())
        
        print('<gql> runner>runTest>pyfilepath: ',pyfilepath)
        #print('<gql> runner>runTest>code: ',code)
        #print('<gql> runner>runTest>self.scope: ',self.scope)
#         log('<gql> runner>runTest>pyfilepath: ',pyfilepath)
#         log('<gql> runner>runTest>code: ',code)
#         log('<gql> runner>runTest>self.scope: ',self.scope)
        
        try:
            exec(compile(code.encode("utf-8"), pyfilepath, 'exec'), self.scope)
        except Exception as err:
            tb = traceback.format_exc()
            log("Final Error", tb)
            six.reraise(*sys.exc_info())
    
    def runTestPy(self):
        '''运行Py文件用例'''
        #scriptpath, pyfilename = script_dir_name(self.args.script)
        #pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(self.args.script)
        
        self.scope["__file__"] = pyfilepath
        with open(pyfilepath, 'r', encoding="utf8") as f:
            code = f.read()
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())

        try:
            exec(compile(code.encode("utf-8"), pyfilepath, 'exec'), self.scope)
        except Exception as err:
            tb = traceback.format_exc()
            log("Final Error", tb)
            six.reraise(*sys.exc_info())
    
    def runTestPyTest(self):
        '''运行Py文件用例'''
        #scriptpath, pyfilename = script_dir_name(self.args.script)
        #pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(self.args.script)
        
        self.scope["__file__"] = pyfilepath
        with open(pyfilepath, 'r', encoding="utf8") as f:
            code = f.read()
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())

        try:
            exec(compile(code.encode("utf-8"), pyfilepath, 'exec'), self.scope)
        except Exception as err:
            tb = traceback.format_exc()
            log("Final Error", tb)
            six.reraise(*sys.exc_info())
                    
    @classmethod
    def exec_other_script(cls, scriptpath):
        """run other script in test script"""

        warnings.simplefilter("always")
        warnings.warn("please use using() api instead.", PendingDeprecationWarning)

        def _sub_dir_name(scriptname):
            dirname = os.path.splitdrive(os.path.normpath(scriptname))[-1]
            dirname = dirname.strip(os.path.sep).replace(os.path.sep, "_").replace(cls.SCRIPTEXT, "_sub")
            return dirname

        def _copy_script(src, dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst, ignore_errors=True)
            os.mkdir(dst)
            for f in os.listdir(src):
                srcfile = os.path.join(src, f)
                if not (os.path.isfile(srcfile) and f.endswith(cls.TPLEXT)):
                    continue
                dstfile = os.path.join(dst, f)
                shutil.copy(srcfile, dstfile)

        # find script in PROJECT_ROOT
        scriptpath = os.path.join(ST.PROJECT_ROOT, scriptpath)
        # copy submodule's images into sub_dir
        sub_dir = _sub_dir_name(scriptpath)
        sub_dirpath = os.path.join(cls.args.script, sub_dir)
        _copy_script(scriptpath, sub_dirpath)
        # read code
        pyfilename = os.path.basename(scriptpath).replace(cls.SCRIPTEXT, ".py")
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        with open(pyfilepath, 'r', encoding='utf8') as f:
            code = f.read()
        # replace tpl filepath with filepath in sub_dir
        code = re.sub("[\'\"](\w+.png)[\'\"]", "\"%s/\g<1>\"" % sub_dir, code)
        exec(compile(code.encode("utf8"), pyfilepath, 'exec'), cls.scope)


def setup_by_args(args):
    # init devices
    if isinstance(args.device, list):
        devices = args.device
    elif args.device:
        devices = [args.device]
    else:
        devices = []
        print("do not connect device")

    # set base dir to find tpl
    dirpath, _ = script_dir_name(args.script)

    # set log dir
    if args.log:
        args.log = script_log_dir(dirpath, args.log)
        print("save log in '%s'" % args.log)
    else:
        print("do not save log")

    # guess project_root to be basedir of current .air path
    project_root = os.path.dirname(args.script) if not ST.PROJECT_ROOT else None

    auto_setup(dirpath, devices, args.log, project_root)


def run_script(parsed_args, testcase_cls=AirtestCase):
    global args  # make it global deliberately to be used in AirtestCase & test scripts
    args = parsed_args
    print('runner>run_script>args: ',args)
    suite = unittest.TestSuite()
    suite.addTest(testcase_cls())
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if not result.wasSuccessful():
        #sys.exit(-1)
        raise Exception('测试用例失败')

def run_script2(parsed_args, testcase_cls=AirtestCase):
    global args  # make it global deliberately to be used in AirtestCase & test scripts
    args = parsed_args
    print('runner>run_script>args: ',args)
    args.devices=['android:///']
    print('runner>run_script>args: ',args)
    suite = unittest.TestSuite()
    suite.addTest(testcase_cls())
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if not result.wasSuccessful():
        #sys.exit(-1)
        raise Exception('测试用例失败')

def run_air_batch_mode(device, proj_root, tc_folder='', tc_name='',f_type='.air'):
    # 聚合结果
    report_dir = os.sep.join([proj_root, 'reports'])
    case_dir = os.sep.join([proj_root, tc_folder])
    
    results = []
    # 获取所有用例集
    if os.path.isdir(report_dir):
        print('report folder is exist')
        report_subs = os.listdir(report_dir) 
        print('report folder > files: ',report_subs)
        if len(report_subs):
            def is_dir(item):
                item_path=os.sep.join([report_dir,item])
                return os.path.isdir(item_path)
            
            folder_lists=list(filter(is_dir,report_subs))
            print('report folder > folders: ',folder_lists)
            folder_lists.sort(key=lambda fn:os.path.getctime(os.sep.join([report_dir,fn])))
            # getmtime ? getctime
            final_num=folder_lists[-1]
            report_num=int(final_num)+1
        else:
            report_num=0
    else:
        os.makedirs(report_dir)
        print('report folder is created')
        report_num=0
        
    report_dir_num = os.sep.join([proj_root,'reports',str(report_num)])
    print('report_dir_num: ',report_dir_num)
    os.makedirs(report_dir_num)
    
    
    for f in os.listdir(case_dir):
        print('case_dir > f:',f)
        #if f.endswith(".air"):
        if f.endswith(f_type):    
            # f为.air案例名称
            print('   (.air)test file:',f)
            airName = f
            script = os.path.join(case_dir, f)
            # airName_path为.air的全路径：BASE_DIR\案例集\testcase.air
            print('   script:',script)
            # 日志存放路径和名称：BASE_DIR\reports\案例集\testcase\
            tc_report_dir = os.path.join(report_dir_num, airName.replace('.air', ''))
            print('tc_report_dir：',tc_report_dir)
            if os.path.isdir(tc_report_dir):
                print('tc_report_dir exist ')
            else:
                os.makedirs(tc_report_dir)
                print('tc_report_dir is created')
            
            log_file=os.path.join(tc_report_dir, 'log.txt')
            
            if not os.path.exists(log_file):
                log_content = open(log_file,'w')
                print('create log file: ',log_content)
                log_content.close()
            else:
                print(log_file + " already existed.")
            output_file = os.path.join(tc_report_dir, 'log.html')
            args = Namespace(device=device, log=tc_report_dir, recording=None, script=script)
            try:
                print('运行脚本开始')
                
                #start_app("com.yiwang.fangkuaiyi")
            
                run_script(args, AirtestCase)
                
                print('运行脚本结束')
            except Exception as e:
                print('运行失败，',e)
            finally:
                #stop_app("com.yiwang.fangkuaiyi")
                
                try:
                    print('生成报告')
                    rpt = report.LogToHtml(script_root=case_dir, log_root=tc_report_dir, script_name=script)
                    print('output_file:',output_file)
                    rpt.report("log_template.html", output_file=output_file)
                    result = {}
                    result["name"] = airName.replace('.air', '')
                    result["result"] = rpt.test_result
                    results.append(result)
                except Exception as e:
                    print('运行失败，暂时不抛异常，',e)
                
    
    print('生成聚合报告')
    # 生成聚合报告
    static_dir=os.sep.join([proj_root,'statics'])
    print('static_dir: ',static_dir)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(static_dir),
        extensions=(),
        autoescape=True
    )
    template = env.get_template("summary_template.html", static_dir)
    print('template: ',template)
    html = template.render({"results": results,"report_num":report_num})
    summary_file = os.path.join(report_dir_num, "summary.html")
    with open(summary_file, 'w', encoding="utf-8") as f:
        f.write(html)
    print('summary_file:',summary_file)