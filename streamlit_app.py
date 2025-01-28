import streamlit as st

def time_to_seconds(hours, minutes, seconds):
    return hours*3600 + minutes*60 + seconds

def seconds_to_time(seconds):
    hours = seconds // 3600
    remaining = seconds % 3600
    minutes = remaining // 60
    seconds = remaining % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def get_group_intervals(winner_seconds):
    groups = [
        ("Elit", 1.0),
        ("1", 1.15),
        ("2", 1.25),
        ("3", 1.40),
        ("4", 1.55),
        ("5", 1.70),
        ("6", 1.85),
        ("7", 2.00),
        ("8", 2.30),
        ("9", float('inf'))
    ]
    
    intervals = []
    prev_max_time = 0
    
    for i, (name, max_ratio) in enumerate(groups):
        if name == "Elit":
            max_time = winner_seconds
            interval_str = f"≤ {seconds_to_time(max_time)}"
            ratio_str = "≤ 1.00x"
        else:
            min_time = prev_max_time + 1
            if max_ratio == float('inf'):
                interval_str = f"> {seconds_to_time(min_time - 1)}"
                ratio_str = f"> {groups[i-1][1]:.2f}x"
                max_time = None
            else:
                max_time = int(winner_seconds * max_ratio)
                interval_str = f"{seconds_to_time(min_time)} – {seconds_to_time(max_time)}"
                ratio_str = f"{groups[i-1][1]:.2f}x – {max_ratio:.2f}x"
        
        intervals.append({
            "group": name,
            "interval": interval_str,
            "ratio": ratio_str
        })
        
        if max_time is not None:
            prev_max_time = max_time
    
    return intervals

def calculate_seeding(winner_time, given_time):
    if winner_time <= 0:
        return "Error", 0
    
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
        st.info(f"**Tidsratio**: {ratio:.2f}x")
        
        # Visa alla tidsintervall
        st.markdown("### Tidsintervall för alla led")
        intervals = get_group_intervals(winner_seconds)
        
        # Skapa en tabell
        table = "| Led | Tidsintervall | Ratio |\n"
        table += "|-----|---------------|-------|\n"
        for interval in intervals:
            table += f"| {interval['group']} | {interval['interval']} | {interval['ratio']} |\n"
        st.markdown(table)
        
        # Förklaring
        st.markdown("### Förklaring")
        st.write(f"Din tid ({seconds_to_time(eval_seconds)}) är {ratio:.2f}x vinnarens tid ({seconds_to_time(winner_seconds)}) på {distance} km.")

st.markdown("---")
st.caption("Baserat på seedningsdata från Vasaloppet 2025. Gränser kan variera något mellan olika lopp.")