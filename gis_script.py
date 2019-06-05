import geopandas as gpd
import folium
import os
import branca

sogn = os.path.join('data/sogn', 'sogn.geojson')

def sogn_style(feature):
    return {
        'fillColor': '#00000000',
        'color': 'black',
        'z-index': -1,
    }

map = folium.Map(location=[55.5044, 9.7472], zoom_start=13)

folium.GeoJson(sogn, style_function=sogn_style, name='Sogn', show=False).add_to(map)

fg = folium.FeatureGroup(name='routes').add_to(map)

colours = ['red', 'orange', 'yellow', 'blue', 'purple', 'green', 'darkblue',
           'darkred', 'pink', 'black', 'gray', 'darkpurple', 'darkgreen', '#87FF33',
           'brown', 'lightblue', 'lightgreen', 'cadetblue', 'lightgray','#FF33DD',
           '#FFD633', '#00FFFF', '#8D33FF', '#8E44AD', '#58D68D']
colour_index = 0

for f_name in os.listdir('Results'):
    route = gpd.read_file('Results/{}'.format(f_name))

    for index, row in route.iterrows():

        left_col_colour = "#2A799C"
        right_col_colour = "#C5DCE7"
        nr_beholdere = row['count']
        jan_per = row['jan_p_e']
        feb_per = row['feb_p_e']
        rute = row['RuteLabel']
        total_jan = row['jan_mean']
        total_feb = row['feb_mean']

        html = """<!DOCTYPE html>

        <html>

        <head>
        <h4 style="margin-bottom:0"; width="190px">{}</h4>""".format(rute) + """

        </head>
            <table style="height: 126px; width: 180px;">
        <tbody>
        <tr>
        <td style="background-color: """ + left_col_colour + """;"><span style="color: #ffffff;">antal beholdere</span></td>
        <td style="width: 200px;background-color: """ + right_col_colour + """;">{}</td>""".format(nr_beholdere) + """
        </tr>
        <td style="background-color: """ + left_col_colour + """;"><span style="color: #ffffff;">jan gennemsnit</span></td>
        <td style="width: 200px;background-color: """ + right_col_colour + """;">{}</td>""".format(total_jan) + """
        </tr>
        <td style="background-color: """ + left_col_colour + """;"><span style="color: #ffffff;">feb gennemsnit</span></td>
        <td style="width: 200px;background-color: """ + right_col_colour + """;">{}</td>""".format(total_feb) + """
        </tr>
        <tr>
        <td style="background-color: """ + left_col_colour + """;"><span style="color: #ffffff;">januar vægt per beholder</span></td>
        <td style="width: 200px;background-color: """ + right_col_colour + """;">{}</td>""".format(jan_per) + """
        </tr>
        <tr>
        <td style="background-color: """ + left_col_colour + """;"><span style="color: #ffffff;">februar vægt per beholder</span></td>
        <td style="width: 200px;background-color: """ + right_col_colour + """;">{}</td>""".format(feb_per) + """
        </tr>
        </tbody>
        </table>
        </html>
        """

        iframe = branca.element.IFrame(html=html, width=220, height=280)
        popup = folium.Popup(iframe, parse_html=True)
        folium.Circle(location=(row['lat'],row['lng']),
                            radius=5,
                            color=colours[colour_index],
                            popup=popup,
                            fill=True).add_to(fg)
    colour_index += 1

folium.LayerControl().add_to(map)
map.keep_in_front(fg)
map.save('Middelfart.html')