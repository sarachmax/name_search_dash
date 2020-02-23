import dash_table

def show_table(df):
    return dash_table.DataTable(
        id = 'view_database',
        columns = [
            {"name": i, "id": i} for i in df.columns
        ],
        data=df.to_dict('records'),
        style_table={
            'maxHeight': '1500px',
            'maxWidth' : '90%',
            'width'    : '1500px',
            'overflowY': 'scroll',
        }
    )

