# -*- coding: utf-8 -*-

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html


from dash.dependencies import Input, Output, State
from search_page import search_page
from add_page import add_page  
from view_data_table import show_table
from data_manager import ConnectDB
from authen import valid_accounts

import pandas as pd

tabs_styles = {
    'height': '45px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    valid_accounts
)

app.config.suppress_callback_exceptions = True

page_header = html.H1('แพร่เซ็นเตอร์', className='pageHeader')
main_page = html.Div([
    html.Img(src=app.get_asset_url('logo.png'), id='logo'),
    page_header,
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='ค้นหา', children=search_page(), style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='เพิ่มรายชื่อ', children=add_page(), style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
])

app.layout = html.Div([
    html.Div(id='page-content'),
    dcc.Location(id='url', refresh=False),
])

@app.callback(
    [
        Output('add_page_textbox_bag_number', 'value'),
        Output('add_page_textbox_firstname', 'value'),
        Output('add_page_textbox_lastname', 'value'),
        Output('add_page_textbox_product_count', 'value'),
        Output('add_page_dropdown_school', 'value'),  
        Output('add_page_textbox_product_details', 'value'), 
    ],
    [Input('add_page_button_add', 'n_clicks')],
    [
        State('add_page_textbox_firstname', 'value'),
        State('add_page_textbox_lastname', 'value'),
        State('add_page_textbox_product_count', 'value'),  
        State('add_page_dropdown_school', 'value'),  
        State('add_page_textbox_product_details', 'value'), 
    ]
)
def insert_new_customer(n_clicks, firstname, lastname, product_count, school_name, details):
    bag_id = None
    try : 
        db = ConnectDB()
        if n_clicks != None :
            if firstname == None :
                firstname = '' 
            if lastname == None :
                lastname = ''
            if firstname != '' or lastname != '':
                print(school_name)
                bag_id = db.insert_data(firstname, lastname, product_count, school_name, details)
        db.close()  
        
    except Exception as E :
        print(E)
    if bag_id != None : 
        return bag_id, '', '', 1, school_name, ''
    else :
        return bag_id, firstname, lastname, product_count, school_name, details

@app.callback(
    Output('add_page_text_add_status', 'children'),
    [Input('add_page_button_delete', 'n_clicks')],
    [
        State('add_page_textbox_bag_number', 'value'),
    ]
)
def delete_data_on_add_page(n_clicks, bag_id):
    db = ConnectDB()
    text_status = ""
    status = False 
    try : 
        db = ConnectDB()
        if n_clicks != None :
            if bag_id != None :
                status = db.delete_data(bag_id)
        print(f"Delete bag id : {bag_id} from Database status : {status}")
        if status : 
            text_status = f'ทำการลบข้อมูลหมายเลข {bag_id} เรียบร้อยแล้ว'
        db.close()  
    except Exception as E :
        print(E)
        text_status = "Error !"
    return text_status

@app.callback(
    Output('search_page_text_search_status', 'children'),
    [Input('search_page_button_cancel', 'n_clicks')],
    [
        State('search_page_textbox_bag_number', 'value'),
    ]
)
def cancel(n_clicks, bag_id):
    text_status = ""
    status = False 
    try : 
        db = ConnectDB()
        if n_clicks != None :
            if bag_id != None :
                db.update_received_date(bag_id, True)
                text_status = f'ทำการยกเลิกข้อมูลหมายเลข {bag_id} เรียบร้อยแล้ว'
        db.close()  
    except Exception as E :
        print(E)
        text_status = "ยกเลิกข้อมูลไม่สำเร็จ กรุณาตรวจสอบข้อมูลใหม่อีกครั้ง"
    return text_status

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def view_database(pathname):
    print(pathname)
    if pathname != '/view_table' : 
        return main_page
    try : 
        db = ConnectDB()
        query_df = db.show_data()
        if len(query_df) > 0 :
            query_df = query_df.sort_values('id', ascending=False)

        display_df = query_df.copy()[['id', 'issued_date','display_first_name', 'display_last_name', 'school_name', 'product_number', 'detail', 'received_date']].rename(columns={
            'id' : 'หมายเลยถุง',
            'issued_date' : 'วันที่ลงข้อมูล',
            'display_first_name' : 'ชื่อ',
            'display_last_name' : 'นามสกุล',
            'school_name' : 'โรงเรียน',
            'product_number' : 'จำนวนสินค้า',
            'detail' : 'รายละเอียด',
            'received_date' : 'วันที่รับสินค้า',
        })
        # display_df = display_df[['หมายเลยถุง', 'วันที่ลงข้อมูล', 'ชื่อ', 'นามสกุล', 'โรงเรียน', 'จำนวนสินค้า', 'รายละเอียด', 'วันที่รับสินค้า']]
        html_table = show_table(display_df)
        db.close()  
        return html.Div([
            dcc.Link('Go Back', href='/', className='htmlLink'),
            html_table
            ])
    except Exception as E :
        print(E)
        text_status = "Error ! PAGE NOT FOUND 404"
        return text_status 

@app.callback(
    [
        Output('search_page_textbox_bag_number', 'value'),
        Output('search_page_result_table', 'data'),
        Output('search_page_text_search_status-0', 'children'),
    ],
    [
        Input('search_page_button_search', 'n_clicks'),
    ],
    [
        State('search_page_textbox_firstname', 'value'),
        State('search_page_textbox_lastname', 'value'),
    ]
)
def search_customer(n_clicks, firstname, lastname):
    bag_id = None
    display_df = pd.DataFrame(columns=['หมายเลยถุง', 'วันที่ลงข้อมูล', 'ชื่อ', 'นามสกุล', 'โรงเรียน', 'จำนวนสินค้า', 'รายละเอียด', 'วันที่รับสินค้า']).to_dict('records')
    status_text = '' 
    try : 
        db = ConnectDB()
        if n_clicks != None :
            if firstname == None :
                firstname = '' 
            if lastname == None :
                lastname = ''
            if firstname != '' or lastname != '':
                query_df, found = db.read_database(firstname, lastname)
                if found:
                    bag_id = query_df['id'].iloc[-1]
                else : 
                    status_text = "ไม่พบข้อมูลที่ต้องการ กรุณาตรวจสอบ ชื่อ-นามสกุล ใหม่อีกครั้ง"
                display_df = query_df.copy()[['id', 'issued_date','display_first_name', 'display_last_name', 'school_name', 'product_number', 'detail', 'received_date']].rename(columns={
                    'id' : 'หมายเลยถุง',
                    'issued_date' : 'วันที่ลงข้อมูล',
                    'display_first_name' : 'ชื่อ',
                    'display_last_name' : 'นามสกุล',
                    'school_name' : 'โรงเรียน',
                    'product_number' : 'จำนวนสินค้า',
                    'detail' : 'รายละเอียด',
                    'received_date' : 'วันที่รับสินค้า',
                })
                display_df = display_df.to_dict('records')
        db.close()  
    except Exception as E: 
        print(E)
        status_text = "เกิดข้อผิดพลาด ระบบไม่สามารถหาข้อมูลได้"
    return bag_id, display_df, status_text



@app.callback(
    Output('search_page_text_search_status-1', 'children'),
    [Input('search_page_button_recieved', 'n_clicks')],
    [State('search_page_textbox_bag_number', 'value')]
)
def recieved_clicked(n_clicks, bag_id):
    text_status = ""
    try : 
        if n_clicks != None : 
            db = ConnectDB()
            db.update_received_date(bag_id)
            text_status = f"ถุงหมายเลข {bag_id} ได้ทำการรับสินค้าเรียบร้อยแล้ว !"
    except Exception as E :
        print(E)
        text_status = "เกิดข้อผิดพลาดไม่สามารถทำรายการได้"
    return text_status 

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True, threaded=True)
