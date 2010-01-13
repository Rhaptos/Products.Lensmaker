"""
LensWorkflow.py - define LensWorkflow.

Author: Hedley Roos (hedley@upfrontsystems.co.za)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.Lensmaker.config import *

##code-section create-workflow-module-header #fill in your manual code here
##/code-section create-workflow-module-header


productname = 'Lensmaker'

def setupLensWorkflow(self, workflow):
    """Define the LensWorkflow workflow.
    """

    workflow.setProperties(title='LensWorkflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['private', 'private_open', 'published', 'published_open']:
        workflow.states.addState(s)

    for t in ['hide', 'expose_private', 'publish', 'expose_published']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    workflow.addManagedPermission('Access contents information')
    workflow.addManagedPermission('View')
    workflow.addManagedPermission('Modify portal content')
    workflow.addManagedPermission('List folder contents')
    workflow.addManagedPermission('Add lens selected content')

    for l in []:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('private')

    ## States initialization

    stateDef = workflow.states['private']
    stateDef.setProperties(title="""Private""",
                           description="""""",
                           transitions=['publish', 'expose_private', 'expose_published'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('List folder contents',
                           0,
                           ['Manager', 'Owner'])

    stateDef = workflow.states['private_open']
    stateDef.setProperties(title="""Open""",
                           description="""""",
                           transitions=['publish', 'hide', 'expose_published'])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('View',
                           1,
                           ['Anonymous', 'Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('List folder contents',
                           1,
                           ['Anonymous'])
    stateDef.setPermission('Add lens selected content',
                           1,
                           ['Manager', 'Owner', 'Member'])

    stateDef = workflow.states['published']
    stateDef.setProperties(title="""Public""",
                           description="""""",
                           transitions=['hide', 'expose_private', 'expose_published'])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('View',
                           1,
                           ['Anonymous', 'Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('List folder contents',
                           1,
                           ['Anonymous'])

    stateDef = workflow.states['published_open']
    stateDef.setProperties(title="""Public Open""",
                           description="""""",
                           transitions=['expose_private', 'publish', 'hide'])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('View',
                           1,
                           ['Anonymous', 'Manager', 'Owner'])
    stateDef.setPermission('List folder contents',
                           1,
                           ['Anonymous'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Add lens selected content',
                           1,
                           ['Manager', 'Owner', 'Member'])

    ## Transitions initialization

    ## Creation of workflow scripts
    for wf_scriptname in ['afterTransition']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.LensWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['hide']
    transitionDef.setProperties(title="""hide""",
                                new_state_id="""private""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""afterTransition""",
                                actbox_name="""hide""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Owner'},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['afterTransition']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.LensWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['expose_private']
    transitionDef.setProperties(title="""expose_private""",
                                new_state_id="""private_open""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""afterTransition""",
                                actbox_name="""expose_private""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Modify portal content', 'guard_roles': 'Manager;Owner'},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['afterTransition']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.LensWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['publish']
    transitionDef.setProperties(title="""publish""",
                                new_state_id="""published""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""afterTransition""",
                                actbox_name="""publish""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Modify portal content', 'guard_roles': 'Manager;Owner'},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['afterTransition']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.LensWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['expose_published']
    transitionDef.setProperties(title="""expose_published""",
                                new_state_id="""published_open""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""afterTransition""",
                                actbox_name="""expose_published""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Modify portal content', 'guard_roles': 'Manager;Owner'},
                                )

    ## State Variable
    workflow.variables.setStateVar('review_state')

    ## Variables initialization
    variableDef = workflow.variables['review_history']
    variableDef.setProperties(description="""Provides access to workflow history""",
                              default_value="""""",
                              default_expr="""state_change/getHistory""",
                              for_catalog=0,
                              for_status=0,
                              update_always=0,
                              props={'guard_permissions': 'Request review; Review portal content'})

    variableDef = workflow.variables['comments']
    variableDef.setProperties(description="""Comments about the last transition""",
                              default_value="""""",
                              default_expr="""python:state_change.kwargs.get('comment', '')""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['time']
    variableDef.setProperties(description="""Time of the last transition""",
                              default_value="""""",
                              default_expr="""state_change/getDateTime""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['actor']
    variableDef.setProperties(description="""The ID of the user who performed the last transition""",
                              default_value="""""",
                              default_expr="""user/getId""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['action']
    variableDef.setProperties(description="""The last transition""",
                              default_value="""""",
                              default_expr="""transition/getId|nothing""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)


    ## Worklists Initialization


    # WARNING: below protected section is deprecated.
    # Add a tagged value 'worklist' with the worklist name to your state(s) instead.

    ##code-section create-workflow-setup-method-footer #fill in your manual code here
    ##/code-section create-workflow-setup-method-footer



def createLensWorkflow(self, id):
    """Create the workflow for Lensmaker.
    """

    ob = DCWorkflowDefinition(id)
    setupLensWorkflow(self, ob)
    return ob

addWorkflowFactory(createLensWorkflow,
                   id='LensWorkflow',
                   title='Lens Workflow')

##code-section create-workflow-module-footer #fill in your manual code here
addWorkflowFactory(createLensWorkflow,
                   id='lens_workflow',
                   title='Lens Workflow')
##/code-section create-workflow-module-footer

