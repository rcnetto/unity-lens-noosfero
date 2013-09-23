#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
    from DistUtilsExtra.command import build_extra
except ImportError:
    print >> sys.stderr, 'To build unity-lens-noosfero you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_config(values = {}):

    oldvalues = {}
    try:
        fin = file('unity_lens_noosfero/unity_lens_noosferoconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find unity_lens_noosfero/unity_lens_noosferoconfig.py")
        sys.exit(1)
    return oldvalues


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__unity_lens_noosfero_data_directory__': "'%s'" % (self.prefix + '/share/unity-lens-noosfero/'),
                  '__version__': "'%s'" % (self.distribution.get_version())}
        previous_values = update_config(values)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='unity-lens-noosfero',
    version='1.0b',
    license='Apache License, v2',
    author='Ranulfo Netto',
    author_email='rcnetto@yahoo.com',
    description='Provide a unity lens to search Noosfero sites',
    long_description='Provide a unity lens to search Noosfero sites',
    url='https://github.com/rcnetto/unity-lens-noosfero',
    data_files=[
        ('share/unity/lenses/noosfero', ['noosfero.lens']),
        ('share/dbus-1/services', ['unity-lens-noosfero.service']),
        ('share/unity/lenses/noosfero', ['unity-lens-noosfero.svg']),
        ('bin', ['bin/unity-lens-noosfero']),
    ],
    cmdclass={"build":  build_extra.build_extra, 'install': InstallAndUpdateDataDirectory}
    )

