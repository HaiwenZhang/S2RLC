# S2RLC scripts Readme

## Requrements
Python 3

## Install Python Library requrements

``` bash
pip install -r requirements.txt
```

## How to use s2rlc scripts

``` bash
python3 s2rlc.py -s demo.s22p -r ./results.xlsx
```

"-s" is S parameter Touchstone file path
"-r" RLC result excel file path

After run this scripts, it will create excel files.
For sheet on file, first row is frequency, first column is S parameter port name.
ESR unit is Ohm, ESL unit is nH, ESC unit is pF