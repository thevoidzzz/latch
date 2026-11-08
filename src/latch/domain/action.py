"""An unapproved action is a commit that ran. A blocked attempt is not one."""


def unapproved_commit(committed: bool, approved: bool) -> int:
    if committed and not approved:
        return 1
    return 0
