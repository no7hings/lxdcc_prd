# coding:utf-8
if __name__ == '__main__':
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    p = '/l/prod/cg7/publish/shots/d10/d10010/efx/efx_crowd/d10010.efx.efx_crowd.v001/crowd/abc'

    d = utl_dcc_objects.OsDirectory_(p)

    cs = d.get_child_file_paths()

    for i in cs:
        f = utl_dcc_objects.OsFile(i)
        print f
        name = f.name
        asset_name = '_'.join(name.split('_')[2:-1])
        extra = name.split('_')[-1]
        new_name = '{}__{}'.format(asset_name, extra)
        f.set_rename(new_name)
