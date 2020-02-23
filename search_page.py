import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table 
import pandas as pd 

def search_page():
    page_sub_header = html.H2('ค้นหารายชื่อ', className='pageSubHeader')

    text_firstname = html.P(id='search_page_text_firstname', children='ชื่อ', className='textLabel')
    textbox_firstname = dcc.Input(
        id='search_page_textbox_firstname',
        placeholder="ชื่อ",
        type='text',
        value='',
        className = 'textbox_detail'
    )
    
    text_lastname = html.P(id='search_page_text_lastname', children='นามสกุล', className='textLabel')
    textbox_lastname = dcc.Input(
        id='search_page_textbox_lastname',
        placeholder="นามสกุล",
        type='text',
        value='',
        className = 'textbox_detail'
    )

    button_search = html.Button('ค้นหา', id='search_page_button_search', className='searchButton')
    
    text_bag_number = html.P(id='search_page_text_bag_number', children='หมายเลขถุง', className='textLabel')
    textbox_bag_number = dcc.Input(
        id='search_page_textbox_bag_number',
        placeholder="หมายเลขถุง",
        type='number',
        value=None,
        className = 'textbox_bag_number'
    )
    
    button_recieved = html.Button('รับสินค้า', id='search_page_button_recieved', className='receivedButton')
    button_cancel = html.Button('ยกเลิก', id='search_page_button_cancel', className='cancelButton')

    text_status = html.P(id='search_page_text_search_status', children='', className='textStatus')

    text_status_0 = html.P(id='search_page_text_search_status-0', children='', className='textStatus')
    text_status_1 = html.P(id='search_page_text_search_status-1', children='', className='textStatus')

    df = pd.DataFrame(columns=['หมายเลยถุง', 'วันที่ลงข้อมูล', 'ชื่อ', 'นามสกุล', 'โรงเรียน', 'จำนวนสินค้า', 'รายละเอียด', 'วันที่รับสินค้า'])

    search_table = dash_table.DataTable(
        id='search_page_result_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_as_list_view= True,
        style_cell={'padding': '5px'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_table={
            'maxHeight': '800px',
            'maxWidth' : '90%',
            'width'    : '1500px',
            'overflowY': 'scroll',
        }
    )

    page_elements = html.Div([
        page_sub_header,
        html.Div(
            [text_firstname,
            textbox_firstname,
            text_lastname,
            textbox_lastname,
            button_search,
            ],
            className= 'inputDetails'
        ),
        html.Div(
            [text_bag_number,
            textbox_bag_number,
            button_recieved,
            button_cancel,
            ],
            className='inputBagDetails'
        ),
        text_status,
        text_status_0,
        text_status_1,
        html.Div(
            [search_table,],
            className='searchTable'
        ),
        dcc.Link('ดูรายชื่อทั้งหมดในระบบ', href='/view_table', className='htmlLink'),
    ])

    return page_elements
