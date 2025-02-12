def flatten_keyword_demand(df):
    """Flattens keyword demand data"""
    keyword_expanded = []
    
    df[['City_Name', 'State', 'Country']] = df['City'].str.split(',', expand=True)
    
    for index, row in df.iterrows():
        city_keywords = row['Keyword Demand']
        for keyword_data in city_keywords:
            keyword_dict = {
                'City_Name': row['City_Name'],
                'State': row['State'],
                'Country': row['Country'],
                'Keyword': keyword_data['keyword'],
                'Competition_Index': keyword_data['competition_index'],
                'Avg_Search': keyword_data['avg_search'],
                'Competition_Level': keyword_data['competition_level']
            }
            
            for month, volume in keyword_data['monthly_search_volumes'].items():
                keyword_dict[month] = volume
                
            keyword_expanded.append(keyword_dict)
    
    return pd.DataFrame(keyword_expanded)