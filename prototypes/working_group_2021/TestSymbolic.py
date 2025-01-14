# If you want to run the script from this location (where the file lives)
# without installing the package you have to commit a certain institutianalized
# crime by adding the parent directory to the front of the python path.
import sys
import matplotlib.pyplot as plt
import numpy as np
from unittest.case import TestCase, skip
from pathlib import Path
from importlib import import_module
import json 

import general_helpers as gh


class TestSymbolic(TestCase):
    
    @property
    def model_folders(self):
        return ['kv_visit2', 'jon_yib','Aneesh_SDGVM','cable-pop','cj_isam','yz_jules','kv_ft_dlem']

    def test_symobolic_description(self):
        for mf in self.model_folders: 
            with self.subTest(mf=mf):
                mvs = gh.mvs(mf)
                # we assert that some variables are present
                mvs.get_SmoothReservoirModel()
                mvs.get_BibInfo()
    
    #@skip
    def test_download_data(self):
        for mf in self.model_folders:
            with self.subTest(mf=mf):
                conf_dict=gh.confDict(mf)
                msh = gh.msh(mf)
                msh.download_my_TRENDY_output(conf_dict)
    
    def test_get_example_site_vars(self):
        for mf in self.model_folders:
            with self.subTest(mf=mf):
                conf_dict=gh.confDict(mf)
                msh = gh.msh(mf)
                svs, dvs = msh.get_example_site_vars(Path(conf_dict['dataPath']))
                #print(svs)
    

    def test_get_global_mean_vars(self):
        for mf in self.model_folders:
            with self.subTest(mf=mf):
                conf_dict=gh.confDict(mf)
                msh = gh.msh(mf)
                svs, dvs = msh.get_global_mean_vars(Path(conf_dict['dataPath']))
                #print(svs)
    
    @skip
    def test_make_func_dict(self):
        for mf in self.model_folders:
            with self.subTest(mf=mf):
                
                #sys.path.insert(0,mf)
                msh = gh.msh(mf)
                mvs = gh.mvs(mf)
                conf_dict=gh.confDict(mf)
                th= import_module('{}.test_helpers'.format(mf))
                test_args = gh.test_args(mf)
                svs, dvs = msh.get_example_site_vars(Path(conf_dict['dataPath']))
                msh.make_func_dict(mvs,dvs,test_args.epa_0)

    def test_make_iterator_sym(self):
        for mf in self.model_folders:
            with self.subTest(mf=mf):
                
                msh = gh.msh(mf)
                th= import_module('{}.test_helpers'.format(mf))
                mvs = gh.mvs(mf)
                conf_dict=gh.confDict(mf)
                test_args = gh.test_args(mf)
                delta_t_val=30 #n_day iterator
                V_init=test_args.V_init
                it_sym_2 = msh.make_iterator_sym(
                    mvs=test_args.mvs,
                    V_init=V_init,
                    par_dict=test_args.par_dict,
                    func_dict=test_args.func_dict,
                    delta_t_val=delta_t_val
                )
                ns=delta_t_val*3
                times_2= np.arange(0,ns,delta_t_val)
                res_2= np.zeros((len(times_2),len(V_init)))
                res_2[0,:]=V_init
                for i in range(1,len(times_2)-1):
                    res_2[i,:]=it_sym_2.__next__().reshape(len(V_init),)

    def test_param2res_sym(self):
        for mf in self.model_folders:
            with self.subTest(mf=mf):
                mvs = gh.mvs(mf)
                msh = gh.msh(mf)
                th= import_module('{}.test_helpers'.format(mf))
                conf_dict=gh.confDict(mf)
                test_args = gh.test_args(mf)

                cpa = test_args.cpa
                dvs = test_args.dvs
                svs = test_args.svs
                epa_0 = test_args.epa_0
                param2res_sym = msh.make_param2res_sym( mvs, cpa, dvs)
                xs= param2res_sym(epa_0)


    #@skip
    def test_autostep_mcmc_array_cost_func(self):
        # this test is only performed for certain models which have (or have created) monthly data 
        # for all observed variables an can therefore use the simpler general costfunctions in general
        # helpers. 
        # Most other models implement their own costfunctions in model_specific_helpers_2 and are 
        # are tested with different arguments to the mcmc
        for mf in set(self.model_folders).intersection(['cj_isam']):
            #print("############################  {}  ############################".format(mf))
            with self.subTest(mf=mf):
                #sys.path.insert(0,mf)
                mvs = gh.mvs(mf)
                msh = gh.msh(mf)
                th= import_module('{}.test_helpers'.format(mf))
                conf_dict=gh.confDict(mf)
                test_args = gh.test_args(mf)
                cpa = test_args.cpa
                dvs = test_args.dvs
                svs = test_args.svs
                epa_min = test_args.epa_min
                epa_max = test_args.epa_max
                epa_0 = test_args.epa_0

                isQualified = gh.make_param_filter_func(epa_max, epa_min)
                param2res = msh.make_param2res_sym( mvs, cpa, dvs)

                obs=test_args.obs_arr
                #obs=np.column_stack([ np.array(v) for v in svs])
                obs=obs[0:cpa.number_of_months,:] #cut
                # Autostep MCMC: with uniform proposer modifying its step every 100 iterations depending on acceptance rate
                C_autostep, J_autostep = gh.autostep_mcmc(
                    initial_parameters=epa_0,
                    filter_func=isQualified,
                    param2res=param2res,
                    costfunction=gh.make_feng_cost_func(obs),
                    nsimu=20, # for testing and tuning mcmc
                    #nsimu=20000,
                    c_max=np.array(epa_max),
                    c_min=np.array(epa_min),
                    acceptance_rate=15,   # default value | target acceptance rate in %
                    chunk_size=10,  # default value | number of iterations to calculate current acceptance ratio and update step size
                    D_init=1,   # default value | increase value to reduce initial step size
                    K=2 # default value | increase value to reduce acceptance of higher cost functions
                )


    def test_autostep_mcmc_tupel_cost_func(self):
        for mf in set(self.model_folders).intersection(['kv_visit2']):
            with self.subTest(mf=mf):
                #sys.path.insert(0,mf)
                mvs = gh.mvs(mf)
                msh = gh.msh(mf)
                th= import_module('{}.test_helpers'.format(mf))
                conf_dict=gh.confDict(mf)
                test_args = gh.test_args(mf)
                cpa = test_args.cpa
                dvs = test_args.dvs
                svs = test_args.svs
                epa_min = test_args.epa_min
                epa_max = test_args.epa_max
                epa_0 = test_args.epa_0

                isQualified = gh.make_param_filter_func(epa_max, epa_min)
                param2res = msh.make_param2res_sym( mvs, cpa, dvs)
                #obs=np.column_stack([ np.array(v) for v in svs])
                #obs=obs[0:cpa.number_of_months,:] #cut
                # Autostep MCMC: with uniform proposer modifying its step every 100 iterations depending on acceptance rate
                C_autostep, J_autostep = gh.autostep_mcmc(
                    initial_parameters=epa_0,
                    filter_func=isQualified,
                    param2res=param2res,
                    costfunction=msh.make_feng_cost_func_2(svs),
                    nsimu=20, # for testing and tuning mcmc
                    #nsimu=20000,
                    c_max=np.array(epa_max),
                    c_min=np.array(epa_min),
                    acceptance_rate=15,   # default value | target acceptance rate in %
                    chunk_size=10,  # default value | number of iterations to calculate current acceptance ratio and update step size
                    D_init=1,   # default value | increase value to reduce initial step size
                    K=1 # default value | increase value to reduce acceptance of higher cost functions
                )
    
    def test_autostep_mcmc_model_specific_costfunction(self):
        
        for mf in set(self.model_folders).intersection(['Aneesh_SDGVM']):
            with self.subTest(mf=mf):
                #sys.path.insert(0,mf)
                mvs = gh.mvs(mf)
                msh = gh.msh(mf)
                th= import_module('{}.test_helpers'.format(mf))
                conf_dict=gh.confDict(mf)
                test_args = gh.test_args(mf)
                cpa = test_args.cpa
                dvs = test_args.dvs
                svs = test_args.svs
                epa_min = test_args.epa_min
                epa_max = test_args.epa_max
                epa_0 = test_args.epa_0

                isQualified = gh.make_param_filter_func(epa_max, epa_min)
                param2res = msh.make_param2res_sym( mvs, cpa, dvs)
                # Autostep MCMC: with uniform proposer modifying its step every 100 iterations depending on acceptance rate
                C_autostep, J_autostep = gh.autostep_mcmc(
                    initial_parameters=epa_0,
                    filter_func=isQualified,
                    param2res=param2res,
                    costfunction=msh.make_weighted_cost_func(svs),
                    nsimu=20, # for testing and tuning mcmc
                    #nsimu=20000,
                    c_max=np.array(epa_max),
                    c_min=np.array(epa_min),
                    acceptance_rate=15,   # default value | target acceptance rate in %
                    chunk_size=10,  # default value | number of iterations to calculate current acceptance ratio and update step size
                    D_init=1,   # default value | increase value to reduce initial step size
                    K=2 # default value | increase value to reduce acceptance of higher cost functions
                )

    #def test_trace
