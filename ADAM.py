
import streamlit as st
import pandas as pd
from pickle import load
import pickle
import numpy as np
import math as m
from PIL import Image
import os
from glob import glob
#import matplotlib.pyplot as plt

st.header("Shaft Fracture")

st.subheader('Dimensional Parameters')
htp="https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png"
st.image(htp, caption= "Fig. 1: Schematic illustration of the geometry of a typical corrosion defect.")

st.sidebar.header('User Input Parameters')

def user_input_features():
    motor_power = st.sidebar.number_input('Motor Power, P (Watt)', value = 0.01)
    rotation = st.sidebar.number_input('No. of rotation per second, f (rps)', value = 0.01)
    shaft_diameter = st.sidebar.number_input('Shaft diameter, D (mm)', value = 0.01)
    vickers_hardness = st.sidebar.number_input('Vickers hardness, HV (kgf/mm^2)', value = 0.01)
    cf_load = st.sidebar.number_input('Load correction factor, C load ', value = 0.01)
    cf_size = st.sidebar.number_input('Size correction factor, C size ', value = 0.01)
    cf_surf = st.sidebar.number_input('Surface finishing correction factor, C surf ', value = 0.01)
    cf_temp = st.sidebar.number_input('Temperature correction factor, C temp ', value = 0.01)
    cf_reliab = st.sidebar.number_input('Reliable correction factor, C reliab ', value = 0.01)
    cf_notch = st.sidebar.number_input('Notch correction factor, C notch ', value = 0.01)
    stress_conc = st.sidebar.number_input('Stress-Concentration Factor, Kf ', value = 0.01)
    
    notchroot_radius = st.sidebar.number_input('Notch root radius, r (mm)', value = 0.01)
    characteristic_length = st.sidebar.number_input('Characteristic length, p (mm)', value = 0.01)

    data = {'P (Watt)': motor_power,
            'f (rps)': rotation,
            'D (mm)': shaft_diameter,
            'HV (kgf/mm^2)': vickers_hardness,
            'C load' : cf_load,
            'C size' :  cf_size,
            'C surf' : cf_surf,
            'C temp' : cf_temp,
            'C reliab' : cf_reliab,
            'C notch' :cf_notch,
            'Kt' : stress_conc,
            'r (mm)': notchroot_radius,  
            'p (mm)': characteristic_length,
            #'Sy (MPa)': Sy,
            #'Pop_Max (MPa)': Maximum_Operating_Pressure,
            #'Pop_Min (MPa)': Minimum_Operating_Pressure}
           }
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

p=df['P (Watt)'].values.item()
f=df['f (rps)'].values.item()
d=df['D (mm)'].values.item()
hv=df['HV (kgf/mm^2)'].values.item()
cl=df['C load'].values.item()
csi=df['C size'].values.item()
csu=df['C surf'].values.item()
ct=df['C temp'].values.item()
cr=df['C reliab'].values.item()
cn=df['C notch'].values.item()
kt=df['Kt'].values.item()
r=df['r (mm)'].values.item()
p=df['p (mm)'].values.item()


st.subheader('Nomenclature')
st.write('t is the pipe thickness; D is the pipe diameter; L is the pipe length (i.e., by default = 1000 mm); Lc is the corrosion length; Dc is the corrosion depth; Sy is the pipe material yield stress; UTS is the pipe material Ultimate Tensile Strength.')

# Calculate Torsional loading
T = p/(2*m.pi*f)

# Calculate burst pressure of intact pipe P Tresca
τ = (16*T)/(m.pi*d^3)

# Calculate burst pressure of corroded pipe P ASME B31G (2013)
M = m.sqrt(1+0.8*(L/(m.sqrt(D*t)))) #Folias factor

if L < m.sqrt(20*D*t):
    P_ASME_B31G = (2*t*UTS/D)*(1-(2/3)*(Dc/t)/1-(2/3)*(Dc/t)/M)

elif L > m.sqrt(20*D*t):
    P_ASME_B31G = (2*t*UTS/D)*(1-(Dc/t))

# Calculate burst pressure of corroded pipe PDnV
Q = m.sqrt(1+0.31*(Lc)**2/D*t) #Q is the curved fit of FEA results
P_DnV = (2*UTS*t/D-t)*((1-(Dc/t))/(1-(Dc/(t*Q))))

# Calculate burst pressure of corroded pipe P PCORRC Model 
P_PCORRC = (2*t*UTS/D)*(1-Dc/t)

user_input={'P (Watt)': "{:.2f}".format(P),
            'f (rps)': "{:.2f}".format(f),
            'D (mm)': "{:.2f}".format(D),
            'HV (kgf/mm^2)': "{:.2f}".format(hv),
            'C load': "{:.2f}".format(cl),
            'C size': "{:.2f}".format(csi),
            'C surf': "{:.2f}".format(csu),
            'C temp': "{:.2f}".format(ct),
            'C reliab': "{:.2f}".format(cr),
            'C notch': "{:.2f}".format(cn),
            'Kt': "{:.2f}".format(kt),
            'r (mm)': "{:.2f}".format(r),
            'p (mm)' : "{:.2f}".format(p)}
user_input_df=pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)

# Intact Pipe
calculated_param={'Pvm (MPa)': "{:.2f}".format(Pvm)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Intact Pipe Burst Pressure via Von Mises')
st.write(calculated_param_df)

calculated_param={'PTresca (MPa)': "{:.2f}".format(PTresca)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Intact Pipe Burst Pressure via Tresca')
st.write(calculated_param_df)

# Corroded Pipe
calculated_param={'P_ASME_B31G (MPa)': "{:.2f}".format(P_ASME_B31G)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corroded Pipe Burst Pressure via ASME_B31G')
st.write(calculated_param_df)

calculated_param={'P_DnV (MPa)': "{:.2f}".format(P_DnV)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via DnV')
st.write(calculated_param_df)

calculated_param={'P_PCORRC (MPa)': "{:.2f}".format(P_PCORRC)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via PCORRC')
st.write(calculated_param_df)

Pressure = [Pvm, PTresca, P_ASME_B31G, P_DnV, P_PCORRC]
index = ["Pvm (MPa)", "PTresca (MPa)", "P_ASME_B31G (MPa)", "P_DnV (MPa)", "P_PCORRC (MPa)"]
df = pd.DataFrame({"Burst Pressure (MPa)": Pressure}, index=index)

#st.pyplot(df.plot.barh(stacked=True).figure)

# Principle stresses for Maximum Operating Pressure
P1max = Pop_Max*D/(2*t)
P2max = Pop_Max*D/(4*t)
P3max = 0

# Principle stresses for Minimum Operating Pressure
P1min = Pop_Min*D/(2*t)
P2min = Pop_Min*D/(4*t)
P3min = 0

# VM stress Max and Min Operating Pressure
Sigma_VM_Pipe_Max_Operating_Pressure = (1/m.sqrt(2))*((P1max-P2max)**2+(P2max-P3max)**2+(P3max-P1max)**2)**0.5

Sigma_VM_Pipe_Min_Operating_Pressure = 1/m.sqrt(2)*m.sqrt((P1min-P2min)**2+(P2min-P3min)**2+(P3min-P1min)**2)

calculated_param={'Sigma_VM_Pipe_Max_Operating_Pressure (MPa)': "{:.2f}".format(Sigma_VM_Pipe_Max_Operating_Pressure)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Von Mises stress of Maximum Operating Pressure')
st.write(calculated_param_df)

calculated_param={'Sigma_VM_Pipe_Min_Operating_Pressure (MPa)': "{:.2f}".format(Sigma_VM_Pipe_Min_Operating_Pressure)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Von Mises stress of Minimum Operating Pressure')
st.write(calculated_param_df)

Stresses = [Sigma_VM_Pipe_Max_Operating_Pressure, Sigma_VM_Pipe_Min_Operating_Pressure, Sy, UTS]
index = ["Svm_Max (MPa)", "Svm_Min (MPa)", "Yield Stress (MPa)", "UTS (MPa)"]
df = pd.DataFrame({"Stresses (MPa)": Stresses}, index=index)

#st.pyplot(df.plot.barh(color={"Stresses (MPa)": "red"}, stacked=True).figure)

st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assesment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
