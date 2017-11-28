import os, patoolib, urllib2, re, yaml

libDir = os.getcwd()

libs = ['__vmm__', '__tex__', '__hdri__', '__alpha__']

for lib in libs:
    libFolder = os.path.join(libDir, 'lib_tk/%s' % lib)

    if not os.path.exists(libFolder):
        os.mkdir(libFolder)

    profile = []
    for root, dirs, file_names in os.walk(libFolder):
        for file_name in file_names:
            pth = os.path.join(root, file_name)
            profile.append(pth)

    # print profile
    yaml_file = os.path.join(os.path.join(libDir, 'sql_tk'), '%s.config.yml' % lib)
    with open(yaml_file, 'w') as f:
        yaml.dump(profile, f, default_flow_style=False)