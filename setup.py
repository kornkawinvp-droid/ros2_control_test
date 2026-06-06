from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ros2_control_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),
         glob('launch/*.launch.py')),
        (os.path.join('share',package_name,'urdf'),
         glob('urdf/*.xacro')),
        (os.path.join('share',package_name,'meshes'),
         glob('meshes/*.STL')),
        (os.path.join('share',package_name,'rviz'),
         glob('rviz/*.rviz')),
        (os.path.join('share',package_name,'config'),
         glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vespa',
    maintainer_email='kornkawin.vp@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cmd_vel_yflip = ros2_control_test.teleop_convert_y_axis_node:main',
            'yaw_control = ros2_control_test.yaw_control:main',
        ],
    },
)
