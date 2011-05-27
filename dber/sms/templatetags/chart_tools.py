from django import template

register = template.Library()

chart_begin = '''
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load("visualization", "1", {packages:["corechart"]});
'''

chart_end = '</script>'

@register.tag
def chart(parser, token):
    nodelist = parser.parse(('endchart',))
    parser.delete_first_token()
    return ChartNode(nodelist)

class ChartNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        output = chart_begin + output + chart_end
        return output

@register.inclusion_tag('sms/chart.html')
def prepare_chart(chart):
    return {'chart': chart}

@register.inclusion_tag('sms/charts.html')
def prepare_charts(charts):
    return {'charts': charts}
    
@register.simple_tag
def draw_chart(chart):
    if chart['data']['rows'] and chart['data']['columns']:
        return "<div id=%s></div>" % chart['id']
    else:
        return "<p>No dataset for %s</p>" % chart['id']
