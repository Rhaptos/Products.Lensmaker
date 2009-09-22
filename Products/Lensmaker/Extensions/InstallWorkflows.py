"""
InstallWorkflows.py - install LensWorkflow.

Author: Hedley Roos (hedley@upfrontsystems.co.za)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod

##code-section module-header #fill in your manual code here
##/code-section module-header

def installWorkflows(self, package, out):
    """Install the custom workflows for this product."""

    productname = 'Lensmaker'
    workflowTool = getToolByName(self, 'portal_workflow')

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                                        productname+'.'+'LensWorkflow',
                                        'createLensWorkflow')

    workflow = ourProductWorkflow(self, 'LensWorkflow')
    if 'LensWorkflow' in workflowTool.listWorkflows():
        print >> out, 'LensWorkflow already in workflows.'
    else:
        workflowTool._setObject('LensWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['ContentSelectionLens'], workflow.getId())

    ##code-section after-workflow-install #fill in your manual code here
    ##/code-section after-workflow-install

    return workflowTool

def uninstallWorkflows(self, package, out):
    """Deinstall the workflows.

    This code doesn't really do anything, but you can place custom
    code here in the protected section.
    """

    ##code-section workflow-uninstall #fill in your manual code here
    ##/code-section workflow-uninstall

    pass
