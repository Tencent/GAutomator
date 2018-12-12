from setuptools import setup,find_packages
import os

def get_build_env_var_by_name(flag_name):
    
    flag_set = False
    try:
        flag_set = bool(int(os.getenv('ENABLE_' + flag_name.upper() , None)))
    except Exception:
        pass
    
    if not flag_set:
        try:
            flag_set = bool(int(open(flag_name + ".enabled").read(1)))
        except Exception:
            pass

    return flag_set


def main():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    requires = [
                    'requests',
                    'enum34',
                    'urllib3',
                    'opencv-python',
                    'six',
               ],

    build_contrib = get_build_env_var_by_name("contrib")
    PACKAGES = ["ga2"] + ["%s.%s" % ("ga2", i) for i in find_packages("ga2")]
    if build_contrib:
        print("ga2_contrib will be included...")
        PACKAGES_CONTRIB = ["ga2_contrib"] + ["%s.%s" % ("ga2_contrib", i) for i in find_packages("ga2_contrib")]
        PACKAGES+=PACKAGES_CONTRIB
    print(PACKAGES)

    setup(
        name='GAutomator2',
        version='0.0.1',
        description='Python Automation Test Framework for Android/iOS  Games/Apps',
        long_description=long_description,
        keywords=[
            'gautomator2',
            'gautomator 2.0',
            'automation test',
            'mobile automation'
        ],
        author='xavierhan',
        author_email='xavierhan@tencent.com',
        url='http://git.code.oa.com/gautomator2',
    #    packages=[
    #        'ga2',
    #        'ga2.common'
    #    ],
        packages=PACKAGES,
       

        license='Apache 2.0',

        install_requires=requires,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
         ],
        python_requires = ">2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    )



if __name__ == '__main__':
    main()
