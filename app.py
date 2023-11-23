import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
# Create fuzzy variables
wbc = ctrl.Antecedent(np.arange(0, 150001, 1), 'wbc')
rbc = ctrl.Antecedent(np.arange(0, 4.8, 0.1), 'rbc')
platelets = ctrl.Antecedent(np.arange(0, 410001, 1), 'platelets')
diagnosis = ctrl.Consequent(np.arange(0, 141, 1), 'diagnosis')

wbc['low'] = fuzz.gaussmf(wbc.universe, 2000, 1000)
wbc['normal'] = fuzz.gaussmf(wbc.universe, 7000, 1500)
wbc['medium'] = fuzz.gaussmf(wbc.universe, 30000, 10000)
wbc['high'] = fuzz.gaussmf(wbc.universe, 100000, 25000)

rbc['low'] = fuzz.gaussmf(rbc.universe, 1.85, 0.925)
rbc['normal'] = fuzz.gaussmf(rbc.universe, 4.25, 0.275)

platelets['low'] = fuzz.gaussmf(platelets.universe, 75000, 37500)
platelets['normal'] = fuzz.gaussmf(platelets.universe, 225000, 37500)

diagnosis['normal'] = fuzz.gaussmf(diagnosis.universe, 0, 5)
diagnosis['leukemia'] = fuzz.gaussmf(diagnosis.universe, 20, 5)
diagnosis['Pancytopenia'] = fuzz.gaussmf(diagnosis.universe, 40, 5)
diagnosis['Malaria'] = fuzz.gaussmf(diagnosis.universe, 60, 5)
diagnosis['Typhoid'] = fuzz.gaussmf(diagnosis.universe, 80, 5)
diagnosis['Dengue'] = fuzz.gaussmf(diagnosis.universe, 100, 5)
diagnosis['Mild Infection'] = fuzz.gaussmf(diagnosis.universe, 120, 5)

# Define rules
rule1 = ctrl.Rule(wbc['normal'] & rbc['normal'] & platelets['normal'], diagnosis['normal'])
rule2 = ctrl.Rule(wbc['high'] & rbc['low'] & platelets['low'], diagnosis['leukemia'])
rule3 = ctrl.Rule(wbc['low'] & rbc['low'] & platelets['low'], diagnosis['Pancytopenia'])
rule4 = ctrl.Rule(wbc['normal'] & rbc['low'] & platelets['normal'], diagnosis['Malaria'])
rule5 = ctrl.Rule(wbc['medium'] & rbc['normal'] & platelets['normal'], diagnosis['Typhoid'])
rule6 = ctrl.Rule(wbc['normal'] & rbc['normal'] & platelets['low'], diagnosis['Dengue'])

rule7 = ctrl.Rule(wbc['low'] & rbc['low'] & platelets['normal'], diagnosis['Mild Infection'])
rule8 = ctrl.Rule(wbc['low'] & rbc['normal'] & platelets['low'], diagnosis['Mild Infection'])
rule9 = ctrl.Rule(wbc['low'] & rbc['normal'] & platelets['normal'], diagnosis['Mild Infection'])

rule10 = ctrl.Rule(wbc['high'] & rbc['low'] & platelets['normal'], diagnosis['Mild Infection'])
rule11 = ctrl.Rule(wbc['high'] & rbc['normal'] & platelets['low'], diagnosis['Mild Infection'])
rule12 = ctrl.Rule(wbc['high'] & rbc['normal'] & platelets['normal'], diagnosis['Mild Infection'])

rule13 = ctrl.Rule(wbc['normal'] & rbc['low'] & platelets['low'], diagnosis['Mild Infection'])


rule14 = ctrl.Rule(wbc['medium'] & rbc['low'] & platelets['low'], diagnosis['Mild Infection'])
rule15 = ctrl.Rule(wbc['medium'] & rbc['low'] & platelets['normal'], diagnosis['Mild Infection'])
rule16 = ctrl.Rule(wbc['medium'] & rbc['normal'] & platelets['low'], diagnosis['Mild Infection'])

diagnosis_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16])
diagnosis_sim = ctrl.ControlSystemSimulation(diagnosis_ctrl)


st.title("Disease Diagnosis using Fuzzy Logic")

# User input
wbc_value = st.slider("White Blood Cell Count (WBC)", min_value=0, max_value=150000, value=1)
rbc_value = st.slider("Red Blood Cell Count (RBC)", min_value=1.0, max_value=4.8, value=0.0)
platelets_value = st.slider("Platelet Count", min_value=0, max_value=410000, value=1)

# Dengue, Malaria, Typhoid status
dengue_status = st.checkbox("Dengue (Positive/Negative)")
malaria_status = st.checkbox("Malaria (Positive/Negative)")
typhoid_status = st.checkbox("Typhoid (Positive/Negative)")

# Pass input values to the fuzzy system
diagnosis_sim.input['wbc'] = wbc_value
diagnosis_sim.input['rbc'] = rbc_value
diagnosis_sim.input['platelets'] = platelets_value

# Crunch the numbers
diagnosis_sim.compute()

# Get the result
result = diagnosis_sim.output['diagnosis']
max_activation = max(diagnosis_sim.output.items(), key=lambda x: x[1])
result_label = max_activation[0]

# Crunch the numbers
diagnosis_sim.compute()

# Find the term with the highest activation
max_activation = max(diagnosis_sim.output.items(), key=lambda x: x[1])
result_label = max_activation[0]

x = diagnosis_sim.output['diagnosis']
# Display the result in Streamlit GUI
st.subheader("Diagnosis Result:")
st.write(f"The fuzzy diagnosis is: {diagnosis_sim.output['diagnosis']:.2f}")

# Display the result in Streamlit GUI
st.subheader("Diagnosis Result:")

if 0 < x < 20:
    st.write("Normal Condition.")

elif 15 < x < 40:
    st.write("Leukemia is Positive.")

elif 35 < x < 60:
    st.write("Pancytopenia is Positive.")

elif 55 < x < 80:
    st.write("Chances of Malaria, Please check the Malaria box after taking the Malaria test.")
    if malaria_status:
        st.write("Malaria is Positive.")

elif 75 < x < 100:
    st.write("Chances of Typhoid, Please check the typhoid box after taking the typhoid test.")
    if malaria_status:
        st.write("Typhoid is Positive.")

elif 95 < x < 115:
    st.write("Chances of Dengue, Please check the dengue box after taking the dengue test.")
    if dengue_status:
        st.write("Dengue is Positive.")

else:
    st.write("Mild Infection. Once consult doctor for further diagnosis.")

