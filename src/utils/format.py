def format_system_name_and_id(sys_vimm_id: str, sys_name: str):
    if sys_name.replace(' ', '').lower() == sys_vimm_id.lower():
        return sys_name
    return f'{sys_name} ({sys_vimm_id})'
