#-*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import zipfile,os

_filter_dir=("sample","ngui_test","wpyscripts\\test",".idea","doc","bin",".svn",".git","screenshot")
filter_file=("wpyscripts_upload.zip","python_log.log")
filter_dir=[]

def filter_create():
    global filter_dir
    current_path=os.path.abspath(os.getcwd())
    for name in _filter_dir:
        filter_dir.append(os.path.abspath(os.path.join(current_path,name)))


def walk_dir(dirname,filelist):
    for lists in os.listdir(dirname):
        path=os.path.join(dirname,lists)
        dir,filename=os.path.split(path)
        if os.path.isdir(path):
            if path not in filter_dir:
                walk_dir(path,filelist)
        elif filename not in filter_file:
            name,extented=os.path.splitext(filename)
            if extented != ".pyc":
                filelist.append(path)
def zip_files(filelists,zf,pre_dir):
    for tar in filelists:
        arcname = tar[len(pre_dir):]
        #arcname="\\scripts{0}".format(arcname)
        # arcname=os.path.join("\\scripts",arcname)
        zf.write(tar,arcname)

def zip_dir(dirname,zf):
    pre_dir,curr_dir=os.path.split(dirname)
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            if root in filter_dir:
                continue
            for name in files:
                if name not in filter_file:
                    filelist.append(os.path.join(root, name))

    zf.write(filelist[0],"scripts")

    for tar in filelist[1]:
        arcname = tar[len(pre_dir):]
        zf.write(tar,arcname)
    #zf.close()

def addzip(file,zip):
    pre_dir,file_name=os.path.split(file)
    zf.write(file,file_name)

def create_tag_file():
    current_path=os.path.abspath(os.getcwd())
    print("Current path : {0}".format(current_path))
    # wpy_txt=os.path.abspath(os.path.join(current_path,"..\\wetest_temp_script.txt"))
    # f=open(wpy_txt,"wb")
    # f.close()

    wpy_zip=os.path.abspath(os.path.join(current_path,"wpyscripts.zip"))
    try:
        os.remove(wpy_zip)
    except:
        pass

def delete_tag_file():
    current_path=os.path.abspath(os.getcwd())
    print("Current path : {0}".format(current_path))
    wpy_txt=os.path.abspath(os.path.join(current_path,"..","wetest_temp_script.txt"))
    try:
        os.remove(wpy_txt)
    except:
        pass

if __name__ == "__main__":
    filter_create()
    create_tag_file()
    current_path=os.path.abspath(os.getcwd())
    zip_file=os.path.abspath(os.path.join(current_path,"wpyscripts_upload.zip"))
    zf = zipfile.ZipFile(zip_file, "w", zipfile.zlib.DEFLATED)
    filelists=[]
    walk_dir(current_path,filelists)
    zip_files(filelists,zf,current_path)

    #addzip(os.path.abspath(os.path.join(current_path,"..\\wetest_temp_script.txt")),zf)

    zf.close()
    #delete_tag_file()