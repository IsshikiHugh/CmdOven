import sys

def ding() -> None:
    ''' CLI command `ding`. '''
    import oven
    log = ' '.join(sys.argv[1:])
    return oven.notify(log)


def bake() -> None:
    ''' CLI command `bake`. '''
    import oven
    cmd = ' '.join(sys.argv[1:])
    return oven.get_lazy_oven().ding_cmd(cmd)


def oven() -> None:
    ''' CLI command `oven`. '''
    action = sys.argv[1]
    args = sys.argv[2:]

    if action == 'help':
        from oven.utils import print_manual
        return print_manual()
    elif action == 'ding':
        import oven
        return oven.notify(' '.join(args))
    elif action == 'bake':
        import oven
        return oven.get_lazy_oven().ding_cmd(' '.join(args))
    elif action == 'init-cfg':
        from oven.utils import dump_cfg_temp
        return dump_cfg_temp(overwrite=False)
    elif action == 'reset-cfg':
        from oven.utils import dump_cfg_temp
        return dump_cfg_temp(overwrite=True)
    elif action == 'home':
        from oven.utils import get_home_path
        return print(get_home_path())
    else:
        from oven.utils import error_redirect_to_manual
        return error_redirect_to_manual(action)