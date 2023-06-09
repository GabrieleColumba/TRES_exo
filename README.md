# TRES_Exo
TRES code adapted to simulate giant circumbinary planets (CBPs). 

Refer to https://github.com/amusecode/TRES#readme for a general description of TRES code and instructions on the installation procedure.

The main additions concerning planets include:
- Holman & Wiegert (1999) P-type stability criteria for CBPs*;
- energy-limited atmospheric photoevaporation of planets;
- initial planetary spin rate as 0.126 the breakup speed (Bryan+2018).

*to use this criterion you must verify that in TRES.py at line 249 the value is 4, as:    secular_code.parameters.stability_limit_specification = 4

<!-- ### Description
TRES is a numerical framework for simulating hierarchical triple systems with stellar and planetary components. 
Mass transfer from one star to another and the consequential effect to the orbital dynamics is realized via heuristic recipes.
These recipes are combined with three-body dynamics and stellar evolution inluding their mutual influences. 

TRES includes the effects of common-envelope evolution, circularized stable mass transfer, tides, gravitational wave emission and up-to-date stellar evolution through SeBa. Other stellar evolution codes such as SSE can also be used. Coming soon: TRES with MESA, transition to N-body calculations (including stellar evolution and dissipative processes) when the system's evolution is not secular anymore. 

This readme contains the following parts:

[Compilation](#Compilation)

[Simple examples](#Simple-examples-of-runs)

[Understanding the TRES output](#Understanding-the-TRES-output)

[Reducing the TRES output](#Reducing-the-TRES-output)

[TRES development team](#TRES-development-team)

[References](#References)
 -->


<!-- ## Installation & Compilation
TRES makes use of the Astrophysical Multipurpose Software Environment (AMUSE). See https://amusecode.github.io/ for how to install AMUSE. 
Note that for standard TRES usage, the only necessary community code to install is SeBa. 

Thus, after installing the AMUSE pre-requisites, we can simply install the minimal framework and then add SeBa:

```
pip install [--user] amuse-framework
pip install [--user] amuse-seba
```

After compiling AMUSE, TRES needs to be installed and compiled by means of the Makefile as following:

First, clone the TRES github repository:

```
git clone https://github.com/amusecode/TRES.git
```

Then, from the root of the cloned respository compile the Makefile:

```

cd seculartriple_TPS
make 

``` -->

## Simple runs examples
After installing and compiling the code (see instructions above) you can run from a terminal the following examples.

#### Example 1
Evolve a single system (binary star + CBP) that survives for one Hubble time (13.5 Gyr); use the following parameters:

- primary mass:   M1           1.04  Msun 
- secondary mass: M2           1.00  Msun
- CBP mass:       M3           0.011 Msun
- inner binary semimajor axis:  Ain       54.6  Rsun
- CBP semimajor axis:           Aout      477.8 Rsun
- inner binary eccentricity:    Ein       0.67
- CBP eccentricity:             Eout      0.15
- relative orbital inclination: i         1.9 (rad)
- simulation time:      T    1000 Myr


Run command:
```
python TRES.py --M1 1.04 --M2 1. --M3 0.011 --Ain 54.6 --Aout 477.8 --Ein 0.67 --Eout 0.15 -i 1.9 -T 1000  --no_stop_at_mass_transfer -f 'testRun_1.hdf'
```
assuming AMUSE is correctly installed in your python environment. This run will save the output to file 'testRun_1.hdf' (-f flag). Use the rdc_ py to read the output and print it in readable text format.

If you wish to run the complete evolution, use -T 13500 to simulate one Hubble time and you'll obtain a DWD-orbiting CBP ('Magrathea' planet).


#### Example. 2
Evolve a single system (binary star + CBP) where the inner binary merge from DWD around 10 Gyr; use the following command:

```
python TRES.py --M1 1.33 --M2 1.06 --M3 0.0046 --Ain 26.35 --Aout 3012.9 --Ein 0.3 --Eout 0.1 -i 1.7 -T 11000  --no_stop_at_mass_transfer -f 'testRun_2.hdf'
```


## Input parameters 

The full list of possible input parameters and options is found at https://github.com/amusecode/TRES#input-parameters.

<!-- 
```
                  parameter                               unit / default
--M1    {-M}      inner_primary_mass                      in Solar mass
--M2    {-m}      inner secondary mass                    in Solar mass 
--M3    {-l}      outer mass                              in Solar mass
--Ain   {-A}      inner semi major axis                   in Solar radius
--Aout  {-a}      outer semi major axis                   in Solar radius
--Ein   {-E}      inner eccentricity 
--Eout  {-e}      outer eccentricity 
-i, -I            relative inclination                    in rad  
--Gin   {-G}      inner argument of pericenter            in rad
--Gout  {-g}      outer argument of pericenter            in rad
--Oin   {-O}      inner longitude of ascending node       in rad
                  (outer longitude of ascending nodes = inner - pi)               
-Z      {-z}      metallicity                             default = 0.02 (Solar)
-t, -T            end time                                in Myr
-N, -n            integer number asigned to the triple    default = 0
    
    
-f                name of output file                     default = TRES
-F                type of output file (hdf5/txt)          default = hdf5
--dir_plots       directory for plots for debugging default = "" (current directory)
                  mode  (aka REPORT_DEBUG == True)
--max_CPU_time    maximum CPU time allowed (only works in combination with "stop_at_CPU_time")    
                                                default = 7200 (seconds)

--SN_kick_distr   supernova kick distribution   default = 10
        options:
        0:  No kick 
        1:  Hobbs, Lorimer, Lyne & Kramer 2005, 360, 974  
        2:  Hobbs, Lorimer, Lyne & Kramer 2005, 360, 974  scaled down for bh by mass
        3:  Arzoumanian ea 2002, 568, 289
        4:  Arzoumanian ea 2002, 568, 289 scaled down for bh by mass
        5:  Hansen & Phinney 1997, 291, 569
        6:  Hansen & Phinney 1997, 291, 569 scaled down for bh by mass
        7:  Paczynski 1990, 348, 485
        8:  Paczynski 1990, 348, 485 scaled down for bh by mass
        9:  Verbunt, Igoshev & Cator, 2017, 608, 57
        10:  Verbunt, Igoshev & Cator, 2017, 608, 57 scaled down for bh by mass 

```

Additionally, there is a list of stopping conditions that determines whether the simulation of a system should stop at a certain evolutionary phase. 
By default, these stopping conditions are set to True, which means they are in effect. However, the four specific mass transfer cases (stable, unstable, eccentric stable & eccentric unstable) are set to False by default. Once "--no_stop_at_mass_transfer" is set to False, it is possible to set the specific mass transfer cases to True.

```

action items                                    add these to:
--no_stop_at_mass_transfer                      avoid stopping the simulation at the onset of mass transfer 
--no_stop_at_init_mass_transfer                 avoid stopping the simulation if there is mass transfer initially
--no_stop_at_outer_mass_transfer                avoid stopping the simulation when tertiary initiates mass transfer 
                                                methodology is as of yet non-existent
--stop_at_stable_mass_transfer                  avoid stopping the simulation at the onset of stable mass transfer in the inner binary
--stop_at_unstable_mass_transfer                avoid stopping the simulation at the onset of unstable mass transfer in the inner binary (leading to common-envelope evolution)
--stop_at_eccentric_stable_mass_transfer        avoid stopping the simulation at the onset of stable mass transfer in the inner binary if the orbit is eccentric
--stop_at_eccentric_unstable_mass_transfer      avoid stopping the simulation at the onset of unstable mass transfer in the inner binary if the orbit is eccentric

--no_stop_at_merger                             avoid stopping the simulation after a merger
--no_stop_at_inner_collision                    avoid stopping the simulation after a collision in the inner binary
--no_stop_at_outer_collision                    avoid stopping the simulation after a collision involving the outer star
--no_stop_at_disintegrated                      avoid stopping after the system disintegrated into seperate systems
--stop_at_semisecular_regime                    to stop the simulation if the sytem is in the semi secular regime
--stop_at_SN                                    to stop the simulation when a supernova occurs
--stop_at_CPU_time                              to stop the simulation when the computational time exceeds a given value

```

 -->
 
<!-- ### Multiple systems with specified parameters

If you need to follow the triple evolution for multiple systems with parameters which are already specified you can start TRES multiple times, e.g.
```

python TRES.py -M 1.2 -m 0.5 -l 0.6 -E 0.1 -e 0.5 -A 200 -a 20000 -z 0.001 -T 10 
python TRES.py -M 1.5 -m 1 -l 0.6 -E 0.1 -e 0.5 -A 50 -a 20000 -z 0.001 -T 10 
python TRES.py -M 1.5 -m 1 -l 0.05 -E 0.1 -e 0.5 -A 50 -a 20000 -z 0.02 -T 10 

```
This is probably not handy for more than 5 systems. Although this can be added in e.g. a shell or Python script.
 -->

## Understanding the TRES output

Normally TRES adds the evolution history of individual systems in the TRES.hdf file. Every snapshot represents a moment in the evolution of the triple system when something interesting happened, for example one of the star transitions from the main-sequence to the hertzsprung gap, or mass transfer starts or stops. 


### Reducing the TRES output

The python script rdc_TRES.py reduce the TRES hdf output. Example command (that saves the output into a text file):
```
python rdc_TRES.py -f 'testRun_1.hdf'  > 'simul_1.dat'
```

The full list of available options is [default]:
```
-f      root of the name of the input file [TRES]
-F      extension of input file [hdf5]
-S      printing style [2] among: 
    0:      TRES standard - selected parameters
    1:      Full - all possible parameters are printed
    2:      Selected parameters are printed in a human readible way
```

<!-- Which parameters are printed and in which style can be adjusted to your liking in the function rdc().
Currently there are 3 options settable on the command line via -S (print_style):
```
    0:      TRES standard - selected parameters
    1:      Full - all possible parameters are printed
    2:      Selected parameters are printed in a human readible way
```
 -->

Legend for default option -S 2: 

6 lines are printed for every snapshot. The lines contain:

General information on the system: 
```
Line 1: snapshot number, time, triple number, relative_inclination, dynamical_instability, kozai_type, error_flag_secular, CPU_time
```
Orbital information (inner binary | outer binary) :
```
Line 2: 'bs:', binary type, stability, semimajoraxis, eccentricity, argument_of_pericenter, longitude_of_ascending_node 
           | , binary type, stability, semimajoraxis, eccentricity, argument_of_pericenter, longitude_of_ascending_node 
```
Stellar information (primary | secondary | tertiary)
```
Line 3: 'st:', is_donor, stellar_type, mass, spin_angular_frequency, radius, core mass
          |  , is_donor, stellar_type, mass, spin_angular_frequency, radius, core mass
          |  , is_donor, stellar_type, mass, spin_angular_frequency, radius, core mass
```        

For all stellar and binary types classes see https://github.com/amusecode/TRES#reducing-the-tres-output.
<!-- 
For option 0: 
One line is printed for every snapshot with the parameters in the same order as above. The units are Solar Mass, Solar radius, Myr. 

The stellar types in TRES follow the standard terminology of AMUSE:
```
0 deeply or fully convective low mass MS star
1 Main Sequence star
2 Hertzsprung Gap
3 First Giant Branch
4 Core Helium Burning
5 Early Asymptotic Giant Branch
6 Thermally Pulsating Asymptotic Giant Branch (not used in SeBa -> labelled as 5) 
7 Main Sequence Naked Helium star
8 Hertzsprung Gap Naked Helium star
9 Giant Branch Naked Helium star
10 Helium White Dwarf
11 Carbon/Oxygen White Dwarf
12 Oxygen/Neon White Dwarf
13 Neutron Star
14 Black Hole
15 Massless Supernova
16 Unknown stellar type
17 Pre-main-sequence Star
18 Planet
19 Brown Dwarf
```

The binary type is a classification for a specific orbit, e.g. the inner or the outer orbit of a triple. The following options exist:
```
unknown
merger
disintegrated
dynamical_instability
detached
contact
collision
semisecular
rlof
stable_mass_transfer
common_envelope
common_envelope_energy_balance (i.e. alpha-CE)
common_envelope_angular_momentum_balance (i.e. gamma-CE)
double_common_envelope
```

Do you want to rerun a system in your datafile? No need to copy all the parameters, simply run rdc_TRES.py with two extra parameters: 

```
--print_init      to print initial conditions for re-running 
-l                the line number of the first line in your hdf datafile where the system appears
                  where the stars are on the zero-age main-sequence. 
``` 
For example: ```rdc_TRES.py -f TRES.hdf --print_init -l 0```. This will return something like:
```amuse TRES.py -M 1.3 -m 0.5  -l  0.5 -A 200.0 -a 20000.0 -E 0.1 -e 0.5 -G 0.1 -g 0.5 -I 1.3962634016 ```


 -->



## Random Population synthesis

A random population can be generated and simulated with TPS.py, with a Monte Carlo based approach. Example run: 
```
python TPS.py -n 10 --M_max 5 --M_min 4  --M_distr 0 --A_max 2000 --A_min 200 --A_distr 2
```
where M_max e M_min are the primary star mass boundaries and \_distr is the chosen prior distribution to extract random samples from.
See https://github.com/amusecode/TRES#input-parameters for the full list of initialising options and priors. 

TPS.py embeds TRES.py to simulate the evolution of each single triple system.
The output of TPS.py is saved analogously as TRES output, with the evolution of different systems appended in sequence.

We report here below the distributions specifically implemented for CBPs.

```
[...]
--Qout_max     {--q_max}    upper limit for the outer mass ratio [1.]
--Qout_min     {--q_min}    lower limit for the mass of the outer star [0.]
--Qout_distr   {--q_distr}  outer mass ratio option: 
        2: "Galicher 2016 powerlaw (M^-1.31)",  # not default
--l_max    upper limit for the outer mass  [16 Mjup]
--l_min    lower limit for the outer mass  [0.2 Mjup]
 
--Aout_max     {--a_max}    upper limit for the outer semi-major axis [5e6 RSun]
--Aout_min     {--a_min}    lower limit for the outer semi-major axis [5 RSun]
--Aout_distr   {--a_distr}  outer semi-major axis option: 
        6: "flat distribution",  # (uniform)
        7: "Galicher 2016 powerlaw (a^-0.61)",                                 
--Eout_max     {--e_max}    upper limit for the outer eccentricity [1.]
--Eout_min     {--e_min}    lower limit for the outer eccentricity [0.]
--Eout_distr   {--e_distr}  outer eccentricity option: 
        5: "Beta distribution (Bowler+ 2020)",    # SSOs 
```



## References

Please read and refer to [Columba et al. 2023](https://www.aanda.org/component/article?access=doi&doi=10.1051/0004-6361/202345843) for more details and the full report on the new implementations in TRES-Exo.
See [Toonen et al. 2016](https://ui.adsabs.harvard.edu/abs/2016ComAC...3....6T/abstract) for details on TRES.




