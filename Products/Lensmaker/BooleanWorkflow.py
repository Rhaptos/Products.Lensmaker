from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFPlone.FolderWorkflow import createFolderWorkflow as baseCreateWorkflow
from Products.CMFCore.permissions import View

def setupBooleanWorkflow(wf):
    wf.transitions.deleteTransitions(['retract', 'show'])
    
    wf.states.deleteStates(['visible'])
    wf.states.setInitialState(id='private')
    # we might want to strip the unused transitions off the state, but I don't think it hurts anything
    
    # make sure Owner is represented, so we get owners in allowedRolesAndUsers
    wf.states.published.setPermission(View, 1, ('Anonymous','Manager','Owner'))

def createBooleanWorkflow(id):
    wf = baseCreateWorkflow(id)
    setupBooleanWorkflow(wf)
    wf.setProperties(title='Boolean Workflow, DCWorkflow based')
    return wf

addWorkflowFactory(createBooleanWorkflow, id='boolean_workflow',
                   title='Boolean Workflow, DCWorkflow based')
