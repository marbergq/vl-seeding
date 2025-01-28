import streamlit as st

def time_to_seconds(hours, minutes, seconds):
    return hours*3600 + minutes*60 + seconds

def calculate_seeding(winner_time, given_time):
    if winner_time <= 0:
        return "Error: Vinnartiden kan inte vara noll"
    
    ratio = given_time / winner_time
    ratio = round(ratio, 2)
    
    if ratio <= 1.0:
        return "Elit", ratio
    elif 1.0 < ratio <= 1.15:
        return "1", ratio
    elif 1.15 < ratio <= 1.25:
        return "2", ratio
    elif 1.25 < ratio <= 1.40:
        return "3", ratio
    elif 1.40 < ratio <= 1.55:
        return "4", ratio
    elif 1.55 < ratio <= 1.70:
        return "5", ratio
    elif 1.70 < ratio <= 1.85:
        return "6", ratio
    elif 1.85 < ratio <= 2.00:
        return "7", ratio
    elif 2.00 < ratio <= 2.30:
        return "8", ratio
    else:
        return "9", ratio

st.title("Vasaloppet Seedningsberäknare 🎿")

# Input sektion
col1, col2 = st.columns(2)
with col1:
    st.header("Vinnartid")
    win_h = st.number_input("Timmar (vinnare)", min_value=0, value=2)
    win_m = st.number_input("Minuter (vinnare)", min_value=0, value=0)
    win_s = st.number_input("Sekunder (vinnare)", min_value=0, value=0)

with col2:
    st.header("Att utvärdera")
    eval_h = st.number_input("Timmar (utvärdera)", min_value=0, value=2)
    eval_m = st.number_input("Minuter (utvärdera)", min_value=0, value=30)
    eval_s = st.number_input("Sekunder (utvärdera)", min_value=0, value=0)

distance = st.number_input("Loppets längd (km)", min_value=10, value=42)

# Beräkning
if st.button("Beräkna seedning"):
    winner_seconds = time_to_seconds(win_h, win_m, win_s)
    eval_seconds = time_to_seconds(eval_h, eval_m, eval_s)
    
    if winner_seconds == 0:
        st.error("Vinnartiden kan inte vara noll!")
    else:
        seeding, ratio = calculate_seeding(winner_seconds, eval_seconds)
        st.success(f"**Seedningsgrupp**: {seeding}")
        st.info(f"**Tidsratio**: {ratio}")
        
        # Förklaring
        st.markdown("### Förklaring")
        st.write(f"Din tid är {ratio:.2f}x vinnarens tid på {distance} km.")
        st.write("""
        **Seedningsgränser**:
        - Elit: ≤ 1.00x
        - 1: 1.01-1.15x
        - 2: 1.16-1.25x  
        - 3: 1.26-1.40x
        - 4: 1.41-1.55x
        - 5: 1.56-1.70x
        - 6: 1.71-1.85x
        - 7: 1.86-2.00x
        - 8: 2.01-2.30x
        - 9: > 2.30x
        """)

st.markdown("---")
st.caption("Baserat på seedningsdata från Vasaloppet 2025. Gränser kan variera något mellan olika lopp.")