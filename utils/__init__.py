import pandas as pd

def get_analistas(df_base,nucleo=None):
    if nucleo is not None:
        df_base = df_base[df_base['Núcleo'] == nucleo]

    analysts_columns = ['Analista 1','Analista 2', 'Analista 3', 'Analista 4']
    unique_analysts = pd.unique(df_base[analysts_columns].values.ravel('K'))

    unique_analysts = unique_analysts[~pd.isna(unique_analysts)]  
    analysts_df = pd.DataFrame(unique_analysts, columns=['Analista'])
    nucleus_mapping = {}
    for column in analysts_columns:
        for idx, row in df_base.iterrows():
            analyst = row[column]
            if pd.notna(analyst) and analyst not in nucleus_mapping:
                nucleus_mapping[analyst] = row['Núcleo']

    # Add the nucleus information to the analysts dataframe
    analysts_df['Núcleo'] = analysts_df['Analista'].map(nucleus_mapping)
    return analysts_df


def generate_pcp(df_base,nucleo=None,membro=None):
    if nucleo is not None:
        df_base = df_base[df_base['Núcleo'] == nucleo]

    if membro is not None:
        condicoes = (
            (df_base['Analista 1'] == membro) |
            (df_base['Analista 2'] == membro) |
            (df_base['Analista 3'] == membro) |
            (df_base['Analista 4'] == membro)
        )
        df_base = df_base[condicoes]

    
    df_base['Início Real'] = pd.to_datetime(df_base['Início Real'], errors='coerce')
    df_base['Fim Previsto'] = pd.to_datetime(df_base['Fim Previsto'], errors='coerce')
    start_date = df_base['Início Real'].min()
    end_date = df_base['Fim Previsto'].max()

    pacing_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    pacing_table = pd.DataFrame(pacing_dates, columns=['Data'])

    executing_projects = df_base[df_base['Status'].isin(['Executando','Concluído', 'Concluindo Pendências'])]

    pacing_table['Projeto por Analista'] = [{} for _ in range(len(pacing_table))]

    analyst_columns = ['Analista 1','Analista 2', 'Analista 3', 'Analista 4']

    for _, project in executing_projects.iterrows():
        start = project['Início Real']
        
        if project['Status'] is 'Executando' or project['Status'] is 'Concluindo Pendências':
            end = project['Fim Previsto']
        elif project['Status'] is 'Concluído':
            end = project['Fim Real']
        else:
            end = project['Fim Previsto']
        project_name = project['Projeto']
        if pd.notna(start) and pd.notna(end) and end >= start:
            involved_analysts = project[analyst_columns].dropna().unique()
            for day in pacing_table.loc[(pacing_table['Data'] >= start) & (pacing_table['Data'] <= end), 'Data']:
                for analyst in involved_analysts:
                    if analyst in pacing_table.loc[pacing_table['Data'] == day, 'Projeto por Analista'].values[0]:
                        pacing_table.loc[pacing_table['Data'] == day, 'Projeto por Analista'].values[0][analyst].append(project_name)
                    else:
                        pacing_table.loc[pacing_table['Data'] == day, 'Projeto por Analista'].values[0][analyst] = [project_name]

    return pacing_table

def calculate_projects_per_analyst(daily_dict):
        if not daily_dict:
            return 0  
        all_projects = set()
        all_analysts = set()
        
        for analyst, projects in daily_dict.items():
            all_analysts.add(analyst)
            all_projects.update(projects)
        
        if len(all_analysts) == 0:
            return 0  
        return len(all_projects) / len(all_analysts)

def get_base():
    df_base = pd.read_excel('base/PCP.xlsx',sheet_name='Base')
    return df_base

def count_unique_projects(project_dict):
    unique_projects = set()
    for projects in project_dict.values():
        unique_projects.update(projects)
    return len(unique_projects)
