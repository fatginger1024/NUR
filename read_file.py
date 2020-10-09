import glob
import h5py
import os
import numpy as np


from scipy.interpolate import RegularGridInterpolator

datadir = './CoolingTables/'

tables = {
    'metal_free': [
        'electron_density_over_n_h',
        'net_cooling',
        'helium_mass_fraction_bins',
        'hydrogen_density_bins',
        'temperature_bins',
    ],
    'total_metals': [
        'net_cooling',
        'hydrogen_density_bins',
        'temperature_bins',
    ],
    'solar': [
        'electron_density_over_n_h',
        'hydrogen_density_bins',
        'temperature_bins',
    ]
}


def get_redshift(datadir):
    files = glob.glob(os.path.join(datadir, 'z_[0-9].*[0-9].hdf5'))
    rs = []
    for i in files:
        rs.append(float(i.replace('.hdf5', '').split('z_')[-1]))
    order = np.argsort(rs)
    files = np.array(files)
    rs = np.array(rs)
    return rs[order], files[order]


def get_table(f, name):
    for i in f.keys():
        if i.lower() == name:
            return f[i]


def get_data(fp, t_name):
    f = h5py.File(fp, 'r')
    print("open %s, reading table: %s" % (fp, t_name))
    table = get_table(f, t_name)
    data = {}
    for i in tables[t_name]:
        data[i] = get_table(table, i)[...]
        if t_name == 'metal_free' and (i == 'electron_density_over_n_h' or i == 'net_cooling'):
            index = np.where(
                get_table(table, 'helium_mass_fraction_bins')[...] == 0.258)[0][0]
        #   print('test:',index)
            data[i] = get_table(table, i)[index]
    return data


def stack_in_redshift(tables_in_redshift, prop):
    data = []
    for i in tables_in_redshift:
        data.append(i[prop])
    data = np.stack(data)
    return data


def get_bins(tables_in_redshift, prop):
    return tables_in_redshift[0][prop]


def interpolat_3d(data, x, y, z):
    func = RegularGridInterpolator((x, y, z), data)
    return func


def main():
    rs, files = get_redshift(datadir=datadir)
    MF = []
    TM = []
    SO = []
    for i in range(len(rs)):
        redshift = rs[i]
        fp = files[i]
        MF.append(get_data(fp, 'metal_free'))
        TM.append(get_data(fp, 'total_metals'))
        SO.append(get_data(fp, 'solar'))
    mf_ed = stack_in_redshift(MF, 'electron_density_over_n_h')
    mf_nc = stack_in_redshift(MF, 'net_cooling')
    mf_hdbin = get_bins(MF, 'hydrogen_density_bins')
    mf_tbin = get_bins(MF, 'temperature_bins')
    my_mf_nc = interpolat_3d(mf_nc, rs, mf_tbin, mf_hdbin)
    my_mf_ed = interpolat_3d(mf_ed, rs, mf_tbin, mf_hdbin)

    tm_nc = stack_in_redshift(TM, 'net_cooling')
    tm_hdbin = get_bins(TM, 'hydrogen_density_bins')
    tm_tbin = get_bins(TM, 'temperature_bins')
    my_tm_nc = interpolat_3d(tm_nc, rs, tm_tbin, tm_hdbin)

    so_ed = stack_in_redshift(SO, 'electron_density_over_n_h')
    so_hdbin = get_bins(SO, 'hydrogen_density_bins')
    so_tbin = get_bins(SO, 'temperature_bins')
    my_so_ed = interpolat_3d(so_ed, rs, so_tbin, so_hdbin)
    return my_mf_ed, my_mf_nc, my_tm_nc, my_so_ed


def get_net_cooling(funcs, points, frac):
    func_mf_ed, func_mf_nc, func_tm_nc, func_so_ed = funcs
    mf_ed = func_mf_ed(points)
    mf_nc = func_mf_nc(points)
    tm_nc = func_tm_nc(points)
    so_ed = func_so_ed(points)
    lam = mf_nc + tm_nc*mf_ed/so_ed*frac
    return lam

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    funcs = main()
    # problem a:
    z = 3
    temp = np.logspace(4, 8.8, 1000)
    density = np.array([1e0, 1e-2, 1e-4, 1e-6])
    for d in density:
        points = np.array([[z, t, d] for t in temp])
        lam = get_net_cooling(funcs, points, 0.25)
        plt.plot(temp, lam, label='%f' % d)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    # problem b
    zs = np.linspace(0,9,1000)
    temp = np.logspace(4, 8.8, 1000)
    d = 1e-4
    for z in zs[1:]:
        points = np.array([[z, t, d] for t in temp])
        lam = get_net_cooling(funcs, points, 0.5)
