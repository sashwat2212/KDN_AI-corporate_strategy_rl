import streamlit as st
import numpy as np
import pandas as pd
import os

st.title("📈 Agentic AI for Corporate Strategy")


data = [
    (0,  [349, 228, 171, 195, 209], [-910, -670, -390, -650, -810]),
    (100, [296, 256, 262, 162, 334], [-1040, -340, -830, -380, -510]),
    (200, [341, 271, 449, 372, 417], [-690, -940, -1610, -1530, -1480]),
    (300, [378, 343, 407, 432, 462], [-1020, -1270, -1380, -1730, -1880]),
    (400, [466, 471, 468, 457, 489], [-1540, -1490, -1270, -1180, -1410]),
    (500, [458, 497, 470, 452, 465], [-1170, -1480, -1300, -1130, -1750]),
    (600, [461, 475, 467, 436, 497], [-1340, -1400, -1280, -1140, -1480]),
    (700, [497, 467, 451, 471, 500], [-1830, -1530, -1140, -1740, -1500]),
    (800, [453, 500, 447, 432, 475], [-1170, -1500, -1130, -1130, -1400]),
    (900, [448, 500, 467, 449, 500], [-1220, -1500, -1280, -1160, -1500]),
]


df = pd.DataFrame(
    [(ep, *rwd, *cap) for ep, rwd, cap in data],  
    columns=["Episode", "R1", "R2", "R3", "R4", "R5", "C1", "C2", "C3", "C4", "C5"]
)


st.subheader("📊 Episode-wise Rewards and Capital")
st.dataframe(df.style.format(precision=2), use_container_width=True)


output_dir = "output"
st.subheader("📈 Performance Over Time")

def display_image(image_path, caption):
    if os.path.exists(image_path):
        st.image(image_path, caption=caption, use_container_width=True)

display_image(os.path.join(output_dir, "agent_performance.png"), "📌 Agent Performance over Episodes")
display_image(os.path.join(output_dir, "capital_growth.png"), "💰 Capital Growth Over Episodes")
display_image(os.path.join(output_dir, "market_share.png"), "📉 Market Share Over Episodes")
