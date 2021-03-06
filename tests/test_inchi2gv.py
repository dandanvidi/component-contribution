import sys
sys.path.append('../python')
import inchi2gv
from compound_cacher import CompoundCacher
from molecule import Molecule

#logger = logging.getLogger('')
#logger.setLevel(logging.DEBUG)
ccache = CompoundCacher('../cache/compounds.json')
groups_data = inchi2gv.init_groups_data()
group_list = groups_data.GetGroupNames()
group_names = groups_data.GetGroupNames()
decomposer = inchi2gv.InChIDecomposer(groups_data)

# test the decomposition of ATP into groups
ATP_inchi = ccache.get_compound('C00002').inchi
group_def = decomposer.inchi_to_groupvec(ATP_inchi)
for j, group_name in enumerate(group_names):
    if group_def[j] != 0:
        print group_name, ' x %d' % group_def[j]


patterns = ['c~[O;+0]', 'c~[O;+1]', 'c~[n;+1]~c', 'c~[n;+0]~c', 'c~[n;-1]~c']

for cid in ['C00255', 'C01007']:
    comp = ccache.get_compound(cid)
    print "-"*50, '\n%s' % cid
    inchi = comp.inchi
    mol = Molecule.FromInChI(inchi)
    print mol.ToSmiles()
    
    print mol.FindSmarts("c~[n;+1]~c")
    
    try:
        groupvec = decomposer.inchi_to_groupvec(inchi)
        sys.stdout.write(str(groupvec) + '\n')
    except inchi2gv.GroupDecompositionError as e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.write(e.GetDebugTable())
    