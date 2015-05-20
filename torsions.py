#   This is baRNAba, a tool for analysis of nucleic acid 3d structure
#   Copyright (C) 2014 Sandro Bottaro (sbottaro@sissa.it)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License V3 as published by
#   the Free Software Foundation, 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import reader as reader
import numpy as np

def torsions(args):


    print "# Calculating torsion angles..."
    files = args.files
    fh = open(args.name,'w')
    fh.write("# This is a baRNAba run.\n")
    for k in args.__dict__:
        s = "# " + str(k) + " " + str(args.__dict__[k]) + "\n"
        fh.write(s)

    for i in xrange(0,len(files)):
        cur_pdb = reader.Pdb(files[i],base_only=False)
        for j in xrange(len(cur_pdb.models)):

            
            # calculate interactions
            bb_torsion = cur_pdb.models[j].get_bb_torsions()
            if(args.hread):
                string = '# ' + files[i] + "-" + str(j) + "\n"
                string += "# " + "".join(cur_pdb.models[j].sequence) + "\n"
                for k in range(len(bb_torsion)):
                    string += "%10s" % (cur_pdb.models[j].sequence_id[k])
                    for l in range(len(bb_torsion[k])):
                        string += "%10.3f" % (bb_torsion[k][l])
                    string += "\n"
            else:
                string = files[i] + "." + str(j) + " "
                for k in range(len(bb_torsion)):
                    for l in range(len(bb_torsion[k])):
                        string += "%10.3f" % (bb_torsion[k][l])

                # e2e stuff..
                pp1 = cur_pdb.models[j].residues[0].get_atom("C2")
                pp2 = cur_pdb.models[j].residues[-1].get_atom("C2")
                if(pp1 != None and pp2 != None):
                    diff = np.array(pp1)-np.array(pp2)
                    e2e =  np.sqrt(np.sum(diff**2))
                    string += " %f " % (e2e)
                else:
                    print "# No C2?", files[i]
                    string += " NaN "
                # end...

                string += "\n"
            fh.write(string)
                
            # calculate interactions
            #ss_torsion = cur_pdb.models[j].get_sugar_torsion()



    fh.close()
    return 0
            
##################### ANNOTATE #######################