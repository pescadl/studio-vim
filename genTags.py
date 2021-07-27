import os
import subprocess
import xml.etree.ElementTree as ET

tree = ET.parse('.cproject');
root = tree.getroot()

cwd = os.getcwd()
sdk_path = os.environ.get('STUDIO_GSDK')

include_paths = []
defines = []

# parse for the project's include paths
for tag in root.findall('./storageModule/cconfiguration[@id="debug"]/storageModule/configuration/folderInfo/toolChain/tool/option[@superClass="gnu.c.compiler.option.include.paths"]/listOptionValue'):
    path = tag.attrib['value'].strip('\"').replace('${StudioSdkPath}/', sdk_path)
    include_paths.append(path)

# parse for the project's defines
for tag in root.findall('./storageModule/cconfiguration[@id="debug"]/storageModule/configuration/folderInfo/toolChain/tool/option[@superClass="com.silabs.ide.si32.gcc.cdt.managedbuild.tool.gnu.c.compiler.def.symbols"]/listOptionValue'):
    defines.append(tag.attrib['value'])

# create gtags and ctags
for path in include_paths:
    # generate gtags and ctags paths
    gtags_path = '/home/dayoung/.cache/tags/' + path.strip('/').replace('/', '-')
    ctags_path = gtags_path + '-tags'

    # create gtags folder if it doesn't exist
    if not os.path.exists(gtags_path):
        os.makedirs(gtags_path)

    # run gtags
    os.chdir(path)

    cmd = 'gtags ' + gtags_path
    subprocess.run(cmd.split())

    # run ctags
    cmd = 'ctags -f ' + ctags_path + ' -R ' + path
    subprocess.run(cmd.split())

# move current working directory back to initial directory
os.chdir(cwd)
