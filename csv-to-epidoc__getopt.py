import requests as rq
import pandas as pd
import json
import io
import getopt
import sys

config = ""
outputpath = ""

try:
    opts, args = getopt.getopt(sys.argv[1:],"hc:o:",["configfile=","outputpath="])
except getopt.GetoptError:
    print('csv-to-epidoc.py -c <configfile> -o <outputpath>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('csv-to-epidoc.py -c <configfile> -o <outputpath>')
        sys.exit()
    elif opt in ("-c", "--configfile"):
        config = arg
    elif opt in ("-o", "--outputpath"):
        outputpath = arg

def handle(config):
    with open(config, 'r') as f:
        jsonfile = f.read()

    config = json.loads(jsonfile)

    _map = {
            'title': 'default',
            'editor': 'default',
            'authority': 'default',
            'filename': 'default',
            'license': 'default',
            'settlement': 'default',
            'repository': 'default',
            'idno': 'default',
            'objectType': 'default',
            'material': 'default',
            'dimensions': 'default',
            'handDesc': 'default',
            'scriptDesc': 'default',
            'decoDesc': 'default',
            'originDate': 'default',
            'originPlace': 'default',
            'listPerson': 'default',
            'langUsage': 'default',
            'facsimile': 'default',
            'transcription': 'default',
            'translation': 'default',
            'description': 'default',
            'commentary': 'default',
            'apparatus': 'default',
            'bibliography': 'default',
        }

    for k,v in config['map'].items():
        if k in _map.keys():
            _map[k] = v

    xml_files = []

    for url in config["csv"]:
        r = rq.get(url)
        df = pd.read_csv(io.StringIO(r.text), sep=config["sep"])
        df['default'] = 'no mapping'

        for _, row in df.iterrows():
            newline = "\n"
            template = f"""<?xml version="1.0" encoding="UTF-8"?>
        <?xml-model href="http://www.stoa.org/epidoc/schema/8.19/tei-epidoc.rng" schematypens="http://relaxng.org/ns/structure/1.0"?>
        <?xml-model href="http://www.stoa.org/epidoc/schema/8.19/tei-epidoc.rng" schematypens="http://purl.oclc.org/dsdl/schematron"?>
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                    <fileDesc>
                        <titleStmt>
                            <title>{row[_map['title']]}</title>
                            <editor>{row[_map['editor']]}</editor>
                        </titleStmt>
                        <publicationStmt>
                            <authority>{row[_map['authority']]}</authority>
                            <idno type="filename">{row[_map['filename']]}.xml</idno>
                            <availability status="free">
                                <licence target="">This file is provided under a {row[_map['license']]}. Please follow the URL to obtain further information about the license.</licence>
                            </availability>
                        </publicationStmt>
                        <sourceDesc>
                            <msDesc>
                                <msIdentifier>
                                    <settlement>{row[_map['settlement']]}</settlement>
                                    <repository>{row[_map['repository']]}</repository>
                                    <idno type="URI">{row[_map['idno']]}</idno>
                                </msIdentifier>
                                <physDesc>
                                    <objectDesc>
                                        <supportDesc>
                                            <support>
                                                <objectType>{row[_map['objectType']]}</objectType>
                                                <material>{row[_map['material']]}</material>
                                                <dimensions>
                                                    {row[_map['dimensions']]}
                                                </dimensions>
                                            </support>
                                        </supportDesc>
                                    </objectDesc>
                                    <handDesc>
                                        {(lambda lst: newline.join([ f'<handNote>{item}</handNote>' for item in lst.split(newline)]))(row[_map['handDesc']])}
                                    </handDesc>
                                    <scriptDesc>
                                        {(lambda lst: newline.join([ f'<scriptNote>{item}</scriptNote>' for item in lst.split(newline)]))(row[_map['scriptDesc']])}
                                    </scriptDesc>
                                    <decoDesc>
                                        {(lambda lst: newline.join([ f'<decoNote>{item}</decoNote>' for item in lst.split(newline)]))(row[_map['decoDesc']])}
                                    </decoDesc>
                                </physDesc>
                                <history>
                                    <origin>
                                        <origDate>{row[_map['originDate']]}</origDate>
                                        <origPlace>
                                            <placeName>{row[_map['originPlace']]}</placeName>
                                        </origPlace>
                                    </origin>
                                </history>
                            </msDesc>
                        </sourceDesc>
                    </fileDesc>
                    <profileDesc>
                        <particDesc>
                            <listPerson>
                                {row[_map['listPerson']]}
                            </listPerson>
                            <listRelation>
                                <relation name="" mutual=""/>
                            </listRelation>
                        </particDesc>
                        <langUsage>
                            {row[_map['langUsage']]}
                        </langUsage>
                    </profileDesc>
                </teiHeader>
                <facsimile>
                {row[_map['facsimile']]}
                </facsimile>
                <text>
                    <body>
                        <div type="edition" xml:space="default">
                            <div type="textpart" subtype="front" n="1" xml:lang="">
                                <ab>
                                    {row[_map['transcription']]}
                                </ab>
                            </div>
                        </div>
                        <div type="translation">
                            <div type="textpart" n="1">
                                <p>
                                    {row[_map['translation']]}
                                </p>
                            </div>
                        </div>
                        <div type="commentary" subtype="description">
                            {row[_map['description']]}
                        </div>
                        <div type="commentary" subtype="commentary">
                            {row[_map['commentary']]}
                        </div>
                        <div type="apparatus" subtype="edition">
                            <listApp n="1">
                                {row[_map['apparatus']]}
                            </listApp>
                        </div>
                        <div type="bibliography">
                            <listBibl>
                                {row[_map['bibliography']]}
                            </listBibl>
                        </div>
                    </body>
                </text>
            </TEI>"""
            xml_files.append(template)

    #out = json.dumps({ 'xml': xml_files })

    for index, xml in enumerate(xml_files):
        with open(f'./{outputpath}/epidoc_{str(index+1).zfill(4)}.xml', 'w') as f:
            f.write(xml)

if (config and outputpath):
    handle(config)