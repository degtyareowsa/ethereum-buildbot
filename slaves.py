#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ###### BUILDSLAVES

# The 'slaves' list defines the set of recognized buildslaves. Each element is
# a BuildSlave object, specifying a unique slave name and password.  The same
# slave name and password must be configured on the slave.
from buildbot.buildslave import BuildSlave
from buildbot.buildslave.ec2 import EC2LatentBuildSlave

# using simplejson instead of json since Twisted wants ascii instead of unicode
import simplejson as json

slaves = []

# Load slaves from external file, see slaves.json.sample
for slave in json.load(open("slaves.json")):
    if 'latentslave' in slave['name']:
        slaves.append(EC2LatentBuildSlave(
            slave['name'],
            slave['password'],
            'c4.large',
            max_builds=1,
            ami='ami-ec6c7186',
            region='us-east-1',
            placement='e',
            user_data='{"SLAVENAME": "%s"}' % slave['name'],
            spot_instance=True,
            max_spot_price=0.05,
            price_multiplier=1.15))
    else:
        slaves.append(BuildSlave(slave['name'], slave['password']))
