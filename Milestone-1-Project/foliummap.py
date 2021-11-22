# Now let's build an interactive map - with a menu of all the indicators.
# These indicators have different measures, so we will standardize them in order to have consistency in the visualization
# Merged_df_norm is our final, normalized dataset
# FOLIUM map code reference: Frederic Gigou SIADS 521 assignment 3

# preparing the data_set
merged_df3=finaldf.copy()
merged_df3.set_index("code",inplace=True)
df3=merged_df3[liste_full]
merged_df_norm = df3.apply(lambda x: (x - np.nanmean(x)) / np.nanstd(x))
df3.reset_index(inplace=True)
df3["Country"]=df3["code"].apply(lambda val:valeurs(val,value=False))
df1=df3
# renaming columns for map visualization
df1.columns=["code","2011 Sales $","GDP","CPI","Population", "Imports", "Internet penetration", "Distance", "Expenditure on Health", "PPP per Capita", "Life Expectancy", "Country"]

