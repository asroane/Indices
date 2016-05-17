#plotting spectral types vs indices
'''lines commented with "change" should change the number for j['index_value'] or j['index_name'] for the molecule in the
text file to find indices for'''
import pandas as pd
from astrodbkit import astrodb
import index_calc
import pylab
import avgflux
import math
import matplotlib.pyplot as plt

fieldspectraltypes = []
fieldindices = []
lowspectraltypes = []
lowindices = []
db = astrodb.Database('/users/brownscholar/desktop/bdnyc/bdnyc315.db')

#db = astrodb.Database('path/to/db') "h2o_indices.txt"
dfspec=pd.DataFrame(data=db.query("SELECT id, source_id, wavelength, wavelength_units, flux, flux_units, unc, snr, wavelength_order, regime, publication_id, obs_date, instrument_id, telescope_id, mode_id, airmass, filename, comment FROM spectra"), columns=['id','source_id','wavelength','wavelength_units','flux','flux_units','unc','snr','wavelength_order','regime', 'publication_id','obs_date','instrument_id','telescope_id','mode_id','airmass','filename', 'comment'])
fieldgravity_standards = [4,97,229,131,99,197,190]
lowgravity_standards = [80,267,48,84,181,102,275]

for i in fieldgravity_standards:
	j = index_calc.index_3inputs(dfspec,i,"gravnoheader.txt") #use 3 inputs for gravity sensitive indices, 2 for water indices
	k = db.query("select spectral_types.spectral_type from spectra join spectral_types on spectra.source_id = spectral_types.source_id where spectra.id = {} and spectral_types.regime = 'OPT'".format(i))
	try:
		l = k[0]
		fieldspectraltypes.append(l[0])
		fieldindices.append(j['index_value'][1]) #change
		name = j['index_name'][1] #change
	except TypeError:
		pass
		
for i in lowgravity_standards:
	j = index_calc.index_3inputs(dfspec,i,"gravnoheader.txt") #use 3 inputs for gravity sensitive indices, 2 for water indices
	k = db.query("select spectral_types.spectral_type from spectra join spectral_types on spectra.source_id = spectral_types.source_id where spectra.id = {} and spectral_types.regime = 'OPT'".format(i))
	try:
		l = k[0]
		lowspectraltypes.append(l[0])
		lowindices.append(j['index_value'][1]) #change
	except TypeError:
		pass

plt.scatter(lowspectraltypes,lowindices,facecolors='red', edgecolors='none', s=50)
plt.scatter(fieldspectraltypes,fieldindices,facecolors='blue', edgecolors='none', s=50)
plt.xlabel("OPT Spectral Type", fontsize = 30)
plt.ylabel("%s Index" %name, fontsize = 30)
plt.title('%s' %name, fontsize = 40)
plt.show()
plt.close()