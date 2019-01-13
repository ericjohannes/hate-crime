# my script

# connect to sql server
# for location_name
# read

# close connection to sql server
import pandas as pd
import MySQLdb

con = MySQLdb.Connect(host="silo.cs.indiana.edu", port=45188, user="hate_crimes", passwd="password", db="hate_crimes")

sql = "SElECT * FROM hate_crime"
index_col = "INCIDENT_ID"
table_df = pd.read_sql(sql, con=con, index_col = index_col)
table_df = pd.read_sql(sql, con=con)

# works!

# seems that ; is used to join multiple values, '/' just means a value is broad, like anti russian or anti greek
# break location_name out, separate all by / and ; and make it true/false for each
# break offense_name out, separate all by / and ; and make it true/false for each
# break bias_desc out, separate all by / and ; and make it true/false for each
# break victim_types out, separate all by / and ; and make it true/false for each

# finds rows where there is a ';'
table_df[table_df['BIAS_DESC'].str.find(';') > -1]

# this works
bias_df = pd.DataFrame(table_df.BIAS_DESC.str.split(';').tolist(), index=table_df.INCIDENT_ID).stack()
bias_df = bias_df.reset_index()[[0, 'INCIDENT_ID']] # var1 variable is currently labeled 0
bias_df.columns = ['BIAS_DESC', 'INCIDENT_ID'] # renaming var1


bias_df[bias_df['BIAS_DESC'].isnull()]

# try to write to sql table

# with sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('mysql://hc_admin1:password@silo.cs.indiana.edu:45188/hate_crimes')

bias_df.to_sql(name='bias_desc', con=engine, index=False, if_exists='append')

table_list = ['location_name', 'offense_name', 'victim_types']

# three more times
offense_df = pd.DataFrame(table_df.OFFENSE_NAME.str.split(';').tolist(), index=table_df.INCIDENT_ID).stack()
offense_df = offense_df.reset_index()[[0, 'INCIDENT_ID']] # var1 variable is currently labeled 0
offense_df.columns = ['OFFENSE_NAME', 'INCIDENT_ID'] # renaming var1
offense_df.to_sql(name='offense_name', con=engine, index=False, if_exists='append')

location_df = pd.DataFrame(table_df.LOCATION_NAME.str.split(';').tolist(), index=table_df.INCIDENT_ID).stack()
location_df = location_df.reset_index()[[0, 'INCIDENT_ID']] # var1 variable is currently labeled 0
location_df.columns = ['LOCATION_NAME', 'INCIDENT_ID'] # renaming var1
location_df.to_sql(name='location_name', con=engine, index=False, if_exists='append')

victims_df = pd.DataFrame(table_df.VICTIM_TYPES.str.split(';').tolist(), index=table_df.INCIDENT_ID).stack()
victims_df = victims_df.reset_index()[[0, 'INCIDENT_ID']] # var1 variable is currently labeled 0
victims_df.columns = ['VICTIM_TYPES', 'INCIDENT_ID'] # renaming var1
victims_df.to_sql(name='victim_types', con=engine, index=False, if_exists='append')

