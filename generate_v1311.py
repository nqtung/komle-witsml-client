"""Generate python bindings

Generate bindings from xml schema files using pyxb and download WSDL file for the given version.
This is a one time run to get the python bindings, but the energistics server can timeout, just try again if that happens.

Also see, http://w3.energistics.org/schema/witsml_v1.3.1.1_data/doc/WITSML_Schema_docu.htm#_Data_object_schema and
http://w3.energistics.org/schema/witsml_v1.3.1.1_data/doc/schema/obj_well.xsd for the schema.
"""

import os
import subprocess


version = 'v1.3.1.1'
host = f'https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_{version}_Data_Schema'
root = 'komle_plus'
package_name = f'bindings/v1311'
module_name = 'witsml'

obj_files = [
    'obj_bhaRun.xsd',
    'obj_cementJob.xsd',
    'obj_convCore.xsd',
    'obj_dtsInstalledSystem.xsd',
    'obj_dtsMeasurement.xsd',
    'obj_fluidsReport.xsd',
    'obj_formationMarker.xsd',
    'obj_log.xsd',
    'obj_message.xsd',
    'obj_mudLog.xsd',
    'obj_opsReport.xsd',
    'obj_realtime.xsd',
    'obj_rig.xsd',
    'obj_risk.xsd',
    'obj_sidewallCore.xsd',
    'obj_surveyProgram.xsd',
    'obj_target.xsd',
    'obj_trajectory.xsd',
    'obj_trajectoryStation.xsd',
    'obj_tubular.xsd',
    'obj_wbGeometry.xsd',
    'obj_well.xsd',
    'obj_wellbore.xsd',
    'obj_wellLog.xsd',
]


cmd = ['pyxbgen']
for obj_file in obj_files:
    obj_path = os.path.join(host, obj_file)
    cmd.extend(['--schema-location', obj_path, '--module', module_name])

cmd.extend(['--module-prefix', package_name])
cmd.extend(['--binding-root', root])
res = subprocess.run(cmd)

print('Generated:')
print(f'Module {module_name} from')
print(f'{obj_path} ++')

wits_path = os.path.join(root, package_name, module_name) + '.py'

with open(wits_path, "r") as no_version_file:
    data = no_version_file.read()


with open(wits_path, "w") as with_version_file:
    with_version_file.write(data + f'__version__ = "{version[1:]}"\n')

py_path = os.path.join(root, package_name)
for f in os.listdir(py_path):
    if f.endswith('.py'):
        f_path = os.path.join(py_path, f)
        with open(f_path, 'r') as py_file:
            code = py_file.read()

        code = code.replace(f"import {package_name}.", f"import {root}.{package_name}.")
        code = code.replace(f"from {package_name}.", f"from {root}.{package_name}.")

        with open(f_path, 'w') as fixed_py_file:
            fixed_py_file.write(code)

