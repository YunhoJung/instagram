from django import template

register = template.Library()


@register.filter
def query_string(q):
    # ret = '?'
    # for k, v_list in q.lists():
    #     for v in v_list:
    #         ret += '&{}={}'.format(k, v)
    return '?' + '&'.join(['{}={}'.format(k, v) for k, v_list in q.lists() for v in v_list])
