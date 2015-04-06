from jsonweb import decode


def policy_factory(policy_repr):
    """
    Params:
        policy_repr - serialized representation of a policy instance
    Returns:
        deserialized policy instance
    """
    instnace = decode.loader(policy_repr)
    return instance
