import site
print(site.getsitepackages())

# import partio

# ./python -m pip install /home/chenhui/Dev/partio/ 
# ~/anaconda3/envs/asflip/bin


import sysconfig
print(sysconfig.get_config_var('LIBDIR'))