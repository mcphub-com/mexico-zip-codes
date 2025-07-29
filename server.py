import requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")

__rapidapi_url__ = 'https://rapidapi.com/acrogenesis-llc-api/api/mexico-zip-codes'

mcp = FastMCP('mexico-zip-codes')

@mcp.tool()
def search_zip_codes(codigo_postal: Annotated[str, Field(description='Part of a zip code')],
                     limit: Annotated[Union[int, float, None], Field(description='Default: 10')] = None) -> dict: 
    '''Search for valid zip codes with starting digits'''
    url = 'https://mexico-zip-codes.p.rapidapi.com/buscar/'
    headers = {'x-rapidapi-host': 'mexico-zip-codes.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'codigo_postal': codigo_postal,
        'limit': limit,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def search_zip_code_by_colonia_municipio_and_estado(estado: Annotated[str, Field(description='')],
                                                    municipio: Annotated[str, Field(description='')],
                                                    colonia: Annotated[Union[str, None], Field(description='')] = None,
                                                    limit: Annotated[Union[int, float, None], Field(description='Default: 10')] = None) -> dict: 
    '''Get all the zip codes for a given Colonia (optional), Municipio, and Estado'''
    url = 'https://mexico-zip-codes.p.rapidapi.com/buscar_por_ubicacion'
    headers = {'x-rapidapi-host': 'mexico-zip-codes.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'estado': estado,
        'municipio': municipio,
        'colonia': colonia,
        'limit': limit,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def zip_code_information(zip_code: Annotated[str, Field(description='A zip code')]) -> dict: 
    '''Retrieves the information of a particular zip code'''
    url = 'https://mexico-zip-codes.p.rapidapi.com/codigo_postal/64630'
    headers = {'x-rapidapi-host': 'mexico-zip-codes.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zip_code': zip_code,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()



if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
