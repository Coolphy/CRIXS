from adress import *
import h5py
import xarray as xr
import pandas as pd
from bokeh.plotting import figure, show,output_notebook,output_file, save
from itertools import cycle

__all__ = ['VERITAS']

class VERITAS:

    def __init__(self,p='/data/visitors/veritas/20240848/2024100208/raw/'):

        self.data_folder = p
        self._acq = []
        self._entry = []
        self._rixs = {}
        self._xas = {}
        self._meta = {}

    def load_entry(self,file,run_list,labels):
        
        """
        load scan file

        RMU : aemexp2_ch1
        TFY : aemexp2_ch2
        TEY : aemexp2_ch3
        """
        
        # load file
        f = h5py.File(file, 'r')
        print(f'Open file {file}')
        for entry in run_list:
            if entry in self._entry:
                pass
            else:
                temp = {}
                temp['Pt_No'] = f[entry]['measurement']['Pt_No'][:]
                for label in labels:
                    try:
                        temp[label] = f[entry]['measurement'][label][:]
                    except:
                        raise KeyError(f'Entry {entry} no {label}')

                self._entry.append(entry)
                self._xas[entry] = temp
        f.close()

    def load_acq(self,file,run_list):
        
        """
        load rixs file

        save meta data
        """
        
        # load file
        f = h5py.File(file, 'r')
        print(f'Open file {file}')
        for acq in run_list:
            if acq in self._acq:
                pass
            else:               
                meta = {}
                # meta['Temp'] = temperature
                meta['RMU']  = sum(f[acq]['External']['aemexp2_ch1']['InstantCurrent'][:,1])
                meta['TFY']  = sum(f[acq]['External']['aemexp2_ch2']['InstantCurrent'][:,1])
                meta['TEY']  = sum(f[acq]['External']['aemexp2_ch3']['InstantCurrent'][:,1])
                meta['FF']  = sum(f[acq]['External']['aemexp2_ch4']['InstantCurrent'][:,1])
                meta['x']  = round(f[acq]['startmetadata']['a_mp1_x']['position'][()],4)
                meta['y']  = round(f[acq]['startmetadata']['a_mp1_y']['position'][()],4)
                meta['z']   = round(f[acq]['startmetadata']['a_mp1_z']['position'][()],4)
                meta['yaw']   = round(f[acq]['startmetadata']['a_mp1_yaw']['position'][()],3)
                meta['arm']  = round(f[acq]['startmetadata']['q_angle']['position'][()],3)
                meta['slits']  = round(f[acq]['startmetadata']['a_slit1_v']['position'][()],3)
                meta['energy']   = round(f[acq]['startmetadata']['beamline_energy']['position'][()],3) 
                meta['phase']  = round(f[acq]['startmetadata']['epu_r3_316_phase']['position'][()])
                
                self._meta[acq] = meta
                rixs = f[acq]['Instrument']['DLD8080']['calibrated_data']['calib_x_spectrum'][:]
                ee = f[acq]['Instrument']['DLD8080']['calibration']['energy_scale'][:]

                self._acq.append(acq)
                self._rixs[acq] = {
                    'rixs':rixs,
                    'emission':ee,
                }
                
        f.close()
        

    def load_xas(self, filename, scans):
        """
        load xas data

        return RMU,TFY,TEY
        """
        if isinstance(scans, int):
            scans = [scans]

        # find prefix
        prefix = 'entry'
        new_scans = []
        for scan in scans:
            if prefix+f'{scan}' in self._entry:
                pass
            else:
                new_scans.append(prefix+f'{scan}')

        if len(new_scans) == 0:
            pass
        else:
            file = self.data_folder + '/' + filename
            self.load_entry(file,new_scans,['beamline_energy','aemexp2_ch1','aemexp2_ch2','aemexp2_ch3','aemexp2_ch4'])

        output = {}
        for scan in scans:
            output[prefix+f'{scan}'] = xr.Dataset({
                'RMU':xr.DataArray(self._xas[prefix+f'{scan}']['aemexp2_ch1'],dims=['Photon Energy'],coords={'Photon Energy':self._xas[prefix+f'{scan}']['beamline_energy']}),
                'TFY':xr.DataArray(self._xas[prefix+f'{scan}']['aemexp2_ch2'],dims=['Photon Energy'],coords={'Photon Energy':self._xas[prefix+f'{scan}']['beamline_energy']}),
                'TEY':xr.DataArray(self._xas[prefix+f'{scan}']['aemexp2_ch2'],dims=['Photon Energy'],coords={'Photon Energy':self._xas[prefix+f'{scan}']['beamline_energy']}),
                })
        return output

    def load_mesh(self, filename, scans):
        """
        load xas data

        return RMU,TFY,TEY
        """
        if isinstance(scans, int):
            scans = [scans]

        # find prefix
        prefix = 'entry'
        new_scans = []
        for scan in scans:
            if prefix+f'{scan}' in self._entry:
                pass
            else:
                new_scans.append(prefix+f'{scan}')

        if len(new_scans) == 0:
            pass
        else:
            file = self.data_folder + '/' + filename
            self.load_entry(file,new_scans,['a_mp1_x','a_mp1_y','aemexp2_ch1','aemexp2_ch2','aemexp2_ch3','aemexp2_ch4'])

        output = {}
        for scan in scans:
            temp1 = self._xas[prefix+f'{scan}']
            y_center,x_center, RMU, TFY, TEY = ADRESS().mesh(temp1['a_mp1_x'],temp1['a_mp1_y'],temp1['aemexp2_ch1'],temp1['aemexp2_ch2'],temp1['aemexp2_ch3'])
            temp2 = {
                'RMU':xr.DataArray(RMU, dims=['y', 'x'], coords={'x': x_center, 'y':y_center}),
                'TFY':xr.DataArray(TFY, dims=['y', 'x'], coords={'x': x_center, 'y':y_center}),
                'TEY':xr.DataArray(TEY, dims=['y', 'x'], coords={'x': x_center, 'y':y_center}),
            }
            output[prefix+f'{scan}'] = xr.Dataset(temp2)
        return output

    
    def load_rixs(self, filename, scans):
        """
        load xas data

        return Emission energy, RIXS
        """
        if isinstance(scans, int):
            scans = [scans]

        # find prefix
        prefix = 'acq'
        new_scans = []
        for scan in scans:
            if prefix+f'{scan}' in self._acq:
                pass
            else:
                new_scans.append(prefix+f'{scan}')

        if len(new_scans) == 0:
            pass
        else:
            file = self.data_folder + '/' + filename
            self.load_acq(file,new_scans)

        output = {}
        for scan in scans:
            output[prefix+f'{scan}'] = xr.Dataset({'RIXS':xr.DataArray(self._rixs[prefix+f'{scan}']['rixs'], dims=['Emission energy'], coords={'Emission energy': self._rixs[prefix+f'{scan}']['emission']})})

        return output

    def load_ascan(self, filename, scans, motor='beamline_energy'):
        """
        load xas data

        return RMU,TFY,TEY
        """
        if isinstance(scans, int):
            scans = [scans]

        # find prefix
        prefix = 'entry'
        new_scans = []
        for scan in scans:
            if prefix+f'{scan}' in self._entry:
                pass
            else:
                new_scans.append(prefix+f'{scan}')

        if len(new_scans) == 0:
            pass
        else:
            file = self.data_folder + '/' + filename
            self.load_entry(file,new_scans,[motor,'aemexp2_ch1','aemexp2_ch2','aemexp2_ch3','aemexp2_ch4'])

        output = {}
        for scan in scans:
            output[prefix+f'{scan}'] = xr.Dataset({
                'RMU':xr.DataArray(self._xas[prefix+f'{scan}']['aemexp2_ch1'],dims=[motor],coords={motor:self._xas[prefix+f'{scan}'][motor]}),
                'TFY':xr.DataArray(self._xas[prefix+f'{scan}']['aemexp2_ch2'],dims=[motor],coords={motor:self._xas[prefix+f'{scan}'][motor]}),
                'TEY':xr.DataArray(self._xas[prefix+f'{scan}']['aemexp2_ch2'],dims=[motor],coords={motor:self._xas[prefix+f'{scan}'][motor]}),
                })
        return output

    def save_runtable(self,filename,scans):
        """
        save meta data
        """
        if isinstance(scans, int):
            scans = [scans]

        # find prefix
        prefix = 'acq'
        new_scans = []
        for scan in scans:
            if prefix+f'{scan}' in self._acq:
                pass
            else:
                new_scans.append(prefix+f'{scan}')

        if len(new_scans) == 0:
            pass
        else:
            file = self.data_folder + '/' + filename
            self.load_acq(file,new_scans)

        output = {}
        for scan in scans:
            output[prefix+f'{scan}'] = self._meta[prefix+f'{scan}']

        df = pd.DataFrame.from_dict(output,orient='index')
        df.to_csv('RunTable.csv')

        return df

    def plot_lines(self,dataset,x='beamline_energy',y='TEY'):
        # output_file(filename="bokeh_plot.html", title="")
        TOOLTIPS = [("x", "$x"),("y", "$y")]
        p = figure(width = 600,height = 400,
                   tools='pan,box_zoom,wheel_zoom,reset,save,crosshair,hover', tooltips=TOOLTIPS,
                  x_axis_label =x,y_axis_label =y)
        colors = cycle(["#0072BD", "#D95319", "#EDB120", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F"])
        for key in dataset:
            p.line(dataset[key][x], dataset[key][y],legend_label=key,color=next(colors))
        p.legend.click_policy="hide"
        # show(p)
        # save(p)
        return p

    def plot_image(self,dataarray,x='x',y='y'):
        # output_file(filename="bokeh_plot.html", title="")
        TOOLTIPS = [("x", "$x"),("y", "$y")]
        p = figure(width = 600,height = 400,
                   tools='pan,box_zoom,wheel_zoom,reset,save,crosshair,hover', tooltips=TOOLTIPS,
                  x_axis_label ='x (mm)',y_axis_label ='y (mm)')
        p.image(image=[dataarray.values],
                dw=dataarray.coords[x].diff(dim=x).mean().item(), 
                dh=dataarray.coords[y].diff(dim=y).mean().item(), 
                y=dataarray.coords[y][0].item(), 
                x=dataarray.coords[x][0].item(),
                palette="Turbo256",level="image")
        p.y_range.flipped = True
        # show(p)
        # save(p)
        return p
        


    