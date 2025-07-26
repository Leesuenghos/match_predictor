import pandas as pd

# 팀 이름 인코딩 매핑
TEAM_ENCODING = {
    "Arsenal": 0, "Aston Villa": 1, "Bournemouth": 2, "Brentford": 3,
    "Brighton": 4, "Burnley": 5, "Chelsea": 6, "Crystal Palace": 7,
    "Everton": 8, "Fulham": 9, "Liverpool": 10, "Luton": 11,
    "Manchester City": 12, "Manchester United": 13, "Newcastle": 14,
    "Nottingham Forest": 15, "Sheffield United": 16, "Tottenham": 17,
    "West Ham": 18, "Wolverhampton": 19
}

# 포메이션 인코딩 매핑
FORMATION_ENCODING = {
    "4-4-2": 0, "4-3-3": 1, "3-5-2": 2, "4-2-3-1": 3,
    "3-4-3": 4, "5-3-2": 5, "5-4-1": 6, "3-4-2-1": 7,
    "4-5-1": 8, "3-1-4-2": 9, "4-1-4-1": 10, "4-3-1-2": 11,
    "3-3-1-3": 12, "4-1-3-2": 13, "4-2-2-2": 14
    # 필요 시 더 추가
}

def preprocess_processed_team_stats(df):
    # ✅ 날짜 관련 파생 피처 생성
    df["match_year"] = pd.to_datetime(df["date"]).dt.year
    df["match_month"] = pd.to_datetime(df["date"]).dt.month
    df["match_day"] = pd.to_datetime(df["date"]).dt.day
    df["match_hour"] = pd.to_datetime(df["date"]).dt.hour

    # ✅ team_name 인코딩
    df.loc[:, "team_name"] = df["team_name"].map(TEAM_ENCODING)

    # ✅ formation 인코딩 (-1: 알 수 없음)
    df.loc[:, "home_formation"] = df["home_formation"].map(FORMATION_ENCODING).fillna(-1).astype(int)
    df.loc[:, "away_formation"] = df["away_formation"].map(FORMATION_ENCODING).fillna(-1).astype(int)

    # ✅ 컬럼 정렬 및 결측치 제거
    selected_cols = [
        "fixture_id", "team_name", "match_year", "match_month", "match_day", "match_hour",
        "is_home", "possession", "shots_total", "shots_on_goal", "passes", "fouls",
        "cards_yellow", "cards_red", "offsides", "home_formation", "away_formation"
    ]

    df = df[selected_cols]
    df = df.dropna(subset=["team_name", "fixture_id"])

    # ✅ 타입 정리 (필요 시 명시적 형변환)
    df.loc[:, "team_name"] = df["team_name"].astype(int)
    df.loc[:, "fixture_id"] = df["fixture_id"].astype(int)

    return df
