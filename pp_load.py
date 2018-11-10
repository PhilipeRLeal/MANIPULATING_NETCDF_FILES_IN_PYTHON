# encoding: utf-8

# import netCDF4 as nc

# dt_45_2055 = nc.Dataset('/home/vitorgalazzo/Documents/RCP4.5_anomaly_2055.nc')
# dt_85_2055 = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2055.nc')
# dt_45_2099 = nc.Dataset('/home/vitorgalazzo/Documents/RCP4.5_anomaly_2099.nc')
# dt_85_2099 = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2099.nc')
dta = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2055_nf.nc')
dtb = nc.Dataset('/home/vitorgalazzo/Documents/RCP4.5_anomaly_2055_JFM_nf.nc')
dtc = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2099_AMJ_nf.nc')
dtd = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2099_JAS_nf.nc')
dte = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2099_OND_nf.nc')
# dt_85_2099_nf = nc.Dataset('/home/vitorgalazzo/Documents/RCP8.5_anomaly_2099_nf.nc')

histlist = [dta,
dtb,
dtc,
dtd,
dte]

hl = np.array([histlist[x].variables['histclim'][:] for x in xrange(5)])

harr = hl[:,::-1,:]

harr = np.where(harr>1e10,np.nan,harr)

ssn = ['year', 'JFM', 'AMJ', 'JAS', 'OND']

dt_45_2055 = []
for s in ssn:
	filename = '/home/vitorgalazzo/Documents/Clima/clima/anomaly/RCP4.5_anomaly_2055_%s.nc' % s
	dt_45_2055.append(nc.Dataset(filename))

dt_85_2055 = []
for s in ssn:
	filename = '/home/vitorgalazzo/Documents/Clima/clima/anomaly/RCP8.5_anomaly_2055_%s.nc' % s
	dt_85_2055.append(nc.Dataset(filename))

dt_45_2099 = []
for s in ssn:
	filename = '/home/vitorgalazzo/Documents/Clima/clima/anomaly/RCP4.5_anomaly_2099_%s.nc' % s
	dt_45_2099.append(nc.Dataset(filename))

dt_85_2099 = []
for s in ssn:
	filename = '/home/vitorgalazzo/Documents/Clima/clima/anomaly/RCP8.5_anomaly_2099_%s.nc' % s
	dt_85_2099.append(nc.Dataset(filename))
	

lat  = dt_45_2055[0].variables['lat'][:]
lon  = dt_85_2055[0].variables['lon'][:]

# dtlist = [dt_45_2055, dt_85_2055, dt_45_2099, dt_85_2099]
varlist = ['histclim', 'anomaly', 'histstddev', 'varratio']


arr45_2055l = []
arr85_2055l = []
arr45_2099l = []
arr85_2099l = []
for x in xrange(5):
	arr45_2055l.append(np.array([dt_45_2055[x].variables[v][:] for v in varlist]))
	arr45_2055 = np.array(arr45_2055l)
	arr85_2055l.append(np.array([dt_85_2055[x].variables[v][:] for v in varlist]))
	arr85_2055 = np.array(arr85_2055l)
	arr45_2099l.append(np.array([dt_45_2099[x].variables[v][:] for v in varlist]))
	arr45_2099 = np.array(arr45_2099l)
	arr85_2099l.append(np.array([dt_85_2099[x].variables[v][:] for v in varlist]))
	arr85_2099 = np.array(arr85_2099l)
	

	# arr85_2055_nf = np.array([dt_85_2055_nf.variables[x][:] for x in varlist])
	# arr85_2099_nf = np.array([dt_85_2099_nf.variables[x][:] for x in varlist])

arr45_2055_t = arr45_2055[:,:,::-1,:]
arr85_2055_t = arr85_2055[:,:,::-1,:]
arr45_2099_t = arr45_2099[:,:,::-1,:]
arr85_2099_t = arr85_2099[:,:,::-1,:]
# arr85_2055_nf = arr85_2055_nf[:,::-1,:]
# arr85_2099_nf = arr85_2099_nf[:,::-1,:]

arr45_2055_t = np.where(arr45_2055_t>1e10,np.nan,arr45_2055_t)
arr85_2055_t = np.where(arr85_2055_t>1e10,np.nan,arr85_2055_t)
arr45_2099_t = np.where(arr45_2099_t>1e10,np.nan,arr45_2099_t)
arr85_2099_t = np.where(arr85_2099_t>1e10,np.nan,arr85_2099_t)
# arr85_2055_nf = np.where(arr85_2055_nf>1e10,np.nan,arr85_2055_nf)
# arr85_2099_nf = np.where(arr85_2099_nf>1e10,np.nan,arr85_2099_nf)

anm45_2055mol = arr45_2055_t[:,1,:,:]
anm85_2055mol = arr85_2055_t[:,1,:,:]
anm45_2099mol = arr45_2099_t[:,1,:,:]
anm85_2099mol = arr85_2099_t[:,1,:,:]

ct = 1e-6*3600*24*12.0107

anm45_2055 = anm45_2055mol*ct
anm85_2055 = anm85_2055mol*ct
anm45_2099 = anm45_2099mol*ct
anm85_2099 = anm85_2099mol*ct

ln45_2055 = []
for a in anm45_2055:
	linhas=[]
	for x in a:
		l = [x]*12
		for y in l:
			linhas.append(y)
	ln = []
	for x in linhas:
		y = np.array([[z]*12 for z in x]).reshape(1,1488)
		ln.append(y[0])
	ln45_2055.append(ln)

anm45_2055_9 = np.array(ln45_2055)

ln85_2055 = []
for a in anm85_2055:
	linhas=[]
	for x in a:
		l = [x]*12
		for y in l:
			linhas.append(y)
	ln = []
	for x in linhas:
		y = np.array([[z]*12 for z in x]).reshape(1,1488)
		ln.append(y[0])
	ln85_2055.append(ln)

anm85_2055_9 = np.array(ln85_2055)

ln45_2099 = []
for a in anm45_2099:
	linhas=[]
	for x in a:
		l = [x]*12
		for y in l:
			linhas.append(y)
	ln = []
	for x in linhas:
		y = np.array([[z]*12 for z in x]).reshape(1,1488)
		ln.append(y[0])
	ln45_2099.append(ln)

anm45_2099_9 = np.array(ln45_2099)

ln85_2099 = []
for a in anm85_2099:
	linhas=[]
	for x in a:
		l = [x]*12
		for y in l:
			linhas.append(y)
	ln = []
	for x in linhas:
		y = np.array([[z]*12 for z in x]).reshape(1,1488)
		ln.append(y[0])
	ln85_2099.append(ln)

anm85_2099_9 = np.array(ln85_2099)


# f, axm = plt.subplots()
# m = bm(ellps = 'WGS84', llcrnrlon=-130, llcrnrlat=-62, urcrnrlon=-6, urcrnrlat=32,
# 		 resolution='i', ax=axm)
