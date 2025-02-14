"""Generate python bindings

Generate bindings from xml schema files using pyxb and download WSDL file for the given version.
This is a one time run to get the python bindings, but the energistics server can timeout, just try again if that happens.

Also see, http://w3.energistics.org/schema/witsml_v1.3.1_api/doc/WITSML_API_docu.htm and
http://w3.energistics.org/schema/witsml_v1.3.1_api/doc/schema/obj_capClient.sxd for the schema.
"""

import os
import subprocess


version = 'v1.3.1'
host = f'https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_{version}_API_schema/'
root = 'komle_witslm_client'
package_name = f'bindings/v1311/api'
module_name = 'witsml'

obj_files = [
    'obj_capClient.xsd',
    'obj_capPublisher.xsd',
    'obj_capServer.xsd',
    'obj_capSubscriber.xsd',
    'obj_subscription.xsd',
]

cmd = ['pyxbgen']
for obj_file in obj_files:
    obj_path = os.path.join(host, obj_file)
    print(f'--schema-location {obj_path} --module {module_name}')
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

