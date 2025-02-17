from amuse.units import units, constants
from amuse.io import write_set_to_file
from amuse.io import read_set_from_file
from amuse.support.console import set_printing_strategy
import numpy as np
import io
    
minimum_time_step = 1.e-9 |units.Myr


bin_type = {    
                'unknown': 0,       
                'merger': 1, 
                'disintegrated': 2, 
                'dynamical_instability': 3, 
                'detached': 4,       
                'contact': 5,    
                'collision': 6,    
                'semisecular': 7,      
                'rlof': 8,   #only used for stopping conditions
                'stable_mass_transfer': 9, 
                'common_envelope': 10,     
                'common_envelope_energy_balance': 11,     
                'common_envelope_angular_momentum_balance': 12,
                'double_common_envelope': 13,
            }            



lib_print_style = { 0: "TRES standard; selected parameters", 
                1: "Full",
                2: "Readable format",}#default

def print_particle(particle):
        if particle.is_star:
            print(particle)                 
        else:
            print(particle) 
            print_particle(particle.child1)                
            print_particle(particle.child2)                


def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

       
#for more info on mass transfer stability, see triple[0].is_mt_stable & triple[0].child2.is_mt_stable
def rdc(file_name_root, print_style, print_full, print_init, line_number):

    file_name = file_name_root + ".hdf"            
    if file_name_root[-4:]==".hdf":
        file_name = file_name_root

    triple=read_set_from_file(file_name , "hdf5")
#    counter = list(enumerate(triple.history))[0][1].number 

    if print_init:
        for i, triple in enumerate(triple.history):
            if i == line_number:
                print('amuse TRES.py ', end = '' )
                print(' -M ', triple[0].child2.child1.mass.value_in(units.MSun), ' -m ', triple[0].child2.child2.mass.value_in(units.MSun), ' -l ', triple[0].child1.mass.value_in(units.MSun), end = '')
                print(' -A ', triple[0].child2.semimajor_axis.value_in(units.RSun), ' -a ', triple[0].semimajor_axis.value_in(units.RSun), end = '')
                print(' -E ', triple[0].child2.eccentricity, ' -e ', triple[0].eccentricity, end = '')
                print(' -G ', triple[0].child2.argument_of_pericenter, ' -g ', triple[0].argument_of_pericenter, end = '')
                print(' -I ', triple[0].relative_inclination, end = '\t')
                
                if triple[0].time > minimum_time_step:
                    print('Warning: these parameters do not represent a system at birth (ZAMS).')

        return

    print(lib_print_style[print_style])
    triple_string = ''
    snapshot_string = '' 
    triple_number = 0
    previous_triple_number = -1 
    
    for i, triple in enumerate(triple.history):
#        print(triple[0].number, triple[0].time)
#        if triple[0].number == counter:
#            counter += 1    
#            print('\n\n')

        #which snapshots to save
        if print_full: #all snapshots    
            triple_string = triple_string + snapshot_string   
        else: #first & last line 
#            print(i, triple[0].number,triple_number, previous_triple_number)
            if triple[0].number>triple_number: # last line
                 triple_string = triple_string + snapshot_string
                 triple_number = triple[0].number
                 print(triple_string[:-2]) #prevents empty line
                 triple_string = ''
            elif triple_number > previous_triple_number: #first line
                 triple_string = triple_string + snapshot_string
                 previous_triple_number = triple_number                         
        snapshot_string = '' 
        
        if print_style == 2:
            if i>0:
                snapshot_string = snapshot_string + print_to_string(' ')
            snapshot_string = snapshot_string + print_to_string(i, triple[0].number, triple[0].time, triple[0].relative_inclination, triple[0].dynamical_instability, triple[0].kozai_type, triple[0].error_flag_secular, triple[0].CPU_time)
            snapshot_string = snapshot_string + print_to_string(' bs: ', triple[0].child2.bin_type, triple[0].child2.semimajor_axis, triple[0].child2.eccentricity, triple[0].child2.argument_of_pericenter, triple[0].child2.longitude_of_ascending_node)
            snapshot_string = snapshot_string + print_to_string('|', triple[0].bin_type, triple[0].semimajor_axis, triple[0].eccentricity, triple[0].argument_of_pericenter, triple[0].longitude_of_ascending_node)
            snapshot_string = snapshot_string + print_to_string(' st: ',  triple[0].child2.child1.is_donor, triple[0].child2.child1.stellar_type, triple[0].child2.child1.mass,  triple[0].child2.child1.spin_angular_frequency, triple[0].child2.child1.radius, triple[0].child2.child1.core_mass)
            snapshot_string = snapshot_string + print_to_string('|', triple[0].child2.child2.is_donor,  triple[0].child2.child2.stellar_type, triple[0].child2.child2.mass, triple[0].child2.child2.spin_angular_frequency, triple[0].child2.child2.radius,triple[0].child2.child2.core_mass)
            snapshot_string = snapshot_string + print_to_string('|', triple[0].child1.is_donor, triple[0].child1.stellar_type, triple[0].child1.mass, triple[0].child1.spin_angular_frequency, triple[0].child1.radius, triple[0].child1.core_mass)


#            print(' ')
#            print(i, triple[0].number, triple[0].time, triple[0].relative_inclination, triple[0].dynamical_instability, triple[0].kozai_type, triple[0].error_flag_secular, triple[0].CPU_time)
#                  
#            print( ' bs: ', triple[0].child2.bin_type, triple[0].child2.semimajor_axis, triple[0].child2.eccentricity, triple[0].child2.argument_of_pericenter, triple[0].child2.longitude_of_ascending_node,)# triple[0].child2.mass_transfer_rate,
#            print( '|', triple[0].bin_type, triple[0].semimajor_axis, triple[0].eccentricity, triple[0].argument_of_pericenter, triple[0].longitude_of_ascending_node)#, triple[0].mass_transfer_rate
#            print( ' st: ',  triple[0].child2.child1.is_donor, triple[0].child2.child1.stellar_type, triple[0].child2.child1.mass,  triple[0].child2.child1.spin_angular_frequency, triple[0].child2.child1.radius, triple[0].child2.child1.core_mass,)
#            print( '|', triple[0].child2.child2.is_donor,  triple[0].child2.child2.stellar_type, triple[0].child2.child2.mass, triple[0].child2.child2.spin_angular_frequency, triple[0].child2.child2.radius,triple[0].child2.child2.core_mass, )
#            print( '|', triple[0].child1.is_donor, triple[0].child1.stellar_type, triple[0].child1.mass, triple[0].child1.spin_angular_frequency, triple[0].child1.radius, triple[0].child1.core_mass)
            

        elif print_style == 1:
            print_particle(triple[0])
        
#            print('triple particle', triple[0])
#            print('child1', triple[0].child1)
#            print('child2',triple[0].child2)
#            print('child2.child1',triple[0].child2.child1)
#            print('child2.child2',triple[0].child2.child2)
            exit(0)
        else:

            snapshot_string = snapshot_string + print_to_string(triple[0].number, triple[0].time.value_in(units.Myr), triple[0].relative_inclination, int(triple[0].dynamical_instability), int(triple[0].kozai_type), int(triple[0].error_flag_secular), triple[0].CPU_time, end = '\t')
            snapshot_string = snapshot_string + print_to_string(bin_type[triple[0].child2.bin_type], triple[0].child2.semimajor_axis.value_in(units.RSun), triple[0].child2.eccentricity, triple[0].child2.argument_of_pericenter, triple[0].child2.longitude_of_ascending_node, end = '\t')
            snapshot_string = snapshot_string + print_to_string(bin_type[triple[0].bin_type], triple[0].semimajor_axis.value_in(units.RSun), triple[0].eccentricity, triple[0].argument_of_pericenter, triple[0].longitude_of_ascending_node, end = '\t')
            snapshot_string = snapshot_string + print_to_string(int(triple[0].child2.child1.is_donor), triple[0].child2.child1.stellar_type.value_in(units.stellar_type), triple[0].child2.child1.mass.value_in(units.MSun),  triple[0].child2.child1.spin_angular_frequency.value_in(1./units.Myr), triple[0].child2.child1.radius.value_in(units.RSun), triple[0].child2.child1.core_mass.value_in(units.MSun), end = '\t')
            snapshot_string = snapshot_string + print_to_string(int(triple[0].child2.child2.is_donor),  triple[0].child2.child2.stellar_type.value_in(units.stellar_type), triple[0].child2.child2.mass.value_in(units.MSun), triple[0].child2.child2.spin_angular_frequency.value_in(1./units.Myr), triple[0].child2.child2.radius.value_in(units.RSun),triple[0].child2.child2.core_mass.value_in(units.MSun), end = '\t')
            snapshot_string = snapshot_string + print_to_string(int(triple[0].child1.is_donor), triple[0].child1.stellar_type.value_in(units.stellar_type), triple[0].child1.mass.value_in(units.MSun), triple[0].child1.spin_angular_frequency.value_in(1./units.Myr), triple[0].child1.radius.value_in(units.RSun), triple[0].child1.core_mass.value_in(units.MSun))

#            print(triple[0].number, triple[0].time.value_in(units.Myr), triple[0].relative_inclination, int(triple[0].dynamical_instability), int(triple[0].kozai_type), int(triple[0].error_flag_secular), triple[0].CPU_time, end = '\t')
#            print(bin_type[triple[0].child2.bin_type], triple[0].child2.semimajor_axis.value_in(units.RSun), triple[0].child2.eccentricity, triple[0].child2.argument_of_pericenter, triple[0].child2.longitude_of_ascending_node, end = '\t')
#            print(bin_type[triple[0].bin_type], triple[0].semimajor_axis.value_in(units.RSun), triple[0].eccentricity, triple[0].argument_of_pericenter, triple[0].longitude_of_ascending_node, end = '\t')
#            print(int(triple[0].child2.child1.is_donor), triple[0].child2.child1.stellar_type.value_in(units.stellar_type), triple[0].child2.child1.mass.value_in(units.MSun),  triple[0].child2.child1.spin_angular_frequency.value_in(1./units.Myr), triple[0].child2.child1.radius.value_in(units.RSun), triple[0].child2.child1.core_mass.value_in(units.MSun), end = '\t')
#            print(int(triple[0].child2.child2.is_donor),  triple[0].child2.child2.stellar_type.value_in(units.stellar_type), triple[0].child2.child2.mass.value_in(units.MSun), triple[0].child2.child2.spin_angular_frequency.value_in(1./units.Myr), triple[0].child2.child2.radius.value_in(units.RSun),triple[0].child2.child2.core_mass.value_in(units.MSun), end = '\t' )
#            print(int(triple[0].child1.is_donor), triple[0].child1.stellar_type.value_in(units.stellar_type), triple[0].child1.mass.value_in(units.MSun), triple[0].child1.spin_angular_frequency.value_in(1./units.Myr), triple[0].child1.radius.value_in(units.RSun), triple[0].child1.core_mass.value_in(units.MSun))





        if i==0:
            triple_string = triple_string + snapshot_string
            #in case triple[0].number in file doesn't start at 0
            triple_number = triple[0].number
            previous_triple_number = triple_number                         
    
    triple_string = triple_string + snapshot_string
    print(triple_string)


def parse_arguments():
    from amuse.units.optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", dest="file_name_root", default = "TRES",
                      help="file name [%default]")                      
    parser.add_option("-S", dest="print_style", type="int", default = 2,
                      help="print style [%default]") 
    parser.add_option("-F", dest="print_full", action="store_true", default = False, 
                      help="print every snapshot for specified triple [%default]")
    parser.add_option("--print_init", dest="print_init", action="store_true", default = False, 
                      help="print initial conditions for re running [%default]")
    parser.add_option("-l", dest="line_number", type="int", default = 0,
                      help="line number for printing initial conditions [%default]") #will only do something when print_init = True


                      
    options, args = parser.parse_args()
    return options.__dict__


if __name__ == '__main__':
    options = parse_arguments()

    set_printing_strategy("custom", 
                          preferred_units = [units.MSun, units.RSun, units.Myr], 
                          precision = 11, prefix = "", 
                          separator = " [", suffix = "]")



    print(' ')
    rdc(**options)  
    
