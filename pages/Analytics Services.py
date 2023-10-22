# importing Libraries
import pandas as pd
import streamlit as st
import numpy as np

# page set config
st.set_page_config(layout="wide", page_title="Analysis Insights")

# Data load
data = pd.read_csv("asiacup.csv")
# Conventions
ODI_temp = data[data["Format"] == "ODI"]
T20I_temp = data[data["Format"] == "T20I"]
Toss = data[data["Format"] == "ODI"]
champ = pd.read_csv("champion.csv")
ODI_batsman = pd.read_csv("batsman data odi.csv")
T20_batsman = pd.read_csv("batsman data t20i.csv")
ODI_bowler = pd.read_csv("bowler data odi.csv")
T20_bowler = pd.read_csv("bowler data t20i.csv")


# ----------------------------------------- Overall Analysis Class ----------------------------------------
class Analysis:
    def __init__(self, key):
        self.key = key

    def General_Stats(self):
        if self.key == "ODI":
            self.OO = ODI_temp.groupby(["Team", "Result"]).size().reset_index(name='Count')
        elif self.key == "T20":
            self.OO = T20I_temp.groupby(["Team", "Result"]).size().reset_index(name='Count')
        else:
            st.error("Invalid format selected.")
            return None

        Win = self.OO[(self.OO["Result"].isin(["Win", "Win D/L"]))].sort_values("Count", ascending=False).rename(
            columns={"Count": "Win"}).drop("Result", axis=1)
        Lose = self.OO[(self.OO["Result"].isin(["Lose", "Lose D/L"]))].sort_values("Count", ascending=False).rename(
            columns={"Count": "Lose"}).drop("Result", axis=1)
        No_Result = self.OO[self.OO["Result"] == "No Result"].sort_values("Count", ascending=False).rename(
            columns={"Count": "No_Result"}).drop("Result", axis=1)
        Frame = pd.merge(Win, Lose, on="Team", how="outer")
        Frame = pd.merge(Frame, No_Result, on="Team", how="outer")
        Frame.fillna(0, inplace=True)
        Frame["Win"] = Frame['Win'].astype(np.int64)
        Frame["No_Result"] = Frame['No_Result'].astype(np.int64)
        Matches = self.OO.groupby(["Team"])["Count"].sum().reset_index().rename(columns={"Count": "Total Matches Played"})
        Frame = pd.merge(Frame, Matches, on="Team")
        Frame["Winning Percentage"] = round((Frame["Win"] / Frame["Total Matches Played"]) * 100).apply(lambda x: str(x) + "%")

        return Frame

    def Image_Show(self,Team):
        # Provide the correct image paths
        team_image_paths = {
            "Pakistan": "logo-images/pcb-logo.png",
            "India": "logo-images/BCCI_logo.png",
            "Sir Lanka": "logo-images/sirlanka-logo.png",
            "Bangladesh": "logo-images/bangaladesh-logo.png",
            "Afghanistan": "logo-images/afganistan-logo.png",
            "UAE": "logo-images/uae-logo.png",
            "Hong Kong": "logo-images/hongcong-logo.png"
        }

        # Check if the selected team exists in the dictionary and display the image
        if Team in team_image_paths:
            st.image(team_image_paths[Team],width=300)

    def Toss_Win_Team_Win(self):
        global Toss
        if self.key == "ODI":
            Toss = data[data["Format"] == "ODI"]
        elif self.key == "T20":
            Toss = data[data["Format"] == "T20I"]
        TW_MW = Toss[(Toss["Toss"] == "Win") & (Toss["Result"] == "Win")].shape[0]
        TW_ML = Toss[(Toss["Toss"] == "Win") & (Toss["Result"] == "Lose")].shape[0]
        TL_ML = Toss[(Toss["Toss"] == "Lose") & (Toss["Result"] == "Lose")].shape[0]
        TL_MW = Toss[(Toss["Toss"] == "Lose") & (Toss["Result"] == "Win")].shape[0]

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Matches", len(Toss))
        with col2:
            st.metric("Toss Win Match Win", TW_MW)
        with col3:
            st.metric("Toss Win Match Lose", TW_ML)
        with col4:
            st.metric("Toss Lose Match Lose", TL_ML)
        with col5:
            st.metric("Toss Lose Match Win", TL_MW)

    def Toss_Descion_Win_Ratio(self):
        global Toss
        if self.key == "ODI":
            Toss = data[data["Format"] == "ODI"]
        elif self.key == "T20":
            Toss = data[data["Format"] == "T20I"]
        bat_win = Toss[(Toss["Toss"] == "Win") & (Toss["Selection"] == "Batting") & (Toss["Result"] == "Win")].shape[0]
        bat_lose = Toss[(Toss["Toss"] == "Win") & (Toss["Selection"] == "Batting") & (Toss["Result"] == "Lose")].shape[0]
        TW_MW = len(Toss[(Toss["Toss"] == "Win") & (Toss["Result"] == "Win")])
        champ["Host Team Winner"] = (champ["Host"] == champ["Champion"]).apply(lambda x: "Yes" if x == True else "No")
        champ["Host Team Runner up"] = (champ["Host"] == champ["Runner Up"]).apply(lambda x: "Yes" if x == True else "No")
        Host_Win_Percentahe = round((len(champ[champ["Host Team Winner"] == "Yes"]) / 14) * 100)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Win Matches", TW_MW)
        with col2:
            st.metric("Toss Win Choose Batting & Match Win", bat_win)
        col3,col4 = st.columns(2)
        with col3:
            st.metric("Tose Win Choose Bowling & Match Lose", bat_lose)
        with col4:
            st.metric("Chance Host Country Win Asia Cup", Host_Win_Percentahe,"-% out of 100")

    def BatBowl_Stats(self):
        global Toss
        if self.key == "ODI":
            Toss = data[data["Format"] == "ODI"]
        elif self.key == "T20":
            Toss = data[data["Format"] == "T20I"]
        B = Toss[(Toss["Selection"] == "Batting") & (Toss["Result"] == "Win")]
        Be = Toss[(Toss["Selection"] == "Bowling") & (Toss["Result"] == "Win")]
        Bat = B.groupby("Team").agg({"Selection": "count"}).rename(columns={"Selection": "Batting First Win"})
        Bol = Be.groupby("Team").agg({"Selection": "count"}).rename(columns={"Selection": "Bowling First Win"})
        DF = pd.merge(Bat, Bol, on="Team", how="left").fillna(0).astype(np.int32)
        return DF

    def Performance_Stats(self):
        global Toss
        if self.key == "ODI":
            Toss = data[data["Format"] == "ODI"]
        elif self.key == "T20":
            Toss = data[data["Format"] == "T20I"]
        Stats = Toss.groupby("Team").agg(
            {"Run Scored": "sum", "Wicket Lost": "sum", "Wicket Taken": "sum", "Fours": "sum", "Sixes": "sum",
             "Given Extras": "sum"}).sort_values("Run Scored", ascending=False)
        five_Wicket = Toss[Toss["Highest Individual wicket"] == 5.0]
        five_Wicket = five_Wicket.groupby("Team")["Highest Individual wicket"].count().reset_index()
        DF = pd.merge(Stats, five_Wicket, on="Team", how="left")
        DF.fillna(0, inplace=True)
        DF[["Run Scored", "Wicket Lost", "Wicket Taken", "Fours", "Sixes", "Given Extras",
            "Highest Individual wicket"]] = DF[
            ["Run Scored", "Wicket Lost", "Wicket Taken", "Fours", "Sixes", "Given Extras",
             "Highest Individual wicket"]].astype(np.int64)
        return DF

    def Team_Performance_Over_Time(self,Team):
        if self.key == "ODI":
            working = pd.merge(ODI_temp, champ, on="Year")
        elif self.key == "T20":
            working = pd.merge(T20I_temp, champ, on="Year")
        col1,col2 = st.columns(2)
        # images processing
        with col1:
            # working = pd.merge(ODI_temp,champ,on="Year")
            temp1 = working[working["Team"] == Team]
            data = temp1.groupby(["Year"]).agg({
                "Run Scored": "sum",
                "Wicket Lost": "sum",
                "Wicket Taken": "sum",
                "Highest Score": "max"
            }).rename(columns={"Highest Score": "Higgest Score Batsman"})
            st.dataframe(data)
            # Right column with images
        with col2:
            self.Image_Show(Team)


    def Head_to_Head(self,team1, team2):
        if self.key == "ODI":
            matches = ODI_temp[((ODI_temp["Team"] == team1) | (ODI_temp["Opponent"] == team1)) & (
                        (ODI_temp["Team"] == team2) | (ODI_temp["Opponent"] == team2))]
        elif self.key == "T20":
            matches = T20I_temp[((T20I_temp["Team"] == team1) | (T20I_temp["Opponent"] == team1)) & (
                        (T20I_temp["Team"] == team2) | (T20I_temp["Opponent"] == team2))]

        # matches = ODI_temp[((ODI_temp["Team"] == team1) | (ODI_temp["Opponent"] == team1)) & ((ODI_temp["Team"] == team2) | (ODI_temp["Opponent"] == team2))]
        # firstly create own dataframe
        Year_wise = matches[["Team", "Opponent", "Year", "Result", "Ground", "Toss", "Player Of The Match"]]
        Year_wise["Result"] = Year_wise["Result"].apply(lambda x: 1 if x == "Win" else 0)
        Teams = Year_wise.groupby(["Team"])["Result"].sum()
        Total_Matches_Played = Teams[0] + Teams[1]

        img1,img2 = st.columns(2)
        with img1:
            self.Image_Show(team1)
        with img2:
            self.Image_Show(team2)

        col1,col2, = st.columns(2)
        with col1:
            st.metric("Total Matches played between both team are ", Total_Matches_Played)
            st.write(f"{Teams.index[0]} Won {Teams.values[0]} Matches")
            st.write(f"{Teams.index[1]} Won {Teams.values[1]} Matches")
            Year_vise = Year_wise.groupby(["Year", "Ground", "Team"])["Result"].sum().unstack()
            Team1_Tosswin_matchwin = len(Year_wise[(Year_wise["Team"] == team1) & (Year_wise["Toss"] == "Win") & (Year_wise["Result"] == 1)])
            st.write(f"Toss win Match win percent of {team1}", round((Team1_Tosswin_matchwin / Total_Matches_Played) * 100),"%")
            Team2_Tosswin_matchwin = len(Year_wise[(Year_wise["Team"] == team2) & (Year_wise["Toss"] == "Win") & (Year_wise["Result"] == 1)])
            st.write(f"Toss win Match win percent of {team2}", round((Team2_Tosswin_matchwin / Total_Matches_Played) * 100),"%")
        with col2:
            Player_of_the_matches = Year_wise.groupby("Year")["Player Of The Match"].unique().reset_index()
            DF = Year_vise.merge(Player_of_the_matches, on="Year")
            return st.dataframe(DF)

    # single team comparsion to all other team
    def Single_Comparison(self,team):
        global Team
        if self.key == "ODI":
            Team = ODI_temp[ODI_temp["Team"] == team]
        elif self.key == "T20":
            Team = T20I_temp[T20I_temp["Team"] == team]

        col1, col2 = st.columns(2)
        with col1:
            # Team  = ODI_temp[ODI_temp["Team"] == team]
            Team["Result"] = Team["Result"].apply(lambda x: 1 if x == "Win" else 0)
            Win = Team.groupby("Opponent")["Result"].sum().sort_index().reset_index().rename(
                columns={"Result": "Win"})  # won
            Total = Team["Opponent"].value_counts().sort_index().reset_index().rename(
                columns={"count":"total matches"})  # total matches
            Table = Total.merge(Win, on="Opponent")
            Table["Lose"] = Table["total matches"] - Table["Win"]
            st.dataframe(Table)
        with col2:
            im1,im2 = st.columns(2)
            with im1:
                self.Image_Show(team)

# -------------------------------------- Batsman Class ------------------------------------------
class Batsman_Record:
    def __init__(self,key):
        self.key = key

    def Top_Run_Score_Overview(self):
        if self.key == "ODI":
            ODIBataman = ODI_batsman.sort_values("Runs", ascending=False)[["Player Name", "Country", "Matches", "Played", "Runs", "Highest Score", "Batting Average","Balls Faced", "Strike Rate"]]
            st.dataframe(ODIBataman.head())
        elif self.key == "T20":
            T20batman = T20_batsman.sort_values("Runs", ascending=False)[["Player Name", "Country", "Matches", "Played", "Runs", "Highest Score", "Batting Average","Balls Faced", "Strike Rate"]]
            st.dataframe(T20batman.head())

    def Higgest_Indivisual_Score(self):
        st.subheader("Higgest indivisual Score in " + self.key)
        if self.key == "ODI":
            ODIHiggestScore = ODI_batsman.sort_values("Highest Score", ascending=False)[["Player Name", "Country", "Highest Score", "Batting Average"]].reset_index().drop("index",axis=1).head(20)
            st.dataframe(ODIHiggestScore)
        elif self.key == "T20":
            T20HiggestScore = T20_batsman.sort_values("Highest Score", ascending=False)[["Player Name", "Country", "Highest Score", "Batting Average"]].reset_index().drop('index',axis=1).head(20)
            st.dataframe(T20HiggestScore)

    def Most_Centuries(self):
        st.subheader("Most no of Centuries in " + self.key)
        if self.key == "ODI":
            ODICenturies = ODI_batsman.sort_values("Centuries", ascending=False)[["Player Name", "Country", "Centuries", "Batting Average", "Strike Rate"]].reset_index().drop("index",axis=1).head(20)
            st.dataframe(ODICenturies)
        elif self.key == "T20":
            T20Centures = T20_batsman.sort_values("Centuries", ascending=False)[["Player Name", "Country", "Centuries", "Batting Average", "Strike Rate"]].reset_index().drop("index",axis=1).head(2)
            st.dataframe(T20Centures)

    def Most_Four_Six(self):
        four, six = st.columns(2)
        with four:
            st.subheader("Most no of Fours in " + self.key)
            if self.key == "ODI":
                ODI_fours = ODI_batsman.sort_values("Fours", ascending=False)[["Player Name", "Country", "Fours"]].head(
                    20)
                st.dataframe(ODI_fours)
            elif self.key == "T20":
                Four = T20_batsman.sort_values("Fours", ascending=False)[["Player Name", "Country", "Fours"]].head(20)
                st.dataframe(Four)
        with six:
            st.subheader("Most no of Sixes in " + self.key)
            if self.key == "ODI":
                ODI_Six = ODI_batsman.sort_values("Sixes", ascending=False)[["Player Name", "Country", "Sixes"]].head(
                    10)
                st.dataframe(ODI_Six)
            elif self.key == "T20":
                Six = T20_batsman.sort_values("Sixes", ascending=False)[["Player Name", "Country", "Sixes"]].head(10)
                st.dataframe(Six)

    def Most_Runs_On_Boundries(self):
        st.subheader("Most runs on Boundries " + self.key)
        if self.key == "ODI":
            Most_Runs_on_Boundries_Bases = ODI_batsman[["Player Name", "Country", "Matches", "Played", "Batting Average", "Strike Rate", "Fours", "Sixes"]]
            Most_Runs_on_Boundries_Bases["Fours"] = Most_Runs_on_Boundries_Bases["Fours"].apply(lambda x: x * 4)
            Most_Runs_on_Boundries_Bases["Sixes"] = Most_Runs_on_Boundries_Bases["Sixes"].apply(lambda x: x * 6)
            Most_Runs_on_Boundries_Bases["Runs_on_boundries"] = Most_Runs_on_Boundries_Bases["Fours"] + Most_Runs_on_Boundries_Bases["Sixes"]
            ODI_run_on_boundries = Most_Runs_on_Boundries_Bases.sort_values("Runs_on_boundries", ascending=False, ignore_index=True)[["Player Name", "Country", "Played", "Runs_on_boundries"]]
            st.dataframe(ODI_run_on_boundries)
        elif self.key == "T20":
            Most_Runs_on_Boundries_Bases = T20_batsman[["Player Name", "Country", "Matches", "Played", "Batting Average", "Strike Rate", "Fours", "Sixes"]]
            Most_Runs_on_Boundries_Bases["Fours"] = Most_Runs_on_Boundries_Bases["Fours"].apply(lambda x: x * 4)
            Most_Runs_on_Boundries_Bases["Sixes"] = Most_Runs_on_Boundries_Bases["Sixes"].apply(lambda x: x * 6)
            Most_Runs_on_Boundries_Bases["Runs_on_boundries"] = Most_Runs_on_Boundries_Bases["Fours"] + Most_Runs_on_Boundries_Bases["Sixes"]
            T20_run_on_boundries = Most_Runs_on_Boundries_Bases.sort_values("Runs_on_boundries", ascending=False, ignore_index=True)[["Player Name", "Country", "Played", "Runs_on_boundries"]]
            st.dataframe(T20_run_on_boundries)

# --------------------------------------------- Bowler Class -------------------------------
class Bowler_Record:
    def __init__(self,key):
        self.key = key
    def Overall_Record(self):
        if self.key == "ODI":
            ODI_Most_Wicket_Taker = ODI_bowler.sort_values("Wickets", ascending=False)[["Player Name", "Country", "Matches", "Played", "Overs", "Maiden Overs", "Runs", "Wickets"]].head(10)
            st.dataframe(ODI_Most_Wicket_Taker)
        elif self.key == "T20":
            T20_Most_Wicket_Taker = T20_bowler.sort_values("Wickets", ascending=False)[["Player Name", "Country", "Matches", "Played", "Overs", "Maiden Overs", "Runs", "Wickets"]].head(10)
            st.dataframe(T20_Most_Wicket_Taker)

    def Four_Five_Houl(self):
        four,five = st.columns(2)
        with four:
            st.subheader("Four Wicket Houl in " + self.key)
            if self.key == "ODI":
                Four_wicket_houl = ODI_bowler.sort_values("Four Wickets", ascending=False, ignore_index=True)[["Player Name", "Country", "Four Wickets"]].head(7)
                st.dataframe(Four_wicket_houl)
            elif self.key == "T20":
                Four_wicket_houlT20 = T20_bowler.sort_values("Four Wickets", ascending=False, ignore_index=True)[["Player Name", "Country", "Four Wickets"]].head(6)
                st.dataframe(Four_wicket_houlT20)
        with five:
            st.subheader("Five Wicket Houl in " + self.key)
            if self.key == "ODI":
                Five_wicket_houl = ODI_bowler.sort_values("Five Wickets", ascending=False, ignore_index=True)[["Player Name", "Country", "Five Wickets"]].head(7)
                st.dataframe(Five_wicket_houl)
            elif self.key == "T20":
                Five_wicket_houlT20 = T20_bowler.sort_values("Five Wickets", ascending=False, ignore_index=True)[["Player Name", "Country", "Five Wickets"]].head(1)
                st.dataframe(Five_wicket_houlT20)

    def MainOver_BestFigure(self):
        madin,best_figure = st.columns(2)
        with madin:
            st.subheader("Madian Overs in " + self.key)
            if self.key == "ODI":
                Madin_inODI = ODI_bowler.sort_values("Maiden Overs", ascending=False, ignore_index=True)[["Player Name", "Country", "Maiden Overs"]].head(10)
                st.dataframe(Madin_inODI)
            elif self.key == "T20":
                Madin_inT20 = T20_bowler.sort_values("Maiden Overs", ascending=False, ignore_index=True)[["Player Name", "Country", "Maiden Overs"]].head(9)
                st.dataframe(Madin_inT20)
        with best_figure:
            st.subheader("Best Bowling Figure in " + self.key)
            if self.key == "ODI":
                Best_Figure_ODI = ODI_bowler.sort_values("Best Figure", ascending=False, ignore_index=True)[["Player Name", "Country", "Time Period", "Best Figure"]].head(10)
                st.dataframe(Best_Figure_ODI)
            elif self.key == "T20":
                Best_Figure_T20 = T20_bowler.sort_values("Best Figure", ascending=False, ignore_index=True)[["Player Name", "Country", "Time Period", "Best Figure"]].head(10)
                st.dataframe(Best_Figure_T20)

#---------------------------------- Wicket Kipper Class --------------------------------------
class Wicket_Kipper:
    def __init__(self):
        st.header("Wicket Kipper Stats")
    def Kipper_ODI(self):
        st.subheader("ODI Overall wicket kipper records")
        ODI_Wicket_kipper = pd.read_csv("wicketkeeper data odi.csv")
        st.dataframe(ODI_Wicket_kipper.head(10))

    def Kipper_T20(self):
        st.subheader("T20 Overall wicket kipper records")
        T20_Wicket_kipper = pd.read_csv("wicketkeeper data t20i.csv")
        st.dataframe(T20_Wicket_kipper.head(10))






#---------------------------------------Sidebar Controller------------------------------------------
# sidebar created
select = st.sidebar.selectbox("Select One",["Overall Team Analysis","Batsman Analysis","Bowler Analysis","Wicket-Kipper Analysis"])
if select == "Overall Team Analysis":
    # Over all Analysis
    st.header("Overall Stats")
    option = st.selectbox("Select Format", ["ODI","T20"])
    if option:
        analysis_object = Analysis(option)
        st.header(option + " Analysis")
    # Toss Factor
    st.subheader("Winning Probability on Toss Factor")
    if option:
        analysis_object.Toss_Win_Team_Win()

    if option:
        frame = analysis_object.General_Stats()
        st.subheader("Overview")
        st.dataframe(frame)

    st.subheader("Each Team Performance Statistics")
    if option:
            Dataframe = analysis_object.Performance_Stats()
            st.dataframe(Dataframe)



    # Batting Probality
    st.subheader("Toss and Batting Probability Comparison")
    if option:
        analysis_object.Toss_Descion_Win_Ratio()

    #div1,div2 = st.columns(2)

    st.subheader("Batting and Bowling First Probability Analysis")
    if option:
            Dataframe = analysis_object.BatBowl_Stats()
            st.dataframe(Dataframe)

    st.subheader("Team Performance Over Year-wise Analysis")
    select = st.selectbox("Select One",["Pakistan","India","Sir Lanka","Bangladesh","Afghanistan","Hong Kong","UAE"])
    analysis_object.Team_Performance_Over_Time(select)


    # Head to Head Teams
    st.subheader("Head-to-Head Comparison Between Two Teams")
    if option:
        col1,col2 = st.columns(2)
        with col1:
            team1 = st.selectbox("Select Team 1",["Pakistan","India","Sir Lanka","Bangladesh","Afghanistan","Hong Kong","UAE"])
        with col2:
            team2 = st.selectbox("Select Team 2",["India","Pakistan","Sir Lanka","Bangladesh","Afghanistan","Hong Kong","UAE"])
        analysis_object.Head_to_Head(team1,team2)

    # Single Team Comparison with All Teams
    st.subheader("Single Team Comparison with All Teams")
    if option:
       Team = st.selectbox("Select a Team", ["India", "Pakistan", "Sir Lanka", "Bangladesh", "Afghanistan", "Hong Kong", "UAE"])
       analysis_object.Single_Comparison(Team)
# ------------------------------------- Batsman Class Calling----------------------------------
if select == "Batsman Analysis":
    st.header('Batsman Stats')
    option = st.selectbox("Select Format", ["ODI", "T20"])
    if option:
        Batsman = Batsman_Record(option)
        st.subheader(option + "  Batsman Analysis")

    if option:
        Batsman.Top_Run_Score_Overview()
    if option:
        Batsman.Higgest_Indivisual_Score()
    if option:
        Batsman.Most_Centuries()
    if option:
        Batsman.Most_Four_Six()
    if option:
        Batsman.Most_Runs_On_Boundries()

# ------------------------------- Bolwer Class Controller --------------------------------
if select == "Bowler Analysis":
    st.header('Bowlers Stats')
    option = st.selectbox("Select Format", ["ODI", "T20"])
    if option:
        Bowler = Bowler_Record(option)
        st.subheader(option + " Bowlers Analysis")
    if option:
        Bowler.Overall_Record()
        Bowler.Four_Five_Houl()
        Bowler.MainOver_BestFigure()

#----------------------------------- Wicket Kipper Class Contorller ----------------------------
if select == "Wicket-Kipper Analysis":
    Kipper = Wicket_Kipper()
    Kipper.Kipper_ODI()
    Kipper.Kipper_T20()











