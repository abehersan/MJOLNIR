import sys 
sys.path.append('/home/lass/Dropbox/PhD/Software/MJOLNIR/')

from Tutorial_Class import Tutorial


def Tester():
        from MJOLNIR.Data import DataSet
        from MJOLNIR import _tools 
        import numpy as np
        import matplotlib.pyplot as plt
        
        numbers = '483-489,494-500' 
        fileList = _tools.fileListGenerator(numbers,'/home/lass/Dropbox/PhD/CAMEAData/',2018) 
        
        ds = DataSet.DataSet(fileList)
        ds.convertDataFile(saveFile=False)
        
        # Define the positions to be cut through
        Q1 = np.array([0,0,0])
        Q2 = np.array([0,0,1])
        Q3 = np.array([-1,0,1])
        Q4 = np.array([-1,0,-1])
        # Collect them into one array
        QPoints = np.array([Q1,Q2,Q3,Q4])
        
        # Define orthogonal width and minimum pixel size along Q-cut
        width = np.array([0.05,0.03,0.05]) # 1/AA
        minPixel = np.array([0.03,0.01,0.01]) # 1/AA
        
        # Define energy bins through the binEdges methods found in _tools
        Energies = np.concatenate(ds.energy,axis=0)
        EnergyBins = np.array([_tools.binEdges(Energies,0.04),
                               _tools.binEdges(Energies,0.1),
                               _tools.binEdges(Energies,0.07)])
        
        
        ax,DataLists,BinListTotal = \
        ds.plotCutQELine(QPoints=QPoints, width=width, minPixel=minPixel, \
                         EnergyBins=EnergyBins, ticks = 12,\
                         vmin=1e-8, vmax=1e-5, plotSeperator = True,
                         seperatorWidth=0.5,zorder=10)
        ax.grid(True,zorder=0,c='k')
        ax.get_figure().savefig('/home/lass/Dropbox/PhD/Software/MJOLNIR/docs/Tutorials/Advanced/plotCutQELineMnF2.png',format='png',dpi=300)
        
        # Plot a single cut through the data set
        
        fig2,ax2 = plt.subplots()
        segID = 2
        # Extract the data from SegmentId
        df = DataLists[segID]
        
        for energy,EnergyDF in df.groupby('Energy'):    
                    
            Intensity = EnergyDF['Int']*1e5
            Intensity_err = EnergyDF['Int_err']
            
            position = EnergyDF['L'] # Plotting along L
            
            ax2.errorbar(position,Intensity,yerr=Intensity_err,fmt='-',label='E = {:.1f} meV'.format(energy))
            
        ax2.set_title('Cut through data along $L$')
        ax2.set_xlabel('L [rlu]')
        ax2.set_ylabel('Int [arb]')
        ax2.legend()
        ax2.grid(True)
        fig2.tight_layout()
        fig2.savefig('/home/lass/Dropbox/PhD/Software/MJOLNIR/docs/Tutorials/Advanced/plotCutQELineMnF21D.png',format='png',dpi=300)
    
    
title = 'Advanced QE-cutting'

introText = 'With the simple show casing of the plotCutQELine in the `Simple plotCutQELine <../Quick/plotCutQELine.html>`_ '\
+'tutorial the next step is to make use of all of the functionality of the method. That is, when performing cuts along different'\
+' :math:`\\vec{Q}` directions one might want different integration widths orthogonal to the direction, different bin sizes along '\
+':math:`\\vec{Q}`, and different energy bins. All of this is possible through the use of kwargs.'

outroText = 'Running the above code results in the following figure: '\
+'\n\n'\
+'.. figure:: plotCutQELineMnF2.png\n  :width: 95%\n  :align: center\n\n'\
+'\n\nMany different kwargs are possible for the cutting method and most of them should make obvious sense, '\
+'but below is a table of arguments, their default value and their action for the plot. \n\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|      Kwarg     | Action                                                                          | Default Value  | Unit |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|      width     | Define the integration width orthogonal to cut direction                        | 0.1            | 1/AA |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|    minPixel    | Minimal possible bin size along cut (using _tools.binEdges)                     | 0.01           | 1/AA |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|       rlu      | Whether to use RLU or instrument positions                                      | True           | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|       fig      | Figure into which the axis is created                                           | None           | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|    dataFiles   | List of converted data files to be used                                         | None           | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|      vmin      | Minimal value used for the coluor scale                                         | min(Intensity) | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|      vmax      | Maximal value used for the coluor scale                                         | max(Intensity) | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|       log      | If the logarithm to the intensity is to be plotted (+1e-20)                     | False          | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|      ticks     | The number of tick marks to be plotted, minimum is len(QPoints)                 | 8              | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'| seperatorWidth | Width of vertical line denoting change of cutting direction                     | 2              | pts  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|  plotSeperator | If a vertical black line is to be plotted to denote change of cutting direction | True           | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n'\
+'|   \*\*kwargs   | Additional kwargs are passed on to the pcolormesh method of Matplotlib          | None           | N/A  |\n'\
+'+----------------+---------------------------------------------------------------------------------+----------------+------+\n\n'\
+'Working with return data\n'+24*'-'+'\n\n'\
+'Having created the plot as wanted, the natural next step is to look at the actual data return from the method. This data is exactly '\
+'the same as what would have been returned by utilizing the non-plotting version cutQELine with the same arguments '\
+'(except for plotting specifics). Of most interest are the DataList, BinListTotal, and centerPositionTotal, containing the '\
+'position/intensity of the cuts, and binning counts as function of segment and bin, as well as the edges and centers of these bins. '\
+'That is, DataList is a pandas DataFrame with columns containing "H", "K", "L", "Energy", "Qx", "Qy", "Intensity"  (neutron count), '\
+'"Int" (noralized intensity), "BinCount" (neutron positions binned in single pixel), "Normalization", "Monitor". '\
+'As an example, the normalized intensities as function of :math:`L` for the third segment at five different energies are plotted. \n\n'\
+'.. figure:: plotCutQELineMnF21D.png\n  :width: 65%\n  :align: center\n\n'\
+'Each energy is shifted by 1 for clarity. As the intensity of the signal is a combination of many different aspects an overall factor of '\
+'1e5 is multiplied to it as to ensure that the numbers are in a reasonable range. In the data the instrumental in-focus and out-of-focus '\
+'effects are visible as the peak at positive :math:`L` are a lot sharper and narrower than the ones at negative :math:`L`. '\
+'This is as expected from a standard measurement. '


introText = title+'\n'+'^'*len(title)+'\n'+introText


    
Example = Tutorial('plotCutQELine',introText,outroText,Tester,fileLocation = '/home/lass/Dropbox/PhD/Software/MJOLNIR/docs/Tutorials/Advanced')

def test_plotCutQELine():
    Example.test()

if True:
    Example.generateTutorial()
else:
    print(outroText)
