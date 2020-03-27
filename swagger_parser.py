import json
from pathlib import Path


def remove_dash(data):
    """
    In Java world we don't like dashes
    :param data: string with '-'
    :return: string without '-'
    """
    tmp_data = data.split('-')
    if len(tmp_data) != 0:
        result = ''
        cnt = 0
        for item in tmp_data:
            if cnt != 0:
                result += item[0].upper() + item[1:]
            else:
                result = item
            cnt += 1
        return result
    else:
        return data


def gen_java(data, property_name, docstring):
    """
    Java code magic here
    :param data: string with Java Name
    :param property_name: property name in cfg
    :param docstring: what you'll have in docstrings
    :return:
    """
    tmp_data = data.split('.')
    var_name = ''
    if len(tmp_data) != 0:
        cnt = 0
        for item in tmp_data:
            if cnt != 0:
                var_name += item[0].upper() + item[1:]
            else:
                var_name = item
            cnt += 1
    else:
        var_name = data
    result = "/**\n" + \
             '\n'.join([f' * {x}' for x in docstring]) + \
             "\n" + \
             "*/\n" + \
             f'public static String {var_name} = cfgProvider.getProperty("{property_name}", String.class);'
    return result


def get_uri_desc(tags, uri_tags, summary):
    """
    Method to generate data for docstrings
    :param tags:
    :param uri_tags:
    :param summary:
    :return:
    """
    result = []
    if len(uri_tags) == 0 or len(tags) == 0:
        result.append(summary)
    else:
        for uri_tag in uri_tags:
            for tag in tags:
                tag_name = tag.get('name', '')
                tag_des = tag.get('description', '')
                if tag_name == uri_tag:
                    result.append(tag_des)
                else:
                    continue
        result.append(summary)
    return result


def parse_json(json_name):
    """
    Parser parse
    :param json_name: file name to parse from resources
    :return: stdout
    """
    json_file = Path('resources', json_name)
    with json_file.open(encoding='utf-8') as fr:
        list_java = []
        data = json.load(fr)
        tags_desc = data.get('tags', [])
        print('--- start of property file ---')
        for path in data['paths']:
            for k, v in data['paths'][path].items():
                # check the deprecated flags, but....
                # if 'deprecated' in v.keys() and v['deprecated'] is False:
                name = path.replace('/', '.').replace('.api.', '').replace('{', '').replace('}', '.').replace('v3.',
                                                                                                              '').replace(
                    '..', '.')
                if str(name).startswith('.'):
                    name = name[1:]
                if not str(name).endswith('.'):
                    name += '.'
                java_name = f'{remove_dash(name)}{k}'
                property_name = f'{name}{k}'
                summary = v.get('summary', '')
                tags = v.get('tags', [])
                docstring = get_uri_desc(tags_desc, tags, summary)
                list_java.append(gen_java(java_name, property_name, docstring))
                print(f'{name}{k} = {path}')
        print('--- end of property file ---')
        print('--- start of java file ---')
        for item in list_java:
            print(item)
        print('--- end of java file ---')


def main():
    parse_json('example.api.json')


if __name__ == '__main__':
    main()
