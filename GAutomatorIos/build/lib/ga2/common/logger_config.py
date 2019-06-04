import logging,os
import six
if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

LOG_FILE = 'wetest.log'


def makesure_dir_exist(path):
    existed=os.path.exists(path)
    if existed:
        return True
    else:
        os.mkdir(path)

handler = logging.StreamHandler()
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# use_ai=False

#mode=os.environ.get("RUNNER_MODE")

# log_dir=os.environ.get("UPLOADDIR")
# #file_path = os.path.split(os.path.realpath(__file__))[0]
# file_path = os.getcwd()
# if log_dir:
#     file_path=os.path.abspath(os.path.join(log_dir,"ga_log.log"))
# else:
#     log_name="ga_log_{0}.log".format(os.environ.get("ADB_SERIAL",os.environ.get("IOS_SERIAL","")))
#     file_path=os.path.abspath(os.path.join(file_path,"..","..",log_name))
# file_handler=logging.FileHandler(file_path)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
#


# def get_ga_logger():
#     if not get_ga_logger.instance:
#         get_ga_logger.instance=logging.getLogger("gautomator")
#     return get_ga_logger.instance
#
#
# get_ga_logger.instance=None