import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table 
from dash.dependencies import Input, Output, State
import pandas as pd 


def input_box(id='', placeholder='fill the value', input_type='text', value=''):
    return dcc.Input(
                    id=id,
                    placeholder=placeholder,
                    type=input_type,
                    value=value,
                    ) 

def plain_text(id='', text=''):
    return html.P(id=id,
            children=text)

def table(id='', df=pd.DataFrame(), page_size=25):
    return dash_table.DataTable(
                id=id, 
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_current=0,
                page_size=page_size,
                page_action='custom'
                )

def main_page():
    page_header = html.H1('ค้นหาชื่อปัก แพร่เซ็นเตอร์')

    text_first_name = plain_text(id='main_page-text_name', text='ชื่อ')
    textbox_first_name = input_box(id='main_page-textbox_first_name', placeholder='FirstName', input_type='text', value='')

    text_last_name = plain_text(id='main_page-text_last_name', text='นามสกุล')
    textbox_last_name = input_box(id='main_page-textbox_last_name', placeholder='LastName', input_type='text', value='')

    text_school_name = plain_text(id='main_page-text_school_name', text='โรงเรียน')
    textbox_school_name = input_box(id='main_page-textbox_school_name', placeholder='SchoolName', input_type='text', value='')

    # text_product_number = plain_text(id='text_product_number', text='จำนวน')
    # textbox_product_number = input_box(id='textbox_product_number', placeholder='ProductNumber', input_type='number', value=None)

    text_bag_number = plain_text(id='main_page-text_bag_number', text='หมายเลข')
    textbox_bag_number = input_box(id='main_page-textbox_bag_number', placeholder='BagNumber', input_type='number', value=None)

    table_format= pd.DataFrame(columns=['BagNumber', 'FirstName', 'LastName', 'ProductNumber', 'RecievedDate'])
    table_search_result = table('main_page-table_search_result', table_format)

    recieved_button = html.Button('รับสินค้า', id='main_page-recieved_button')
    search_button = html.Button('ค้นหา', id='main_page-search_button')
    delete_button = html.Button('ลบข้อมูล', id='main_page-delete_button')
    
    text_run_status = plain_text(id='main_page-text_run_status', text='')

    page = [
        page_header,
        text_first_name, textbox_first_name,
        text_last_name, textbox_last_name,
        text_school_name, textbox_school_name,
        text_bag_number, textbox_bag_number, 
        search_button , recieved_button, delete_button,
        table_search_result
    ]
    page = html.Div(page, style={'backgroundColor':'lightblue'})
    return page 

def add_page():
    page_header = html.H1('เพิ่มรายชื่อ แพร่เซ็นเตอร์')

    text_first_name = plain_text(id='add_page-text_name', text='ชื่อ')
    textbox_first_name = input_box(id='add_page-textbox_first_name', placeholder='FirstName', input_type='text', value='')

    text_last_name = plain_text(id='add_page-text_last_name', text='นามสกุล')
    textbox_last_name = input_box(id='add_page-textbox_last_name', placeholder='LastName', input_type='text', value='')

    text_school_name = plain_text(id='add_page-text_school_name', text='โรงเรียน')
    textbox_school_name = input_box(id='add_page-textbox_school_name', placeholder='SchoolName', input_type='text', value='')

    text_product_number = plain_text(id='add_page-text_product_number', text='จำนวน')
    textbox_product_number = input_box(id='add_page-textbox_product_number', placeholder='ProductNumber', input_type='number', value=None)

    text_bag_number = plain_text(id='add_page-text_bag_number', text='หมายเลข')
    textbox_bag_number = input_box(id='add_page-textbox_bag_number', placeholder='BagNumber', input_type='number', value=None)

    table_format= pd.DataFrame(columns=['BagNumber', 'FirstName', 'LastName', 'ProductNumber', 'RecievedDate'])
    table_search_result = table('add_page-table_search_result', table_format)

    recieved_button = html.Button('เพิ่มรายชื่อ', id='add_page-recieved_button')
    delete_button = html.Button('ลบข้อมูล', id='add_page-delete_button')
    
    text_run_status = plain_text(id='add_page-text_run_status', text='')

    page = [
        page_header,
        text_first_name, textbox_first_name,
        text_last_name, textbox_last_name,
        text_school_name, textbox_school_name,
        text_product_number, textbox_product_number,
        text_bag_number, textbox_bag_number, 
        search_button , recieved_button, delete_button,
        table_search_result
    ]
    page = html.Div(page)
    return page 


app = dash.Dash(__name__)
# search_page = main_page()
# insert_page = add_page() 

tabs = html.Div([dcc.Tabs(id='main_tab', value='main_page', children=[
    dcc.Tab(label='ค้นหาชื่อลูกค้า', value='main_page'),
    dcc.Tab(label='เพิ่มชื่อลูกค้า', value='add_apge')
    ], html.Div(id='tabs-content-example'))
    )

app.layout = tabs

@app.callback(Output('main_tab', 'children'),
              [Input('main_tab', 'value')])
def render_content(tab):
    if tab == 'add_apge':
        return add_page()
    else :
        return main_page() 
# @app.callback(
#     [Output(component_id='bar_chart_max_sharpe_ratio', component_property='figure'),
#      Output(component_id='bar_chart_min_vol', component_property='figure'),
#      Output(component_id='text_run_status', component_property='children')
#     ],
#     [Input(component_id='run_button', component_property='n_clicks')],
#     state=[
#         State(component_id='quotes_dropdown_bar', component_property='value'),
#         State(component_id='textbox_investment_value', component_property='value'),
#         State(component_id='textbox_risk_free_rate', component_property='value'),
#         State(component_id='textbox_optimization_period', component_property='value'),
#     ]
# )
# def update_bar_chart(n_clicks, quotes, investment_value, risk_free_rate, optimization_period):
#     print(quotes)
#     if quotes != [] : 
#         try : 
#             max_sharp_weights_table, sdp, rp, min_vol_weights_table, sdp_min, rp_min, price_data = portfolio_optimizer_app.update_portfolio(quotes, opt_period=optimization_period, risk_free_rate=risk_free_rate) 
#             max_sharp_weights_table *= investment_value 
#             min_vol_weights_table *= investment_value

#             max_sharp_figure = plot_bar_chart(max_sharp_weights_table, plot_title='Max Sharp Ratio Portfolio')
#             min_vol_figure = plot_bar_chart(min_vol_weights_table, plot_title='Min Volatility Portfolio')
#             result_text = 'Last data updated on : ' + price_data.index[-1].strftime('%Y-%m-%d')
#             return max_sharp_figure, min_vol_figure, result_text 
#         except Exception as e : 
#             raise e 
#             # print(e)
#             error_text = 'Error while calculating stocks allocation please change your stock quotes ! '       
#             return empty_figure(), empty_figure(), error_text 
#     return empty_figure(), empty_figure(), ''

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)