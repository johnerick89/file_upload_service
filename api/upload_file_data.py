from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

import pandas as pd
import numpy as np
import json
import xmltodict
import xml.etree.ElementTree as ET

def get_rows(steps,count,file):
    if file.name.endswith('.csv'):
        if count ==0:
            df = pd.read_csv(file, nrows=steps)
        else: 
            df = pd.read_csv(file, skiprows=steps*count, nrows=steps)
    elif file.name.endswith('.txt'):
            if count == 0:
                df = pd.read_csv(file, sep=' ', nrows=steps)
            else: 
                df = pd.read_csv(file, sep=' ', skiprows=steps*count, nrows=steps)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
            if count == 0:
                df = pd.read_excel(file, nrows=steps)
            else: 
                df = pd.read_excel(file, skiprows=steps*count, nrows=steps)
    elif file.name.endswith('.json'):
            if count == 0:
                df = pd.read_json(file, lines=True, nrows=steps, orient='columns', encoding = "ISO-8859-1", dtype={'birth_date': str})
            else: 
                df = pd.read_json(file, lines=True, skiprows=steps*count, nrows=steps, orient='columns', encoding = "ISO-8859-1", dtype={'birth_date': str})
    elif file.name.endswith('.xml'):
            if count == 0:
                xml_data = file.read()
                root = ET.fromstring(xml_data)
                data = []
                for child in root:
                    row = []
                    for item in child:
                        row.append(item.text)
                    data.append(row)
                df = pd.DataFrame(data)
                df = df.head(steps)
            else:
                xml_data = file.read()
                root = ET.fromstring(xml_data)
                data = []
                for i, child in enumerate(root):
                    if i >= (count-1)*steps and i < count*steps:
                        row = []
                        for item in child:
                            row.append(item.text)
                        data.append(row)
                df = pd.DataFrame(data)
    return df

def handle_uploaded_file(file_path): 
    steps = 2000
    n = 0
    count = 0

    with open(file_path, "r") as file:
        while True:

            df = get_rows(steps,count, file)

            create_users(df)

            n+=len(df)
            
            count+=1
            
            if len(df)!=steps:
                break
    file.close()

    print(f"We have completed batch processing of the users data. Total number processed is: {n}") 

def create_users(df):
    # We are importing this here to fix circular imports issue
    from .models import User

    users = []
    for index, row in df.iterrows():
        user = User.objects.create(
            first_name=row[0],
            last_name=row[1],
            national_id=row[2],
            birth_date=row[3],
            address=row[4],
            country=row[5],
            phone_number=row[6],
            email=row[7]
        )
        # user.save()
        users.append(user)
                
    # We'll create users in batches to avoid making too many DB writes
    try:
        User.objects.bulk_create(users)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

