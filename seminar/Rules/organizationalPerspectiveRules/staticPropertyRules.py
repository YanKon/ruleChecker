# An activity of type a1must be performed by a member of role r1
def role_based_activity_authorization_rule():
    return

# An activity of type a1must not be performed by a member of role r1
def prohibited_role_based_allocation_rule():
    return

# It is not optimal that a member of role r1 performs an activity of type a1
def not_optimal_allocation_rule():
    return

# An activity of type a1must be performed by a person who has characteristic C
def required_originator_attribute_rule():
    return

# A person must not become a member of both role r1and role r2
def prohibited_role_acquisition_rule():
    return

# A person must be a member of role r1in order to delegate role r1
def delegation_authorization_rule():
    return

# Person o1 with role r1 cannot be retracted from role r1when the set sPof persons with role r1 only contains person o1
def retract_restriction_rule():
    return