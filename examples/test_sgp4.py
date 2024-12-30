# import the load_utils helper
import load_utils

# init the astrostandards
print('\nInitializing the astrostandards\n')
ptr = load_utils.init_all( logfile='test.log' ) 

# test TLE
L1 = '1 25544U 98067A   24365.67842578  .00026430  00000-0  46140-3 0  9990'
L2 = '2 25544  51.6404  61.8250 0005853  25.4579 117.0387 15.50482079489028'

# load the TLE
tleid = load_utils.TleDll.TleAddSatFrLines( 
    load_utils.Cstr( L1, 512 ),
    load_utils.Cstr( L2, 512 )
    )
print('TLE id inside astrostandards is {}'.format( tleid ) )
assert tleid > 0

# init the SGP4 prop
# you need the license file to be readable (easiest is in current directory) for this to work
sgp4 = load_utils.Sgp4PropDll.Sgp4InitSat( tleid )
print('SGP4 init returned : {}'.format( sgp4 ) )
assert sgp4 == 0

# now lets propagate using the "minutes since epoch" function
# look at the C headers to get good documentation on available functions (e.g.Sgp4PropDll.h)

# data holders for OUTPUT
ds50 = load_utils.ctypes.c_double() 
pos  = (load_utils.ctypes.c_double * 3)()
vel  = (load_utils.ctypes.c_double * 3)()
llh  = (load_utils.ctypes.c_double * 3)()
date = load_utils.Cstr('',19)       # < -- C-string, length 19, initially blank

# loop over minutes to propagate (from epoch)
minutes = range( 0, 1440, 10 )
for M in minutes:
    load_utils.Sgp4PropDll.Sgp4PropMse( 
        tleid,      # <-- input: tleid
        M,          # <-- input: minutes from epoch
        ds50,       # <-- output : days since 1950 of this point (auto-calced from epoch and minutes)
        pos,        # <-- output : position (TEME)
        vel,        # <-- output : velocity (TEME)
        llh)        # <-- output : lat/long/alt

    # convert that 1950 date to a more readable format using astrostandards
    load_utils.TimeFuncDll.UTCToDTG19( ds50, date )   # <-- pass in the date string holder
    print('{}'.format( date.value.decode('utf-8') ) )
    print('POS : {}'.format( list(pos) ) )
    print('VEL : {}'.format( list(vel) ) )
    print('LLH : {}'.format( list(llh) ) )
    print()