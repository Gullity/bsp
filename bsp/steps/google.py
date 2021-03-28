from behave import given, then, when

@given(u'the user access the homepage')
def step_impl(context):
    context.me.go(path='/')


@when(u'he seens "{word}"')
def step_impl(context, word):
    title = context.me.get_title()

    assert title == word


@then(u'be happy')
def step_impl(context):
    pass
