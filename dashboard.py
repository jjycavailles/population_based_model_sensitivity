import ipywidgets as widgets
from ipywidgets import Layout
from io import BytesIO
import colorsys
import pickle # package use to save data
from IPython.display import display, Image
import nbinteract as nbi

import numpy as np

#pip3 install matplotlib -qqq
#import pip
#pip._internal.main(['install', matplotlib])
#import matplotlib.pyplot as plt


from population import *

class Select_box(widgets.VBox):
    def __init__(self, dashboard):
        
        import numpy as np
        
        self.dashboard = dashboard


        #initial point

        self.selection_ia0 = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(1000), description = "N_{ia}^0", value =  1./3)
        self.selection_ia0.observe(dashboard.on_ia0_selected, names = "value")
        
        self.selection_ib0 = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(1000), description = "N_{ib}^0", value =  1./3)
        self.selection_ib0.observe(dashboard.on_ib0_selected, names = "value")
        
        self.selection_sab0 = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(1000), description = "N_{sab}^0", value =  1./3)
        self.selection_sab0.observe(dashboard.on_sab0_selected, names = "value")
        
        self.selection_l = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(100), description = "l ", value =  0.6)
        self.selection_l.observe(dashboard.on_l_selected, names = "value")

        self.selection_h = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(100), description = "h ", value =  2)
        self.selection_h.observe(dashboard.on_h_selected, names = "value")
        
        self.selection_alpha = widgets.FloatSlider(min = 0, max = 1, description = "alpha", value = 0.6)
        self.selection_alpha.observe(dashboard.on_alpha_selected, names = "value")
        
        
        self.selection_r = widgets.FloatSlider(min = 0, max = 4, description = "r", value = 3)
        self.selection_r.observe(dashboard.on_r_selected, names = "value")
        
        self.selection_m = widgets.FloatSlider(min = 0, max = 4, description = "m", value = 2)
        self.selection_m.observe(dashboard.on_m_selected, names = "value")
        
        self.selection_d = widgets.FloatSlider(min = 0, max = 1, description = "d", value = 0.4)
        self.selection_d.observe(dashboard.on_d_selected, names = "value")
        
        self.selection_k = widgets.FloatLogSlider(min = np.log10(1), max = np.log10(100000), description = "K", value =  1000)
        self.selection_k.observe(dashboard.on_k_selected, names = "value")
   

        self.selection_tFinal = widgets.FloatLogSlider(min = np.log10(10), max = np.log10(10000), description = "final time", value =  10)
        self.selection_tFinal.observe(dashboard.on_tFinal_selected, names = "value")
        
        self.selection_nbreStep = widgets.IntSlider(min = 100, max = 100000, description = "number of step", value =  100)
        self.selection_nbreStep.observe(dashboard.on_nbreStep_selected, names = "value")
        
        self.selection_period = widgets.IntSlider(min = 1, max = 100, description = "period", value = 5)
        self.selection_period.observe(dashboard.on_period_selected, names = "value")
            
        
        
        children = [
        self.selection_ia0,
        self.selection_ib0,
        self.selection_sab0,
        self.selection_l,
        self.selection_h,
        self.selection_alpha,
        self.selection_r,
        self.selection_m,
        self.selection_d,
        self.selection_k,
        self.selection_tFinal,
        self.selection_nbreStep,
        self.selection_period,
        ]
        super().__init__(children, layout=Layout(width="100%"))   

class Image_box(widgets.Box):
    def __init__(self, dashboard):
        #%pip install matplotlib
        #import matplotlib.pyplot as plt
        self.image = widgets.Image()
        self.dashboard = dashboard
        
        self.ia0 = self.dashboard.ia0
        self.ib0 = self.dashboard.ib0
        self.sab0 = self.dashboard.sab0
        
        self.l = self.dashboard.l
        self.h = self.dashboard.h
        self.alpha = self.dashboard.alpha
  
        self.r = self.dashboard.r
        self.m = self.dashboard.m
        self.d = self.dashboard.d
        self.k = self.dashboard.k
        
        self.tFinal = self.dashboard.tFinal
        self.nbreStep = self.dashboard.nbreStep
        self.period = self.dashboard.period
        
        #self.t_final = self.dashboard.tFinal
        #self.period_variable_source = self.dashboard.period
        
        
        self.print_image()
        
        image_container = widgets.Box([self.image], layout=Layout(width="100%"))
        
        children = [
   #     image_container,
        self.image,   
        ]
        super().__init__(children, layout=Layout(width="100%"))
        
    def print_image(self):
        #"""
        try:
            import matplotlib.pyplot as plt
        except:
			         import pip
			         pip._internal.main(['install', matplotlib])
            #%pip install matplotlib -qqq
            import matplotlib.pyplot as plt
        #"""
        
        self.t_final = self.tFinal
        self.period_variable_source = self.period
        
        
        T = np.linspace(0, self.t_final, self.nbreStep)
        Random_series_simple = np.random.binomial(1, self.alpha, size = self.nbreStep//self.period_variable_source) # generate again only if alpha changes
        Random_series = np.zeros(self.nbreStep)
        #for i in range(self.period_variable_source):
        #    Random_series[i::self.period_variable_source] = Random_series_simple
        for i in range(len(Random_series_simple)):
            Random_series[i*self.period_variable_source:i*self.period_variable_source+self.period_variable_source:] = Random_series_simple[i]

            
        XXb = self.l + (self.h-self.l)*Random_series

        SS = iterations(T, [self.ia0, self.ib0, self.sab0], XXb, self.l, self.h, self.alpha, self.r, self.m, self.d, self.k)

        Theory = np.array([1./(1+self.h), self.l/(1+self.l), (self.h-self.l)/((1+self.l)*(1+self.h))])

        plt.subplots(2,1, figsize = (15, 15))

        plt.subplot(2,1, 1)
        plt.title("Population model ODEs based on a simple Verhulst model", fontsize = 30)
        mmax = 1.1*np.max(np.max(SS))
        plt.fill_between(T, -0.1 , mmax, where=XXb==self.h, alpha = 0.2, color = "purple", label = "Xb = high")
        plt.fill_between(T, -0.1 , mmax, where=XXb==self.l, alpha = 0.2, color = "orange", label = "Xb = low")

        for i, strat in enumerate(Strat):
            plt.plot(T, SS[:,i], label = strat, color = Color[i])
        #    plt.plot([T[0], T[-1]], [Theory[i], Theory[i]], color = Color[i])
        #plt.ylim(0,1)
        plt.legend(fontsize = 20)
        plt.xlabel("time", fontsize = 30)
        plt.ylabel("Populations", fontsize = 30)

        plt.subplot(2,1, 2)
        plt.title("Population model ODEs based on a simple Verhulst model", fontsize = 30)
        for i, strat in enumerate(Strat):
            plt.plot(T, SS[:,i]/np.sum(SS, axis = 1), label = strat, color = Color[i])
            plt.plot([T[0], T[-1]], [Theory[i], Theory[i]], "--", color = Color[i])
        plt.fill_between(T, -0.1 , 1.1, where=XXb==self.h, alpha = 0.2, color = "purple", label = "Xb = high")
        plt.fill_between(T, -0.1 , 1.1, where=XXb==self.l, alpha = 0.2, color = "orange", label = "Xb = low")
        plt.ylim(-0.1,1.1)
        plt.legend(fontsize = 20)
        plt.xlabel("time", fontsize = 30)
        plt.ylabel("Frequency", fontsize = 30)
        plt.yticks([0, 1, 1./(1+self.h), self.l/(1+self.l), (self.h-self.l)/((1+self.l)*(1+self.h))], ["0", "1", "1./(1+h)", "l/(1+l)", "(h-l)/((1+l)*(1+h))"])


        #plt.show()


        image_file = BytesIO()
        #fig.savefig(fname = image_file)
        plt.savefig(fname = image_file)
        image_file.seek(0)
        image_data = image_file.read()
        self.image.value = image_data
#            self.image.width = 1500
#           self.image.height = 2000
        plt.close()

#          file = open(nom, "rb")
#         image = file.read()
        #plt.imshow(image)
#        self.image.value = image
 #       self.image.format = 'png'
        
        
        return
        

    def change_ia0(self, change):
        self.ia0 = change
        self.print_image()
        return
    
    def change_ib0(self, change):
        self.ib0 = change
        self.print_image()
        return
    
    def change_sab0(self, change):
        self.obl0 = change
        self.print_image()
        return
    
    def change_l(self, change):
        self.l = change
        self.print_image()
        return
    
    
    def change_h(self, change):
        self.h = change
        self.print_image()
        return
    
    def change_alpha(self, change):
        self.alpha = change
        self.print_image()
        return
    
    def change_r(self, change):
        self.r = change
        self.print_image()
        return
    
    
    def change_m(self, change):
        self.m = change
        self.print_image()
        return
    
    def change_d(self, change):
        self.d = change
        self.print_image()
        return
    
    def change_k(self, change):
        self.k = change
        self.print_image()
        return
    
    def change_tFinal(self, change):
        self.tFinal = change
        self.print_image()
        return
    
    def change_nbreStep(self, change):
        self.nbreStep = change
        self.print_image()
        return
    
    def change_period(self, change):
        self.period = change
        self.print_image()
        return

class Dashboard(widgets.VBox):
    def __init__(self):

        self.ia0 = 1./3
        self.ib0 = 1./3
        self.sab0 = 1./3
        
        self.l = 0.6
        self.h = 2
        self.alpha = 0.6
          
        self.r = 3
        self.m = 2
        self.d = 0.4
        self.k = 1000
        
        self.tFinal = 10
        self.nbreStep = 100
        self.period = 5
    
        self.select_box = Select_box(self)
    #    self.text_box = Text_box(self)
        self.image_box = Image_box(self)
        
        
        C1 = widgets.Box([self.image_box], layout=Layout(width="65%"))
        C2 = widgets.Box([self.select_box], layout=Layout(width="32%"))
        
        #rowA = widgets.Box([self.image_box, self.select_box], layout=Layout(width="100%"))
        rowA = widgets.HBox([C1, C2], layout=Layout(width="100%"))
        super().__init__([rowA], layout=Layout(width="100%"))
    

    
    
    def on_ia0_selected(self, change):
        self.ia0 = change["new"]
        self.image_box.change_ia0(change["new"])

    def on_ib0_selected(self, change):
        self.ib0 = change["new"]
        self.image_box.change_ib0(change["new"])

    def on_sab0_selected(self, change):
        self.sab0 = change["new"]
        self.image_box.change_sab0(change["new"])
        

    def on_l_selected(self, change):
        self.l = change["new"]
        self.image_box.change_l(change["new"])

    def on_h_selected(self, change):
        self.h = change["new"]
        self.image_box.change_h(change["new"])
        
    def on_alpha_selected(self, change):
        self.alpha = change["new"]
        self.image_box.change_alpha(change["new"])

        
    def on_r_selected(self, change):
        self.r = change["new"]
        self.image_box.change_r(change["new"])

    def on_m_selected(self, change):
        self.m = change["new"]
        self.image_box.change_m(change["new"])

    def on_d_selected(self, change):
        self.d = change["new"]
        self.image_box.change_d(change["new"])

    def on_k_selected(self, change):
        self.k = change["new"]
        self.image_box.change_k(change["new"])
        
    def on_tFinal_selected(self, change):
        self.tFinal = change["new"]
        self.image_box.change_tFinal(change["new"])
        
    def on_nbreStep_selected(self, change):
        self.nbreStep = change["new"]
        self.image_box.change_nbreStep(change["new"])
        
    def on_period_selected(self, change):
        self.period = change["new"]
        self.image_box.change_period(change["new"])
