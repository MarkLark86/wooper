from wooper.steps.given import *
from wooper.steps.when import *
from wooper.steps.then import *


@when('this step is loaded')
def step_impl_when(context):
    assert True


@then('we assume all went OK')
def step_impl_then(context):
    assert True
