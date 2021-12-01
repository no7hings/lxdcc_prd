# coding:utf-8
from lxutil_prd import utl_prd_configure, utl_prd_core, utl_prd_objects, utl_prd_commands


assetsOpt = utl_prd_objects.AssetsOpt(project='cg7')
for i in ['/l/prod/cg7/publish/assets/env/temple_ground/srf']:
    assetsOpt.set_load_by_plf_path(i)

for i in assetsOpt.get_entity_opts():
    print i.get_vsn_all('prx_ass', stp_brh='surface', stg_brh='prd')
    print i.get_stp_plf_path(stp_brh='surface')

