import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dataClient import dataReqSync
import plotly.graph_objects as go

app = dash.Dash(__name__) ## just to define the only-one-app for others.
app.title = "test warehouse"
server = app.server 
dataReq = dataReqSync()

app.layout = html.Div([
    html.Div( # Row - 0 : title
        className="row",
        children = [html.H1("Demo warehouse : inventory / products ", className='header0')
    ]),
    
    html.Div( # Row - 1 : Operations
        className="row",
        children = [
            html.Div(
                className = "six columns div-user-controls",
                children = [
                    dcc.Dropdown(
                        id='sell-name',
                        options=[
                            {'label': '1', 'value': '1'},
                        ],
                        value='1'), 
                    dcc.Input(id='sell-num', type='number', placeholder='num', min=-3, max=3, step=1), 
                    html.Button('Sell products', id='sell-button')
            ]),
            html.Div(
                className = "six columns div-user-controls",
                children = [
                    html.Button('Show inventory', id='inventory-button')
            ])
    ]),
    
    html.Div( # Row - 2 : Graphs: products available / inventory stocks
        className="row",
        children = [
            html.Div(
                className = "six columns my-container",
                children = [
                    html.P("Figure : available products"),
                    dcc.Graph(id="plot-product-num")
            ]),
            
            html.Div(
                className = "six columns my-container",
                children = [
                    html.P("Figure : Inventory stocks"),
                    dcc.Graph(id="plot-inventory")
            ]),
    ]),
])


@app.callback(
        Output('plot-inventory', 'figure'),
        Input('inventory-button', 'n_clicks'),
    )
def getInventory(n):
    dbData = dataReq.getDb()
    inv = dbData['inventory']
    print('---ínv---',inv)
    fig = go.Figure([go.Bar(x=[i['name'] for i in inv], y=[i['stock'] for i in inv])])
    return fig


@app.callback(Output('plot-product-num', 'figure'),
              Output('sell-name', 'options'),
              Input('sell-button', 'n_clicks'),
              State('sell-name','value'),
              State('sell-num', 'value'))
def sellProducts(n, name, num):
    dataReq.rmProduct(name, num)
    products = dataReq.getProductNum()
    # print(products, products.values(), products.keys())
    fig = go.Figure([go.Bar(y=list(products.values()), x=list(products.keys())) ])
    options = [{'label':k, 'value':k} for k in products.keys()]
    return fig, options

# @app.callback(Output('plot-product-num', 'figure'),
#               Input('sell-button', 'n_clicks'),
#               State('sell-num', 'value'))
# def sellProducts(n, value):
#     return 

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)




