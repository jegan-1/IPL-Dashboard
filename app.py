import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)


@st.cache_data
def load_data():
    matches = pd.read_csv('data/matches_cleaned.csv')
    deliveries = pd.read_csv('data/deliveries_cleaned.csv')
    return matches, deliveries

matches, deliveries = load_data()


st.title("🏏 IPL Analytics Dashboard")
st.markdown("Complete analysis of Indian Premier League")


st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox(
    "Select Season",
    options=['All'] + sorted(matches['season'].unique().tolist())
)


if selected_season != 'All':
    filtered_matches = matches[matches['season'] == selected_season]
else:
    filtered_matches = matches


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", len(filtered_matches))
with col2:
    st.metric("Total Seasons", filtered_matches['season'].nunique())
with col3:
    most_wins = filtered_matches['winner'].value_counts().index[0]
    st.metric("Most Wins", most_wins)
with col4:
    toss_win_rate = (
        filtered_matches['toss_winner'] == filtered_matches['winner']
    ).mean()
    st.metric("Toss Win = Match Win", f"{toss_win_rate:.1%}")

st.divider()


col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Team Win Count")
    wins = filtered_matches['winner'].value_counts().reset_index()
    wins.columns = ['Team', 'Wins']
    fig = px.bar(wins, x='Wins', y='Team',
                 orientation='h',
                 color='Wins',
                 color_continuous_scale='Oranges')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Toss Decision Trend")
    toss = filtered_matches['toss_decision'].value_counts()
    fig = px.pie(values=toss.values,
                 names=toss.index,
                 color_discrete_sequence=['#FF6B35', '#004E89'])
    st.plotly_chart(fig, use_container_width=True)

st.divider()

batsman_col = 'batter' if 'batter' in deliveries.columns else 'batsman'

st.subheader("🏏 Top 10 Run Scorers")
runs = deliveries.groupby(batsman_col)['batsman_runs'].sum()
runs = runs.sort_values(ascending=False).head(10).reset_index()
runs.columns = ['Player', 'Runs']
fig = px.bar(runs, x='Player', y='Runs',
             color='Runs',
             color_continuous_scale='Reds')
st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎳 Top Wicket Takers")
    wickets = deliveries[
        deliveries['dismissal_kind'].notna() &
        ~deliveries['dismissal_kind'].isin([
            'run out', 'retired hurt', 'obstructing the field'
        ])
    ]['bowler'].value_counts().head(10).reset_index()
    wickets.columns = ['Bowler', 'Wickets']
    fig = px.bar(wickets, x='Bowler', y='Wickets',
                 color='Wickets',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📍 Top Venues")
    venues = filtered_matches['venue'].value_counts().head(8).reset_index()
    venues.columns = ['Venue', 'Matches']
    fig = px.pie(venues, values='Matches', names='Venue')
    st.plotly_chart(fig, use_container_width=True)

st.divider()


st.subheader("📈 Matches Per Season")
season_matches = matches.groupby('season').size().reset_index()
season_matches.columns = ['Season', 'Matches']
fig = px.line(season_matches, x='Season', y='Matches',
              markers=True,
              line_shape='spline',
              color_discrete_sequence=['#FF6B35'])
st.plotly_chart(fig, use_container_width=True)