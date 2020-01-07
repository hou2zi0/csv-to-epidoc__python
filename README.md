# csv-to-epidoc__python
Command line tool that converts CSV files to EpiDoc-XML.

## Configfile
The CLI-tool expects a configuration file with the following content:

```json
{
    "csv": [
            "https://hou2zi0.github.io/csv-to-epidoc/data/files/epidat.csv"
        ],
    "sep": "|",
    "map": {
    "title": "Inventory_Number",
    "handDesc": "Hands"
    }
}
```
* `csv` contains a list of URL pointing to CSV files containing the epigraphic data. It is important to know that all CSV files contained in a single CLI call must use the same separator.
* `sep` contains the cell separator character.
* `map` contains a mapping that specifies the mapping of the CSVs columns headers (values) to their respective counterpart within the EpiDoc-XML (key).
    * The mapping direction is `key <-- value == XML <-- CSV`.

Possible keys—representing fields in the XML— are (**may change in the future to be more consistent in regard to the element names in EpiDoc**):

* title
* editor
* authority
* filename
* license
* settlement
* repository
* idno
* objectType
* material
* dimensions
* handDesc
* scriptDesc
* decoDesc
* originDate
* originPlace
* listPerson
* langUsage
* facsimile
* transcription
* translation
* description
* commentary
* apparatus
* bibliography

## Calling the CLI script

```bash
python3 csv-to-epidoc.py -c configfile.json -o output
```

* `-c` specifies the path to the configfile (**required**)
* `-o` specifies the path to the output folder for the single XML files (**required**)

The script requires `Python3` and the following libraries:

* requests
* pandas
* json
* io
* getopt
* sys