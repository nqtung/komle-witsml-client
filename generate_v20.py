"""Generate python bindings

Generate bindings from xml schema files using pyxb and download WSDL file for the given version.
This is a one time run to get the python bindings, but the energistics server can timeout, just try again if that happens.

Also see, http://w3.energistics.org/energyml/data/witsml/v2.0/doc/witsml_schema_overview.html and
http://w3.energistics.org/energyml/data/witsml/v2.0/xsd_schemas/Attachment.xsd for the schema.
"""

import os
import subprocess


version = 'v2.0'
host = f'https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_{version}_Data_Schema/energyml/data/witsml/{version}/xsd_schemas/'
root = 'komle_witslm_client'
package_name = 'bindings/v20'
module_name = 'witsml'

obj_files = [
    'Attachment.xsd',
    'BhaRun.xsd',
    'CementJob.xsd',
    'DepthRegImage.xsd',
    'DownholeComponent.xsd',
    'DrillReport.xsd',
    'FluidsReport.xsd',
    'Log.xsd',
    'MudLogReport.xsd',
    'OpsReport.xsd',
    'Rig.xsd',
    'Risk.xsd',
    'StimJob.xsd',
    'SurveyProgram.xsd',
    'ToolErrorModel.xsd',
    'ToolErrorTermSet.xsd',
    'Trajectory.xsd',
    'Tubular.xsd',
    'Well.xsd',
    'Wellbore.xsd',
    'WellboreCompletion.xsd',
    'WellboreGeology.xsd',
    'WellboreGeometry.xsd',
    'WellboreMarkers.xsd',
    'WellCMLedger.xsd',
    'WellCompletion.xsd',
    'WitsmlAllObjects.xsd',
    'WitsmlCommon.xsd',
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
