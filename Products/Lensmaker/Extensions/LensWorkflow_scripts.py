"""
LensWorkflow_scripts.py - scripts for use in LensWorkflow.

Author: Hedley Roos (hedley@upfrontsystems.co.za)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

# Workflow Scripts for: LensWorkflow

##code-section workflow-script-header #fill in your manual code here
from zope.event import notify
from Products.Lensmaker.events import AfterTransitionEvent
##/code-section workflow-script-header


def afterTransition(self, state_change, **kw):
    # Publish an event
    notify(AfterTransitionEvent(state_change.object))
