import pandas as pd 
from datetime import datetime
import pytz 
import sqlite3

def command_to_query(data, match_all=True, use_and_operator=True):
	command = ''
	query_commands = []
	if use_and_operator : 
		operator = ' AND '
	else : 
		operator = ' OR '
	if match_all : 
		for key in data : 
			query_commands.append('{} = "{}"'.format(key, data[key]))
		for i in range(len(query_commands)):
			if i == 0 :
				command += query_commands[i]
			else : 
				command += operator + query_commands[i] 
	else : 
		for key in data : 
			query_commands.append('{} LIKE "%{}%"'.format(key, data[key]))
		for i in range(len(query_commands)):
			if i == 0 :
				command += query_commands[i]
			else : 
				command += operator + query_commands[i] 
	return command

class ConnectDB:
	def __init__(self):
		self.conn = sqlite3.connect("name.db")
		self.cur = self.conn.cursor()
		self.create_database_table()
		
	def create_database_table(self):
		task_create_table = '''
		CREATE TABLE IF NOT EXISTS CustomerNames (
			id integer PRIMARY KEY, 
			display_first_name text,
			display_last_name text,
			search_first_name text,
			search_last_name text,
			school_name text,
			product_number integer,
			issued_date text,
			received_date text,
			detail text
		);
		'''
		# print("Create New Database ! ! !")
		self.cur.execute(task_create_table)
		self.conn.commit() 

	def insert_data(self, first_name='', last_name='', product_number=0, school_name='', detail=''):
		tz_bangkok = pytz.timezone('Asia/Bangkok')
		current_date = datetime.now(tz_bangkok).strftime('%d-%m-%Y %H:%M:%S')
		data = dict(
			display_first_name=first_name,
			display_last_name=last_name,
			search_first_name=first_name.replace(' ', ''),
			search_last_name=last_name.replace(' ', ''),
			school_name=school_name,
			product_number=product_number,
			detail = detail,
			issued_date = current_date
		)
	
		task_insert = 'INSERT INTO CustomerNames '
		insert_columns = []
		insert_values = [] 
		for key in data : 
			insert_columns.append(key)
			insert_values.append(data[key])
		insert_columns = str(tuple(insert_columns)).replace("'","")
		insert_values = str(tuple(insert_values))
	
	
		task_insert +=  insert_columns + '\n'
		task_insert += 'VALUES ' + insert_values 
		
		self.cur.execute(task_insert)
		self.conn.commit()
	
		task_read_table ='''
		SELECT * 
		FROM CustomerNames
		WHERE '''
		
		query_read_table = task_read_table + command_to_query(data)

		df = pd.read_sql_query(query_read_table, self.conn) 
		
		return df.id.iloc[0]
	
	def update_received_date(self, bag_id, cancel=False):	
		if not cancel : 
			tz_bangkok = pytz.timezone('Asia/Bangkok')
			current_date = datetime.now(tz_bangkok).strftime('%d-%m-%Y %H:%M:%S')
			task_update = '''
			UPDATE CustomerNames
			SET received_date = '{}'
			WHERE id = {};
			'''.format(current_date,bag_id)
		else : 
			task_update = '''
			UPDATE CustomerNames
			SET received_date = '{}'
			WHERE id = {};
			'''.format('',bag_id)
		self.cur.execute(task_update)
		self.conn.commit()
		
	def read_database(self, first_name='',
					   last_name='',
					   bag_id=''):
		data = dict(
			search_first_name=first_name.replace(' ', ''),
			search_last_name=last_name.replace(' ', ''),
			id=bag_id,
		)

		command = {}
		for key in data : 
			if data[key] != '' :
				command[key] = data[key]
		
		task_read_table ='''
		SELECT * 
		FROM CustomerNames
		WHERE '''
	
		query_read_table = task_read_table + command_to_query(command)
		
		df = pd.read_sql_query(query_read_table, self.conn)
		found = True 
		
		if df.empty : 
			query_read_table = task_read_table + command_to_query(command, False)
			df = pd.read_sql_query(query_read_table, self.conn)
			found = False
		if df.empty : 
			query_read_table = task_read_table + command_to_query(command, False, False)
			df = pd.read_sql_query(query_read_table, self.conn)
			found = False 
		return df, found 

	def delete_data(self, bag_id):
		try : 
			sql_delete_query = f"""DELETE from CustomerNames where id = {bag_id}""" 
			self.cur.execute(sql_delete_query)
			self.conn.commit() 
			return True
		except Exception as E:
			print(E) 
			return False  

	def show_data(self):
		query_read_table = '''
			SELECT * 
			FROM CustomerNames
		'''
		df = pd.read_sql_query(query_read_table, self.conn)
		return df 

	def close(self):
		self.conn.close()
#conn.close()
		