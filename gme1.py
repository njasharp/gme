import streamlit as st
import random
import time

st.markdown("""
    <style>
    /* Hide the Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Set background color to black */
    .css-18e3th9 {
        background-color: black;
    }
    .css-1d391kg {
        background-color: black;
    }
    </style>
    """, unsafe_allow_html=True)
# Initialize session state if not already done
if 'labels' not in st.session_state:
    st.session_state.labels = ['Speed', 'Power', 'Flight', 'Intelligence', 'Strength', 'Stamina', 'Magic']
if 'stats' not in st.session_state:
    st.session_state.stats = [70, 60, 50, 80, 90, 75, 85]
if 'cpu_choice' not in st.session_state:
    st.session_state.cpu_choice = None
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'player_health' not in st.session_state:
    st.session_state.player_health = 100
if 'cpu_health' not in st.session_state:
    st.session_state.cpu_health = 100
if 'rounds_played' not in st.session_state:
    st.session_state.rounds_played = 0
if 'player_wins' not in st.session_state:
    st.session_state.player_wins = 0
if 'cpu_wins' not in st.session_state:
    st.session_state.cpu_wins = 0
if 'used_labels' not in st.session_state:
    st.session_state.used_labels = []
if 'status' not in st.session_state:
    st.session_state.status = "Fight!"

# Define attribute interactions
interactions = {
    'Speed': ['Power', 'Stamina'],
    'Power': ['Flight', 'Intelligence'],
    'Flight': ['Strength', 'Magic'],
    'Intelligence': ['Speed', 'Magic'],
    'Strength': ['Power', 'Stamina'],
    'Stamina': ['Intelligence', 'Flight'],
    'Magic': ['Strength', 'Speed']
}

# Function to make CPU choice
def cpu_select():
    if st.session_state.labels:
        return random.choice(st.session_state.labels)
    return None

# Function to determine the winner
def determine_winner(player_choice, cpu_choice):
    if cpu_choice in interactions[player_choice]:
        st.session_state.cpu_health -= 20
        st.session_state.player_wins += 1
        return f"Player Wins! 🎉 {player_choice} {cpu_choice}"
    elif player_choice in interactions[cpu_choice]:
        st.session_state.player_health -= 20
        st.session_state.cpu_wins += 1
        return f"CPU Wins! 🤖 {player_choice} {cpu_choice}"
    else:
        # Coin toss to resolve tie
        coin_toss = random.choice(['Player', 'CPU'])
        if coin_toss == 'Player':
            st.session_state.cpu_health -= 20
            st.session_state.player_wins += 1
            return "It's a Tie! Coin toss decides: Player Wins! 🎉"
        else:
            st.session_state.player_health -= 20
            st.session_state.cpu_wins += 1
            return "It's a Tie! Coin toss decides: CPU Wins! 🤖"

st.sidebar.image("ai_logo.PNG", width=180)
# Display health bars in the sidebar
st.sidebar.markdown("### Health Bars")
st.sidebar.write(f"Player Health: {'❤️' * (st.session_state.player_health // 20)}")
st.sidebar.write(f"CPU Health: {'🤖' * (st.session_state.cpu_health // 20)}")

# Display rounds played and check for game over
st.sidebar.write(f"Rounds Played: {st.session_state.rounds_played}/5")

if st.session_state.rounds_played >= 5 or not st.session_state.labels:
    st.sidebar.markdown("### Game Over")
    if st.session_state.player_wins > st.session_state.cpu_wins:
        st.sidebar.write("Final Result: Player Wins! 🎉")
    elif st.session_state.cpu_wins > st.session_state.player_wins:
        st.sidebar.write("Final Result: CPU Wins! 🤖")
    else:
        st.sidebar.write("Final Result: It's a Tie! 🤝")
    
    # Reset game
    if st.sidebar.button("Reset Game"):
        st.session_state.labels = ['Speed', 'Power', 'Flight', 'Intelligence', 'Strength', 'Stamina', 'Magic']
        st.session_state.stats = [70, 60, 50, 80, 90, 75, 85]
        st.session_state.cpu_choice = None
        st.session_state.result = ""
        st.session_state.player_health = 100
        st.session_state.cpu_health = 100
        st.session_state.rounds_played = 0
        st.session_state.player_wins = 0
        st.session_state.cpu_wins = 0
        st.session_state.used_labels = []
        st.session_state.status = "Fight!"
else:
    st.sidebar.write(f"Round: {st.session_state.rounds_played}/5")
    st.sidebar.write(f"CPU move: {st.session_state.cpu_choice}")

# Display the current labels and stats
st.markdown("## AI Fighter - Choose Your Attribute")
st.text(st.session_state.labels)
st.text(st.session_state.stats)

# Player selects a stat
player_choice = st.radio("Select an attribute:", options=st.session_state.labels)

if st.button("Fight! ⚔️"):
    if player_choice in st.session_state.used_labels:
        st.warning("You cannot select the same attribute twice. Please choose another one.")
    else:
        st.session_state.used_labels.append(player_choice)
        st.session_state.status = "Fighting... ⚔️"
        with st.spinner("Battling..."):
            time.sleep(3)  # Wait for 3 seconds
        st.session_state.cpu_choice = cpu_select()
        if st.session_state.cpu_choice is not None:
            st.session_state.result = determine_winner(player_choice, st.session_state.cpu_choice)
            st.session_state.rounds_played += 1
            # Remove the selected attribute and its stat
            index = st.session_state.labels.index(player_choice)
            st.session_state.labels.pop(index)
            st.session_state.stats.pop(index)
            st.session_state.status = "Fight End!"
            
        st.experimental_rerun()

# Display fight sequence and status
st.sidebar.markdown("### Status")
st.sidebar.markdown(f"## {st.session_state.status}")
if st.session_state.status == "Fight End!":
    st.sidebar.markdown(f"## {st.session_state.result}")

col1, col2 = st.columns(2)
st.markdown("""
    <style>
    .small-font {
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
with col1:
    st.image("legend1.PNG", width=280)
    # Display summary of the game logic
    st.markdown("### Summary of the Game Logic")
    st.markdown("""
        - **Player and CPU each select an attribute.**
        - **Random stat is generated.**
        - **Winner is determined based on who is closer to the random stat.**
        - **Tie resolved by a coin toss.**
        - **Loser’s health is reduced.**
        - **Game ends after 5 rounds or when no attributes are left.**
        - **Final result is displayed, and the game can be reset.**
        """)
    
with col2:
    st.image("legend.PNG", width=320)   

# Display attributes and their interactions
    st.markdown("### Attributes and their Interactions:")
    st.markdown("""
        - **Speed ⚡ beats Power 💪 and Stamina 🏃.**
        - **Power 💪 beats Flight ✈️ and Intelligence 🧠.**
        - **Flight ✈️ beats Strength 🔨 and Magic ✨.**
        - **Intelligence 🧠 beats Speed ⚡ and Magic ✨.**
        - **Strength 🔨 beats Power 💪 and Stamina 🏃.**
        - **Stamina 🏃 beats Intelligence 🧠 and Flight ✈️.**
        - **Magic ✨ beats Strength 🔨 and Speed ⚡.**
        - **Otherwise tie and coin toss win/forfeit **
        """)
    
st.info("Built by dw")







