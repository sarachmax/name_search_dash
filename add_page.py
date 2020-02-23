import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table 
import pandas as pd 

def school_list():
    schools = []
    df = pd.read_csv('schoolList.csv')
    for name in df['SchoolName'] : 
        schools.append(dict(label=name, value=name))
    return schools

def add_page():
    page_sub_header = html.H2('เพิ่มรายชื่อ', className='pageSubHeader')

    text_firstname = html.P(id='add_page_text_firstname', children='ชื่อ', className='textLabel')
    textbox_firstname = dcc.Input(
        id='add_page_textbox_firstname',
        placeholder="ชื่อ",
        type='text',
        value='',
        className = 'textbox_detail'
    )
    
    text_lastname = html.P(id='add_page_text_lastname', children='นามสกุล', className='textLabel')
    textbox_lastname = dcc.Input(
        id='add_page_textbox_lastname',
        placeholder="นามสกุล",
        type='text',
        value='',
        className = 'textbox_detail'
    )

    text_product_count = html.P(id='add_page_text_product_count', children='จำนวนสินค้า', className='textLabel')
    textbox_product_count = dcc.Input(
        id='add_page_textbox_product_count',
        placeholder="จำนวนสินค้า",
        type='number',
        value=1,
        className = 'textbox_detail'
    )

    text_school_name = html.P(id='add_page_text_school', children='โรงเรียน', className='textLabel')
    dropdown_school = dcc.Dropdown(
        id='add_page_dropdown_school',
        options = school_list(),
        value = 'อื่นๆ',
        className = 'school_dropdown'
    )

    text_product_details = html.P(id='add_page_text_product_details', children='รายละเอียด', className='textLabel')
    textbox_product_details = dcc.Input(
        id='add_page_textbox_product_details',
        placeholder="รายละเอียด",
        type='text',
        value='',
        className = 'textbox_detail'
    )

    button_add = html.Button('เพิ่มชื่อ', id='add_page_button_add', className='addButton')
    
    text_bag_number = html.P(id='add_page_text_bag_number', children='หมายเลขถุง', className='textLabel')
    textbox_bag_number = dcc.Input(
        id='add_page_textbox_bag_number',
        placeholder="หมายเลขถุง",
        type='number',
        value=None,
        className = 'textbox_bag_number',
        disabled =False
    )
    button_delete = html.Button('ลบข้อมูล', id='add_page_button_delete', className='deleteButton')

    text_status = html.P(id='add_page_text_add_status', children='', className='textStatus')
    
    text_status_0 = html.P(id='add_page_text_add_status-0', children='', className='textStatus')

    page_elements = html.Div([
        page_sub_header,
        html.Div(
            [text_firstname,
            textbox_firstname,
            text_lastname,
            textbox_lastname,
            text_product_count,
            textbox_product_count,
            text_school_name,
            dropdown_school,
            text_product_details,
            textbox_product_details,
            button_add,
            ],
            className= 'inputDetails'
        ),
        html.Div(
            [text_bag_number,
            textbox_bag_number,
            button_delete,
            ],
            className='inputBagDetails'
        ),
        text_status,
        text_status_0,
        dcc.Link('ดูรายชื่อทั้งหมดในระบบ', href='/view_table', className='htmlLink'),
    ])
    
    return page_elements