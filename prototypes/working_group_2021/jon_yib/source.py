from sympy import Symbol, Function 
from ComputabilityGraphs.CMTVS import CMTVS
from bgc_md2.helper import module_computers
from bgc_md2.models.BibInfo import BibInfo
from bgc_md2.resolve.mvars import (
    InFluxesBySymbol,
    OutFluxesBySymbol,
    InternalFluxesBySymbol,
    TimeSymbol,
    StateVariableTuple,
)
import bgc_md2.resolve.computers as bgc_c

# Make a dictionary for the variables we will use
sym_dict={
    'c_leaf': '',
    'c_root': '',
    'c_wood': '',
    'c_lit_cwd': '',
    'c_lit_met': '',
    'c_lit_str': '',
    'c_lit_mic': '',
    'c_soil_met': '',
    'c_soil_str': '',
    'c_soil_mic': '',
    'c_soil_slow': '',
    'c_soil_passive': '',
    'r_c_lit_cwd_rh': '',
    'r_c_lit_met_rh': '',
    'r_c_lit_str_rh': '',
    'r_c_lit_mic_rh': '',
    'r_c_soil_met_rh': '',
    'r_c_soil_str_rh': '',
    'r_c_soil_mic_rh': '',
    'r_c_soil_slow_rh': '',
    'r_c_soil_passive_rh': '',
    'r_c_leaf_2_c_lit_met': '',
    'r_c_leaf_2_c_lit_str': '',
    'r_c_root_2_c_soil_met': '',    
    'r_c_root_2_c_soil_str': '',
    'r_c_wood_2_c_lit_cwd': '',
    'r_c_lit_cwd_2_c_lit_mic': '',
    'r_c_lit_cwd_2_c_soil_slow': '',
    'r_c_lit_met_2_c_lit_mic': '',
    'r_c_lit_str_2_c_lit_mic': '',
    'r_c_lit_str_2_c_soil_slow': '',
    'r_c_lit_mic_2_c_soil_slow': '',
    'r_c_soil_met_2_c_soil_mic': '',
    'r_c_soil_str_2_c_soil_mic': '',
    'r_c_soil_str_2_c_soil_slow': '',
    'r_c_soil_mic_2_c_soil_slow': '',
    'r_c_soil_mic_2_c_soil_passive': '',
    'r_c_soil_slow_2_c_soil_mic': '',
    'r_c_soil_slow_2_c_soil_passive': '',
    'r_c_soil_passive_2_c_soil_mic': '',
    't': '',
    'silt': '',
    'clay': '',
    'beta_leaf': '',
    'beta_root': '',
}
for k in sym_dict.keys():
    code=k+" = Symbol('{0}')".format(k)
    exec(code)

# some we will also use some symbols for functions (which appear with an argument) 
func_dict={
    'xi': 'a scalar function of temperature and moisture and thereby ultimately of time',
    'NPP': '',
}
for k in func_dict.keys():
    code=k+" = Function('{0}')".format(k)
    exec(code)

t=TimeSymbol("t")
beta_wood = 1.0-(beta_leaf+beta_root)
mvs = CMTVS(
    {
        t,
        StateVariableTuple(( 
            c_leaf,
            c_root,
            c_wood,
            c_lit_cwd,
            c_lit_met,
            c_lit_str,
            c_lit_mic,
            c_soil_met,
            c_soil_str,
            c_soil_mic,
            c_soil_slow,
            c_soil_passive,
        )),
        InFluxesBySymbol(
            {
                c_leaf: NPP(t) * beta_leaf, 
                c_root: NPP(t) * beta_root, 
                c_wood: NPP(t) * beta_wood
            }
        ),
        OutFluxesBySymbol(
            {
                c_lit_cwd: r_c_lit_cwd_rh*c_lit_cwd*xi(t),
                c_lit_met: r_c_lit_met_rh*c_lit_met*xi(t),
                c_lit_str: r_c_lit_str_rh*c_lit_str*xi(t),
                c_lit_mic: r_c_lit_mic_rh*c_lit_mic*xi(t),
                c_soil_met: r_c_soil_met_rh*c_soil_met*xi(t),
                c_soil_str: r_c_soil_str_rh*c_soil_str*xi(t),
                c_soil_mic: r_c_soil_mic_rh*c_soil_mic*xi(t),
                c_soil_slow: r_c_soil_slow_rh*c_soil_slow*xi(t),
                c_soil_passive: r_c_soil_passive_rh*c_soil_passive*xi(t),
            }
        ),
        InternalFluxesBySymbol(
            {
                (c_leaf, c_lit_met): r_c_leaf_2_c_lit_met*c_leaf,
                (c_leaf, c_lit_str): r_c_leaf_2_c_lit_str*c_leaf,
                (c_root, c_soil_met): r_c_root_2_c_soil_met*c_root,
                (c_root, c_soil_str): r_c_root_2_c_soil_str*c_root,
                (c_wood, c_lit_cwd): r_c_wood_2_c_lit_cwd*c_wood,
                (c_lit_cwd, c_lit_mic): r_c_lit_cwd_2_c_lit_mic*c_lit_cwd*xi(t),
                (c_lit_cwd, c_soil_slow): r_c_lit_cwd_2_c_soil_slow*c_lit_cwd*xi(t),
                (c_lit_met, c_lit_mic): r_c_lit_met_2_c_lit_mic*c_lit_met*xi(t),
                (c_lit_str, c_lit_mic): r_c_lit_str_2_c_lit_mic*c_lit_str*xi(t),
                (c_lit_str, c_soil_slow): r_c_lit_str_2_c_soil_slow*c_lit_str*xi(t),
                (c_lit_mic, c_soil_slow): r_c_lit_mic_2_c_soil_slow*c_lit_mic*xi(t),
                (c_soil_met, c_soil_mic): r_c_soil_met_2_c_soil_mic*c_soil_met*xi(t),
                (c_soil_str, c_soil_mic): r_c_soil_str_2_c_soil_mic*c_soil_str*xi(t),
                (c_soil_str, c_soil_slow): r_c_soil_str_2_c_soil_slow*c_soil_str*xi(t),
                (c_soil_mic, c_soil_slow): r_c_soil_mic_2_c_soil_slow*c_soil_mic*xi(t),
                (c_soil_mic, c_soil_passive): r_c_soil_mic_2_c_soil_passive*c_soil_mic*xi(t),
                (c_soil_slow, c_soil_mic): r_c_soil_slow_2_c_soil_mic*c_soil_slow*xi(t),
                (c_soil_slow, c_soil_passive): r_c_soil_slow_2_c_soil_passive*c_soil_slow*xi(t),
                (c_soil_passive, c_soil_mic): r_c_soil_passive_2_c_soil_mic*c_soil_passive*xi(t),               
            }
        ),
        BibInfo(# Bibliographical Information
            name="YIBS",
            longName="",
            version="1",
            entryAuthor="Jon Wells",
            entryAuthorOrcid="",
            entryCreationDate="",
            doi="",
            sym_dict=sym_dict,
            func_dict=func_dict
        ),
    },
    computers=module_computers(bgc_c)
)