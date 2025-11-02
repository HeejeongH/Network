import pandas as pd
import numpy as np
import networkx as nx # type: ignore
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pointbiserialr, chi2_contingency
import seaborn as sns
from scipy.stats import norm
import matplotlib.colors as mcolors
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'Arial' #'Malgun Gothic'

class DataPreprocessor:
    def __init__(self):
        self.short_term = {
            'Hypertension': 'HTN',
            'Diabetes Mellitus': 'DM',
            'Hyperlipidemia': 'HL',
            'Angina/Myocardial Infarction': 'AMI',
            'Stroke': 'Stroke',
            'Chronic kidney disease (eGFR<60)': 'CKD',
            'Obese': 'Obese',
            'Increased waist circumference': '△ WC',
            'Elevated blood pressure': '△ BP',
            'Impaired fasting glucose': 'IFG',
            'Elevated triglycerides': '△ TG',
            'Decreased HDL-C': '▽ HDL-C',
            'Systolic blood pressure (mmHg)': 'SBP',
            'Diastolic Blood Pressure (mmHg)': 'DBP',
            #'Fasting glucose (mg/dL)': 'FBS',
            'Triglycerides (mg/dL)': 'TG',
            #'HbA1c (%)': 'HBA1C',
            'HDL-C (mg/dL)': 'HDL-C.',
            'LDL-C (mg/dL)': 'LDL-C.',
            'eGFR (mL/min/1.73m2)': 'eGFR',
            'Weight (kg)': 'Weight',
            'BMI(kg/m2)': 'BMI',
            'Waist circumference (cm)': 'WC',
            'Physical activity': 'PA',
            'Alcohol Consumption': 'Alcohol',
            'Current smoking': 'Smoking',
            'Grain Products': 'Grain',
            'Protein Foods': 'Protein',
            'Vegetables': 'Vegetables',
            'Dairy Products': 'Dairy',
            'Fruits': 'Fruits',
            'Fried Foods': 'Fried',
            'High Fat Meat': 'High Fat\nMeat',
            'Processed Foods': 'Processed\nFoods',
            'Sugar-Sweetened Beverages': 'SSB',
            'Additional Salt Use': 'Add-Salt',
            'Salty Food Consumption': 'Salty\nFood',
            'Sweet Food Consumption': 'Sweet\nFood',
        }
        
        self.diet_cols = ['Grain', 'Protein', 'Vegetables', 'Fruits', 'Dairy', 'Sweet\nFood', 'Fried', 'High Fat\nMeat', 'Processed\nFoods', 'Salty\nFood', 'SSB', 'Add-Salt']
        self.life_cols = ['PA', 'Alcohol', 'Smoking']
        self.disease_cols = ['HTN', 'DM', 'HL', 'AMI', 'Stroke', 'CKD', 'Obese']
        self.mets_cols = ['△ WC', '△ BP', 'IFG', '△ TG', '▽ HDL-C']
        self.biomarker_cols = ['SBP', 'DBP', 'Weight', 'BMI', 'WC', 'TG', 'HDL-C.', 'LDL-C.', 'eGFR'] #, 'HBA1C', 'FBS'
        
        self.categorical_3 = self.diet_cols + ['PA', 'Alcohol']
        self.categorical_2 = ['Smoking'] + self.disease_cols + self.mets_cols
        self.continuous = self.biomarker_cols
    
    def load_and_prepare_data(self, file_path):
        total_df_only = pd.read_csv(file_path)
        total_df_only.rename(columns=self.short_term, inplace=True)
        return total_df_only
    
    def create_group_datasets(self, data):
        men_df = data[data['Sex'] == 'M']
        men_df_40 = men_df[men_df['Age'] < 40]
        men_df_50 = men_df[(men_df['Age'] >= 40) & (men_df['Age'] < 50)]
        men_df_65 = men_df[(men_df['Age'] >= 50) & (men_df['Age'] < 65)]
        men_df_99 = men_df[men_df['Age'] >= 65]

        women_df = data[data['Sex'] == 'F']
        women_df_40 = women_df[women_df['Age'] < 40]
        women_df_50 = women_df[(women_df['Age'] >= 40) & (women_df['Age'] < 50)]
        women_df_65 = women_df[(women_df['Age'] >= 50) & (women_df['Age'] < 65)]
        women_df_99 = women_df[women_df['Age'] >= 65]

        datasets = {
            'Total': data,
            'Men_All': men_df, 'Men_under40': men_df_40, 'Men_40-49': men_df_50,
            'Men_50-64': men_df_65, 'Men_65plus': men_df_99,
            'Women_All': women_df, 'Women_under40': women_df_40, 'Women_40-49': women_df_50,
            'Women_50-64': women_df_65, 'Women_65plus': women_df_99
        }
        return datasets

    def create_mets_comparison_datasets(self, data):
        """
        DM, AMI, Stroke, CKD가 모두 0인 대상자를 필터링하고,
        MetS 유무에 따라 그룹을 나눕니다.

        MetS는 5가지 요소 중 3가지 이상 해당 시 MetS로 간주
        """
        # DM, AMI, Stroke, CKD가 모두 0인 사람만 필터링
        filtered_data = data[
            (data['DM'] == 0) &
            (data['AMI'] == 0) &
            (data['Stroke'] == 0) &
            (data['CKD'] == 0)
        ].copy()

        # MetS 유무로 분리
        mets_positive = filtered_data[filtered_data['MetS'] == 1]
        mets_negative = filtered_data[filtered_data['MetS'] == 0]

        # 성별로 추가 분리
        datasets = {
            'MetS_Positive_Total': mets_positive,
            'MetS_Negative_Total': mets_negative,
            'MetS_Positive_Men': mets_positive[mets_positive['Sex'] == 'M'],
            'MetS_Negative_Men': mets_negative[mets_negative['Sex'] == 'M'],
            'MetS_Positive_Women': mets_positive[mets_positive['Sex'] == 'F'],
            'MetS_Negative_Women': mets_negative[mets_negative['Sex'] == 'F'],
        }

        # 성별 + 연령대로 추가 분리
        for gender, gender_code in [('Men', 'M'), ('Women', 'F')]:
            pos_gender = mets_positive[mets_positive['Sex'] == gender_code]
            neg_gender = mets_negative[mets_negative['Sex'] == gender_code]

            # 연령대별 분리
            datasets[f'MetS_Positive_{gender}_under40'] = pos_gender[pos_gender['Age'] < 40]
            datasets[f'MetS_Negative_{gender}_under40'] = neg_gender[neg_gender['Age'] < 40]

            datasets[f'MetS_Positive_{gender}_40-49'] = pos_gender[(pos_gender['Age'] >= 40) & (pos_gender['Age'] < 50)]
            datasets[f'MetS_Negative_{gender}_40-49'] = neg_gender[(neg_gender['Age'] >= 40) & (neg_gender['Age'] < 50)]

            datasets[f'MetS_Positive_{gender}_50-64'] = pos_gender[(pos_gender['Age'] >= 50) & (pos_gender['Age'] < 65)]
            datasets[f'MetS_Negative_{gender}_50-64'] = neg_gender[(neg_gender['Age'] >= 50) & (neg_gender['Age'] < 65)]

            datasets[f'MetS_Positive_{gender}_65plus'] = pos_gender[pos_gender['Age'] >= 65]
            datasets[f'MetS_Negative_{gender}_65plus'] = neg_gender[neg_gender['Age'] >= 65]

        return datasets, filtered_data

class CorrelationNetwork:
    def __init__(self, data_preprocessor):
        self.preprocessor = data_preprocessor
        self.categorical_2 = data_preprocessor.categorical_2
        self.categorical_3 = data_preprocessor.categorical_3
        self.continuous = data_preprocessor.continuous
    
    def calculate_correlation_matrix(self, data, col_groups, threshold=0.1, alpha=0.05):
        all_cols = []
        for group in col_groups:
            all_cols.extend(group)
        df = data[all_cols].dropna()
        
        corr_matrix = {}
        pval_matrix = {}
        
        for i in df.columns:
            corr_matrix[i] = {}
            pval_matrix[i] = {}
            for j in df.columns:
                if i != j:
                    if (i in self.categorical_2 or i in self.categorical_3) and \
                       (j in self.categorical_2 or j in self.categorical_3):
                        contingency = pd.crosstab(df[i], df[j])
                        chi2, p_val, _, _ = chi2_contingency(contingency)
                        n = contingency.sum().sum()
                        phi = np.sqrt(chi2 / n)
                        corr_matrix[i][j] = phi
                        pval_matrix[i][j] = p_val
                    elif ((i in self.categorical_2 or i in self.categorical_3) and j in self.continuous) or \
                         (i in self.continuous and (j in self.categorical_2 or j in self.categorical_3)):
                        corr, p_val = pointbiserialr(df[i], df[j])
                        corr_matrix[i][j] = corr
                        pval_matrix[i][j] = p_val
                    else:
                        corr, p_val = spearmanr(df[i], df[j])
                        corr_matrix[i][j] = corr
                        pval_matrix[i][j] = p_val
                else:
                    corr_matrix[i][j] = 1.0
                    pval_matrix[i][j] = 0.0
        
        return pd.DataFrame(corr_matrix), pd.DataFrame(pval_matrix)
    
    def create_correlation_network(self, corr_df, pval_df, col_groups, group_names, colors, sizes, threshold=0.1, alpha=0.05):
        G = nx.Graph()
        for i, group in enumerate(col_groups):
            for column in group:
                G.add_node(column, type=group_names[i], size=sizes[i], color=colors[i])
        for i in range(len(corr_df.columns)):
            for j in range(i+1, len(corr_df.columns)):
                col_i = corr_df.columns[i]
                col_j = corr_df.columns[j]

                is_diet_i = col_i in col_groups[0]
                is_diet_j = col_j in col_groups[0]
                is_health_i = col_i in col_groups[1]
                is_health_j = col_j in col_groups[1]

                if ((is_diet_i and is_health_j) or (is_health_i and is_diet_j)):
                    corr_value = corr_df.loc[col_i, col_j]
                    p_value = pval_df.loc[col_i, col_j]
                    if abs(corr_value) >= threshold and p_value < alpha:
                        G.add_edge(
                            col_i, col_j,
                            weight=abs(corr_value),
                            correlation=corr_value,
                            p_value=p_value
                        )
        return G

    def analyze_diet_correlation_patterns(self, data):
        diet_data = data[self.preprocessor.diet_cols].dropna()
        correlation_matrix = diet_data.corr(method='spearman')
        patterns = []
        for i in range(len(self.preprocessor.diet_cols)):
            for j in range(i+1, len(self.preprocessor.diet_cols)):
                food1, food2 = self.preprocessor.diet_cols[i], self.preprocessor.diet_cols[j]
                corr_val = correlation_matrix.loc[food1, food2]
                
                if abs(corr_val) >= 0.3:
                    pattern_type = 'Positive' if corr_val > 0 else 'Negative'
                elif abs(corr_val) <= 0.1:
                    pattern_type = 'Independent'
                else:
                    pattern_type = 'Moderate'
                
                patterns.append({
                    'Food_Group_1': food1,
                    'Food_Group_2': food2,
                    'Correlation': corr_val,
                    'Pattern_Type': pattern_type
                })
        
        return pd.DataFrame(patterns), correlation_matrix

class CooccurrenceNetwork:
    def __init__(self, data_preprocessor):
        self.diet_cols = data_preprocessor.diet_cols
    
    def create_cooccurrence_network(self, data, diet_quality_level, color, size, threshold_percent=0.2):
        if diet_quality_level == 'poor':
            value = 1
        elif diet_quality_level == 'intermediate':
            value = 3
        elif diet_quality_level == 'ideal':
            value = 5
        elif diet_quality_level == 'non_poor':
            # Poor가 아닌 것 (Intermediate + Ideal)
            value = 'non_poor'

        cooccur_matrix = {}
        for i, col_i in enumerate(self.diet_cols):
            cooccur_matrix[col_i] = {}
            for j, col_j in enumerate(self.diet_cols):
                if i != j:
                    if value == 'non_poor':
                        both_value = len(data[(data[col_i] != 1) & (data[col_j] != 1)])
                    else:
                        both_value = len(data[(data[col_i] == value) & (data[col_j] == value)])
                    cooccur_matrix[col_i][col_j] = both_value
                else:
                    if value == 'non_poor':
                        cooccur_matrix[col_i][col_j] = len(data[data[col_i] != 1])
                    else:
                        cooccur_matrix[col_i][col_j] = len(data[data[col_i] == value])

        cooccur_df = pd.DataFrame(cooccur_matrix)

        G = nx.Graph()
        for col in self.diet_cols:
            if value == 'non_poor':
                count = len(data[data[col] != 1])
            else:
                count = len(data[data[col] == value])
            G.add_node(col, size=size, count=count, color=color)

        all_cooccur_values = []
        for i in range(len(self.diet_cols)):
            for j in range(i+1, len(self.diet_cols)):
                all_cooccur_values.append(cooccur_df.loc[self.diet_cols[i], self.diet_cols[j]])

        threshold = np.percentile(all_cooccur_values, (1-threshold_percent)*100)

        for i in range(len(self.diet_cols)):
            for j in range(i+1, len(self.diet_cols)):
                col_i, col_j = self.diet_cols[i], self.diet_cols[j]
                cooccur_count = cooccur_df.loc[col_i, col_j]
                if cooccur_count >= threshold:
                    G.add_edge(col_i, col_j, weight=cooccur_count, count=cooccur_count)

        return G, cooccur_df

class CentralityAnalyzer:
    def calculate_centrality_measures(self, G):
        if len(G.nodes()) == 0:
            return {}, {}, {}
        
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        
        if nx.is_connected(G):
            print("Connected graph")
            eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
        else:
            print("Disconnected graph")
            try:
                eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
            except:
                eigenvector_centrality = {node: 0 for node in G.nodes()}
        
        return degree_centrality, betweenness_centrality, eigenvector_centrality
    
    def calculate_network_properties(self, G):
        if len(G.nodes()) == 0:
            return {}
        
        properties = {}
        properties['nodes'] = G.number_of_nodes()
        properties['edges'] = G.number_of_edges()
        properties['density'] = nx.density(G)
        properties['clustering'] = nx.average_clustering(G)
        
        if nx.is_connected(G):
            properties['avg_path_length'] = nx.average_shortest_path_length(G)
            properties['diameter'] = nx.diameter(G)
        else:
            largest_cc = max(nx.connected_components(G), key=len)
            G_cc = G.subgraph(largest_cc)
            if len(G_cc) > 1:
                properties['avg_path_length'] = nx.average_shortest_path_length(G_cc)
                properties['diameter'] = nx.diameter(G_cc)
            else:
                properties['avg_path_length'] = 0
                properties['diameter'] = 0
        
        properties['components'] = nx.number_connected_components(G)
        return properties
    
    def analyze_network_centrality_from_graphs(self, basic_networks):
        centrality_results = {}
        
        for group_name, networks in basic_networks.items():
            group_results = {}
            
            cooccurrence_centrality = {}
            for quality in ['poor', 'non_poor']:
                print(f"Analyzing {group_name} - Co-occurrence ({quality})")
                G = networks['cooccurrence'][quality]['graph']
                degree_cent, between_cent, eigen_cent = self.calculate_centrality_measures(G)
                network_props = self.calculate_network_properties(G)

                cooccurrence_centrality[quality] = {
                    'degree_centrality': degree_cent,
                    'betweenness_centrality': between_cent,
                    'eigenvector_centrality': eigen_cent,
                    'network_properties': network_props
                }
            group_results['cooccurrence'] = cooccurrence_centrality
            
            health_centrality = {}
            for network_type in ['diet_disease', 'diet_mets', 'diet_biomarker']:
                print(f"Analyzing {group_name} - Health Network ({network_type})")
                G = networks['health'][network_type]['graph']
                degree_cent, between_cent, eigen_cent = self.calculate_centrality_measures(G)
                network_props = self.calculate_network_properties(G)
                
                health_centrality[network_type] = {
                    'degree_centrality': degree_cent,
                    'betweenness_centrality': between_cent,
                    'eigenvector_centrality': eigen_cent,
                    'network_properties': network_props
                }
            group_results['health'] = health_centrality
            centrality_results[group_name] = group_results
        
        return centrality_results
    
    def identify_hub_nodes(self, centrality_results, top_n=5):
        hub_analysis = {}
        
        for group_name, result in centrality_results.items():
            hubs = {}
            
            if 'degree_centrality' in result:
                degree_hubs = sorted(result['degree_centrality'].items(), key=lambda x: x[1], reverse=True)[:top_n]
                hubs['degree_hubs'] = degree_hubs
            
            if 'betweenness_centrality' in result:
                bridge_nodes = sorted(result['betweenness_centrality'].items(), key=lambda x: x[1], reverse=True)[:top_n]
                hubs['bridge_nodes'] = bridge_nodes
            
            if 'eigenvector_centrality' in result:
                influence_nodes = sorted(result['eigenvector_centrality'].items(), key=lambda x: x[1], reverse=True)[:top_n]
                hubs['influence_nodes'] = influence_nodes
            
            hub_analysis[group_name] = hubs
        
        return hub_analysis

    def calculate_fishers_z_and_cohens_d(self, centrality_results):
        advanced_gender_analysis = []
        
        for network_type in ['diet_disease', 'diet_mets', 'diet_biomarker']:
            men_data = centrality_results.get('Men_All', {}).get('health', {}).get(network_type, {})
            women_data = centrality_results.get('Women_All', {}).get('health', {}).get(network_type, {})
            
            if men_data and women_data:
                men_degree = men_data.get('degree_centrality', {})
                women_degree = women_data.get('degree_centrality', {})
                
                all_nodes = set(men_degree.keys()) | set(women_degree.keys())
                
                for node in all_nodes:
                    men_score = men_degree.get(node, 0)
                    women_score = women_degree.get(node, 0)
                    difference = men_score - women_score
                    
                    # Fisher's Z transformation (정규화된 차이)
                    pooled_mean = (men_score + women_score) / 2
                    fishers_z = np.arctanh(np.clip(difference / (pooled_mean + 0.001), -0.99, 0.99))
                    
                    # Cohen's d 계산 (효과 크기)
                    pooled_std = np.sqrt(((men_score - pooled_mean)**2 + (women_score - pooled_mean)**2) / 2)
                    cohens_d = difference / (pooled_std + 0.001) if pooled_std > 0 else 0
                    
                    # 통계적 유의성 (간단한 z-test 근사)
                    z_score = fishers_z
                    p_value = 2 * (1 - norm.cdf(abs(z_score)))
                    
                    advanced_gender_analysis.append({
                        'Network_Type': network_type,
                        'Node': node,
                        'Men_Centrality': men_score,
                        'Women_Centrality': women_score,
                        'Difference': difference,
                        'Fishers_Z': fishers_z,
                        'Cohens_D': cohens_d,
                        'P_Value': p_value,
                        'Significant': p_value < 0.05,
                        'Effect_Size': 'Large' if abs(cohens_d) >= 0.8 else 'Medium' if abs(cohens_d) >= 0.5 else 'Small'
                    })
        
        return pd.DataFrame(advanced_gender_analysis)

    def analyze_lifecycle_network_evolution(self, centrality_results):
        evolution_analysis = []
        
        age_groups = ['under40', '40-49', '50-64', '65plus']
        age_order = {age: i for i, age in enumerate(age_groups)}
        
        for network_type in ['diet_disease', 'diet_mets', 'diet_biomarker']:
            for gender in ['Men', 'Women']:
                
                age_data = []
                for age_group in age_groups:
                    group_key = f"{gender}_{age_group}"
                    if group_key in centrality_results:
                        group_data = centrality_results[group_key].get('health', {}).get(network_type, {})
                        if group_data:
                            props = group_data.get('network_properties', {})
                            degree_centrality = group_data.get('degree_centrality', {})
                            
                            age_data.append({
                                'age_group': age_group,
                                'age_order': age_order[age_group],
                                'density': props.get('density', 0),
                                'clustering': props.get('clustering', 0),
                                'avg_degree_centrality': np.mean(list(degree_centrality.values())) if degree_centrality else 0,
                                'nodes': props.get('nodes', 0),
                                'edges': props.get('edges', 0)
                            })
                
                if len(age_data) >= 2:
                    age_df = pd.DataFrame(age_data)
                    
                    for metric in ['density', 'clustering', 'avg_degree_centrality']:
                        if metric in age_df.columns:
                            correlation = np.corrcoef(age_df['age_order'], age_df[metric])[0,1]
                            
                            if len(age_df) >= 2:
                                first_value = age_df.iloc[0][metric]
                                last_value = age_df.iloc[-1][metric]
                                change_rate = (last_value - first_value) / (first_value + 0.001) * 100
                            else:
                                change_rate = 0
                            
                            evolution_analysis.append({
                                'Network_Type': network_type,
                                'Gender': gender,
                                'Metric': metric,
                                'Age_Correlation': correlation,
                                'Change_Rate_Percent': change_rate,
                                'Trend_Direction': 'Increasing' if correlation > 0.1 else 'Decreasing' if correlation < -0.1 else 'Stable',
                                'First_Age_Value': age_df.iloc[0][metric] if len(age_df) > 0 else 0,
                                'Last_Age_Value': age_df.iloc[-1][metric] if len(age_df) > 0 else 0
                            })
        
        return pd.DataFrame(evolution_analysis)

class NetworkComparator:
    def compare_centrality_across_groups(self, centrality_results, centrality_type='degree_centrality'):
        comparison_df = pd.DataFrame()
        
        for group_name, result in centrality_results.items():
            if centrality_type in result:
                centrality_data = result[centrality_type]
                temp_df = pd.DataFrame(list(centrality_data.items()),
                                     columns=['variable', f'{group_name}'])
                if comparison_df.empty:
                    comparison_df = temp_df
                else:
                    comparison_df = comparison_df.merge(temp_df, on='variable', how='outer')
        
        comparison_df = comparison_df.set_index('variable').fillna(0)
        return comparison_df
    
    def compare_network_properties(self, centrality_results):
        properties_df = pd.DataFrame()
        
        for group_name, result in centrality_results.items():
            if 'network_properties' in result:
                props = result['network_properties']
                temp_df = pd.DataFrame([props])
                temp_df['group'] = group_name
                properties_df = pd.concat([properties_df, temp_df], ignore_index=True)
        
        return properties_df.set_index('group')

class NetworkVisualizer:
    def __init__(self):
        self.node_sizes = {
            'cooccurence': 3000,
            'cooccurence_w': 3000,
            'correlation': 1000,
            'correlation_w': 2000,
        }

        self.edge_colors = {
            'positive_correlation': "#54B554",
            'negative_correlation': "#DC5C42",
            'neutral': '#808080',
            'default_cooccurrence': "#41555E"
        }

        self.edge_weight = {
            'cooccurence': 3.0,
            'correlation': 3.0,
            'alpha_scale': 0.7
        }

        self.font_size = 16

    def plot_network(self, G, ax, title, centrality_results=None):
        pos = nx.circular_layout(G)

        degree_cent = centrality_results['degree_centrality']
        between_cent = centrality_results['betweenness_centrality']

        # 노드 크기: degree centrality 기반 (제곱 스케일링으로 차이 강조)
        node_sizes = []
        degree_values = [degree_cent.get(node, 0) for node in G.nodes()]
        max_degree = max(degree_values) if degree_values else 1

        for node in G.nodes():
            degree_val = degree_cent.get(node, 0)
            # 제곱 스케일링으로 차이 강조
            normalized_degree = (degree_val / max_degree) ** 2 if max_degree > 0 else 0

            if 'Co-occurrence' in title or 'Poor Diet' in title or 'Ideal Diet' in title:
                size = self.node_sizes['cooccurence'] * 0.5 + normalized_degree * self.node_sizes['cooccurence_w'] * 2
            else:
                size = self.node_sizes['correlation'] * 0.5 + normalized_degree * self.node_sizes['correlation_w'] * 2
            node_sizes.append(size)

        # 노드 색상: betweenness centrality 기반으로 색상 강도 조절 (지수 스케일링)
        node_colors = []
        between_values = [between_cent.get(node, 0) for node in G.nodes()]
        max_between = max(between_values) if between_values else 0.1

        for node in G.nodes():
            between_val = between_cent.get(node, 0)
            base_color = G.nodes[node]['color']

            # 지수 스케일링으로 차이 강조 (alpha: 0.2 ~ 1.0)
            normalized_between = (between_val / max_between) ** 1.5 if max_between > 0 else 0
            alpha = 0.2 + normalized_between * 0.8
            color = mcolors.to_rgba(base_color, alpha)
            node_colors.append(color)

        # 엣지 처리
        if G.number_of_edges() > 0:
            edge_weights = [G.edges[edge]['weight'] for edge in G.edges()]
            max_weight = max(edge_weights) if edge_weights else 1
            
            if 'Co-occurrence' in title or 'Poor Diet' in title or 'Ideal Diet' in title:
                edge_widths = [w / max_weight * self.edge_weight['cooccurence'] + 0.1 for w in edge_weights]
                edge_alphas = [w / max_weight * self.edge_weight['alpha_scale'] for w in edge_weights]
                
                base_color = self.edge_colors['default_cooccurrence']
                color_hex = mcolors.to_rgba(base_color, alpha)
                edge_colors_alpha = [(color_hex[0], color_hex[1], color_hex[2], alpha) for alpha in edge_alphas]
            else:
                edge_widths = [w / max_weight * self.edge_weight['correlation'] + 1 for w in edge_weights]
                edge_colors_alpha = []
                
                for edge in G.edges():
                    correlation = G.edges[edge].get('correlation', 0)
                    weight = G.edges[edge]['weight']
                    alpha = weight / max_weight * self.edge_weight['alpha_scale']

                    if correlation > 0.01:  # 작은 임계값 설정
                        base_color = self.edge_colors['positive_correlation']
                    elif correlation < -0.01:
                        base_color = self.edge_colors['negative_correlation']
                    else:
                        base_color = self.edge_colors['neutral']
                    
                    color_hex = mcolors.to_rgba(base_color, alpha)
                    color = (color_hex[0], color_hex[1], color_hex[2], alpha)
                    edge_colors_alpha.append(color)

        else:
            edge_widths = []
            edge_colors_alpha = []

        nx.draw(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes, edge_color=edge_colors_alpha, 
                width=edge_widths, with_labels=True, font_size=self.font_size, font_weight='bold')
        
        ax.set_title(title, fontsize=23)
        ax.set_xticks([])
        ax.set_yticks([])

    def plot_centrality_comparison(self, centrality_results, centrality_type='degree_centrality', top_n=10):
        comparator = NetworkComparator()
        comparison_df = comparator.compare_centrality_across_groups(centrality_results, centrality_type)
        
        comparison_df['mean'] = comparison_df.mean(axis=1)
        top_variables = comparison_df.nlargest(top_n, 'mean').drop('mean', axis=1)
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(top_variables.T, annot=True, fmt='.3f', cmap='YlOrRd')
        plt.title(f'Top {top_n} Variables by {centrality_type.replace("_", " ").title()}')
        plt.ylabel('Groups')
        plt.xlabel('Variables')
        plt.tight_layout()
        return plt.gcf()
    
    def plot_network_properties_comparison(self, properties_df):
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        numeric_cols = properties_df.select_dtypes(include=[np.number]).columns
        
        for i, col in enumerate(numeric_cols[:6]):
            if i < len(axes):
                properties_df[col].plot(kind='bar', ax=axes[i])
                axes[i].set_title(col.replace('_', ' ').title())
                axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig

class NetworkAnalyzer:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.correlation_network = CorrelationNetwork(self.preprocessor)
        self.cooccurrence_network = CooccurrenceNetwork(self.preprocessor)
        self.centrality_analyzer = CentralityAnalyzer()
        self.comparator = NetworkComparator()
        self.visualizer = NetworkVisualizer()

        self.node_colors = {
            'diet': "#CD97E1",
            'disease': '#FFA500',
            'mets': "#B6F080",
            'biomarker': "#F6E688",
            'poor_diet': "#E58282",
            'non_poor_diet': "#83C7D3"
        }

    def create_basic_networks(self, data_dict):
        basic_networks = {}
        
        for name, data in data_dict.items():
            networks = {}
            
            # 식품군 동시발생 네트워크
            cooccurrence = {}
            for quality in ['poor', 'non_poor']:
                color_key = f'{quality}_diet'
                G, cooccur_df = self.cooccurrence_network.create_cooccurrence_network(
                    data, quality,
                    color=self.node_colors[color_key],
                    size=300,
                    threshold_percent=0.2)

                cooccurrence[quality] = {'graph': G, 'matrix': cooccur_df}
            networks['cooccurrence'] = cooccurrence
            
            # 식품군-건강지표 네트워크
            health_networks = {}
            
            ## Diet-Disease 네트워크
            corr_df, pval_df = self.correlation_network.calculate_correlation_matrix(
                data, [self.preprocessor.diet_cols, self.preprocessor.disease_cols])
            G = self.correlation_network.create_correlation_network(
                corr_df, pval_df, 
                [self.preprocessor.diet_cols, self.preprocessor.disease_cols],
                ['diet', 'disease'], 
                [self.node_colors['diet'], self.node_colors['disease']], 
                [300, 300], 
                threshold=0.01)
            health_networks['diet_disease'] = {'graph': G, 'correlation': corr_df, 'pvalue': pval_df}
            
            ## Diet-MetS 네트워크
            corr_df, pval_df = self.correlation_network.calculate_correlation_matrix(
                data, [self.preprocessor.diet_cols, self.preprocessor.mets_cols])
            G = self.correlation_network.create_correlation_network(
                corr_df, pval_df, 
                [self.preprocessor.diet_cols, self.preprocessor.mets_cols],
                ['diet', 'mets'], 
                [self.node_colors['diet'], self.node_colors['mets']], 
                [300, 300], 
                threshold=0.01)
            health_networks['diet_mets'] = {'graph': G, 'correlation': corr_df, 'pvalue': pval_df}
            
            ## Diet-Biomarker 네트워크
            corr_df, pval_df = self.correlation_network.calculate_correlation_matrix(
                data, [self.preprocessor.diet_cols, self.preprocessor.biomarker_cols])
            G = self.correlation_network.create_correlation_network(
                corr_df, pval_df, 
                [self.preprocessor.diet_cols, self.preprocessor.biomarker_cols],
                ['diet', 'biomarker'], 
                [self.node_colors['diet'], self.node_colors['biomarker']], 
                [300, 300], 
                threshold=0.05)
            health_networks['diet_biomarker'] = {'graph': G, 'correlation': corr_df, 'pvalue': pval_df}
            
            networks['health'] = health_networks
            basic_networks[name] = networks
        
        return basic_networks
    
    def create_optimized_plots(self, basic_networks, centrality_results, save_path='../result/'):
        import os

        # 폴더 구조 생성
        diet_path = os.path.join(save_path, '식습관')
        health_path = os.path.join(save_path, '건강')

        diet_total_path = os.path.join(diet_path, '전체')
        diet_gender_path = os.path.join(diet_path, '성별')
        diet_age_path = os.path.join(diet_path, '성별+나이')

        health_total_path = os.path.join(health_path, '전체')
        health_gender_path = os.path.join(health_path, '성별')
        health_age_path = os.path.join(health_path, '성별+나이')

        for path in [diet_total_path, diet_gender_path, diet_age_path,
                     health_total_path, health_gender_path, health_age_path]:
            os.makedirs(path, exist_ok=True)

        # Total_diet_cooccurrence
        networks = basic_networks['Total']
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        fig.suptitle(f'Diet Co-occurrence Networks\n', fontsize=30, fontweight='bold')

        centrality_poor = centrality_results.get('Total', {}).get('cooccurrence', {}).get('poor', {})
        centrality_non_poor = centrality_results.get('Total', {}).get('cooccurrence', {}).get('non_poor', {})

        self.visualizer.plot_network(
            networks['cooccurrence']['poor']['graph'], axes[0],
            'Poor Diet Co-occurrence', centrality_results=centrality_poor)
        self.visualizer.plot_network(
            networks['cooccurrence']['non_poor']['graph'], axes[1],
            'Non-Poor Diet Co-occurrence', centrality_results=centrality_non_poor)

        plt.tight_layout()
        plt.savefig(os.path.join(diet_total_path, 'Total_diet_cooccurrence_network.png'),
                    dpi=300, bbox_inches='tight')
        plt.close()

        # Total_diet_health_correlation
        fig, axes = plt.subplots(1, 3, figsize=(30, 10))
        fig.suptitle('Diet-Health Correlation Networks\n', fontsize=30, fontweight='bold')

        disease_graph = networks['health']['diet_disease']['graph']
        disease_centrality = centrality_results['Total']['health']['diet_disease']
        disease_density = disease_centrality['network_properties'].get('density', 0)

        mets_graph = networks['health']['diet_mets']['graph']
        mets_centrality = centrality_results['Total']['health']['diet_mets']
        mets_density = mets_centrality['network_properties'].get('density', 0)

        biomarker_graph = networks['health']['diet_biomarker']['graph']
        biomarker_centrality = centrality_results['Total']['health']['diet_biomarker']
        biomarker_density = biomarker_centrality['network_properties'].get('density', 0)

        self.visualizer.plot_network(
            biomarker_graph, axes[0], f'Diet-Biomarker\nDensity: {biomarker_density:.3f}',
            centrality_results=biomarker_centrality)

        self.visualizer.plot_network(
            mets_graph, axes[1], f'Diet-MetS\nDensity: {mets_density:.3f}',
            centrality_results=mets_centrality)

        self.visualizer.plot_network(
            disease_graph, axes[2], f'Diet-Disease\nDensity: {disease_density:.3f}',
            centrality_results=disease_centrality)

        plt.tight_layout()
        plt.savefig(os.path.join(health_total_path, 'Total_diet_health_correlation_network.png'),
                    dpi=300, bbox_inches='tight')
        plt.close()

        # Gender_comparison
        self.create_gender_comparison_plots(basic_networks, centrality_results, diet_gender_path, health_gender_path)

        # Gender_Age_comparison
        self.create_diet_age_progression_plots(basic_networks, centrality_results, diet_age_path)
        self.create_health_diet_age_progression_plots(basic_networks, centrality_results, health_age_path)

    def create_diet_age_progression_plots(self, basic_networks, centrality_results, save_path='../result/'):
        age_groups = ['under40', '40-49', '50-64', '65plus']
        age_labels = ['<40', '40-49', '50-64', '65≤']
        
        for gender in ['Men', 'Women']:
            fig, axes = plt.subplots(2, 4, figsize=(32, 18))
            fig.suptitle(f'Diet Co-occurrence Networks (Age Progression): {gender}\n', 
                         fontsize=30, fontweight='bold')
            
            qualities = ['poor', 'non_poor']
            quality_names = ['Poor Diet', 'Non-Poor Diet']
            edge_colors = [(1,0,0), (0,0,1)]  # 빨간색, 파란색

            for q_idx, (quality, quality_name, edge_color) in enumerate(zip(qualities, quality_names, edge_colors)):
                for i, (age_group, age_label) in enumerate(zip(age_groups, age_labels)):
                    network_key = f'{gender}_{age_group}'

                    graph = basic_networks[network_key]['cooccurrence'][quality]['graph']
                    centrality_data = centrality_results.get(network_key, {}).get('cooccurrence', {}).get(quality, {})

                    self.visualizer.plot_network(
                        graph, axes[q_idx, i], f'{quality_name} - {age_label}', centrality_data)

                axes[q_idx, 0].set_ylabel(f'{quality_name}', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(os.path.join(save_path, f'diet_age_progression_{gender}.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Created {gender} diet age progression plot")

    def create_health_diet_age_progression_plots(self, basic_networks, centrality_results, save_path='../result/'):
        age_groups = ['under40', '40-49', '50-64', '65plus']
        age_labels = ['<40', '40-49', '50-64', '65≤']
        
        network_types = ['diet_biomarker', 'diet_mets', 'diet_disease']
        network_names = ['Diet-Biomarker', 'Diet-MetS', 'Diet-Disease']
        
        for gender in ['Men', 'Women']:
            fig, axes = plt.subplots(3, 4, figsize=(26, 22))
            fig.suptitle(f'Health-Diet Networks (Age Progression): {gender}\n', fontsize=30, fontweight='bold')
            
            for i, (net_type, net_name) in enumerate(zip(network_types, network_names)):
                for j, (age_group, age_label) in enumerate(zip(age_groups, age_labels)):
                    network_key = f'{gender}_{age_group}'
                    density = 0
                    
                    centrality_data = None
                    if network_key in centrality_results:
                        health_data = centrality_results[network_key]['health'].get(net_type, {})
                        density = health_data.get('network_properties', {}).get('density', 0)
                        centrality_data = health_data
                    
                    health_graph = basic_networks[network_key]['health'][net_type]['graph']
                    title = f'{age_label}\nDensity: {density:.3f}'

                    self.visualizer.plot_network(health_graph, axes[i, j], title, centrality_results=centrality_data)
                    
                    if j == 0:
                        axes[i, j].set_ylabel(f'{net_name}', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(os.path.join(save_path, f'health_diet_age_progression_{gender}.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Created {gender} health-diet age progression plot")

    def create_gender_comparison_plots(self, basic_networks, centrality_results, diet_save_path, health_save_path):
        network_types = ['diet_disease', 'diet_mets', 'diet_biomarker']
        network_names = ['Diet-Disease', 'Diet-MetS', 'Diet-Biomarker']
        
        fig, axes = plt.subplots(2, 3, figsize=(24, 16))
        fig.suptitle('Diet-Health Networks: Gender Comparison\n', fontsize=30, fontweight='bold')
        
        for j, (net_type, net_name) in enumerate(zip(network_types, network_names)):
            men_graph = basic_networks['Men_All']['health'][net_type]['graph']
            men_density = centrality_results['Men_All']['health'][net_type]['network_properties'].get('density', 0)
            men_centrality = centrality_results['Men_All']['health'][net_type]
            
            women_graph = basic_networks['Women_All']['health'][net_type]['graph']
            women_density = centrality_results['Women_All']['health'][net_type]['network_properties'].get('density', 0)
            women_centrality = centrality_results['Women_All']['health'][net_type]
            
            self.visualizer.plot_network(
                men_graph, axes[0, j], f'Men: {net_name}\nDensity: {men_density:.3f}', men_centrality)

            self.visualizer.plot_network(
                women_graph, axes[1, j], f'Women: {net_name}\nDensity: {women_density:.3f}', women_centrality)
        
        plt.tight_layout()
        plt.savefig(os.path.join(health_save_path, 'gender_comparison_networks.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 새로 추가: 식습관 네트워크 성별 비교
        fig, axes = plt.subplots(1, 4, figsize=(32, 8))
        fig.suptitle('Diet Co-occurrence Networks: Gender Comparison\n', fontsize=30, fontweight='bold')

        qualities = ['poor', 'non_poor']
        quality_names = ['Poor Diet', 'Non-Poor Diet']

        for i, (quality, quality_name) in enumerate(zip(qualities, quality_names)):
            # 남성
            men_graph = basic_networks['Men_All']['cooccurrence'][quality]['graph']
            men_density = centrality_results['Men_All']['cooccurrence'][quality]['network_properties'].get('density', 0)
            men_centrality = centrality_results['Men_All']['cooccurrence'][quality]

            # 여성
            women_graph = basic_networks['Women_All']['cooccurrence'][quality]['graph']
            women_density = centrality_results['Women_All']['cooccurrence'][quality]['network_properties'].get('density', 0)
            women_centrality = centrality_results['Women_All']['cooccurrence'][quality]

            self.visualizer.plot_network(
                men_graph, axes[i*2], f'Men: {quality_name}\nDensity: {men_density:.3f}', men_centrality)

            self.visualizer.plot_network(
                women_graph, axes[i*2+1], f'Women: {quality_name}\nDensity: {women_density:.3f}', women_centrality)

        plt.tight_layout()
        plt.savefig(os.path.join(diet_save_path, 'diet_cooccurrence_gender_comparison.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def create_mets_comparison_plots(self, mets_networks, mets_centrality, save_path='../result/'):
        """MetS 유무에 따른 식습관 네트워크 비교 시각화"""
        import os

        # MetS 폴더 구조 생성
        mets_path = os.path.join(save_path, 'MetS')
        mets_total_path = os.path.join(mets_path, '전체')
        mets_gender_path = os.path.join(mets_path, '성별')

        for path in [mets_total_path, mets_gender_path]:
            os.makedirs(path, exist_ok=True)

        # Figure 1: Poor Diet Co-occurrence Networks (전체 대상자)
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        fig.suptitle('Figure 1. Poor Diet Co-occurrence Networks',
                     fontsize=26, fontweight='bold')

        pos_graph = mets_networks['MetS_Positive_Total']['cooccurrence']['poor']['graph']
        pos_centrality = mets_centrality['MetS_Positive_Total']['cooccurrence']['poor']
        pos_density = pos_centrality['network_properties'].get('density', 0)

        neg_graph = mets_networks['MetS_Negative_Total']['cooccurrence']['poor']['graph']
        neg_centrality = mets_centrality['MetS_Negative_Total']['cooccurrence']['poor']
        neg_density = neg_centrality['network_properties'].get('density', 0)

        self.visualizer.plot_network(
            pos_graph, axes[0], f'MetS(+)\nDensity: {pos_density:.3f}', pos_centrality)

        self.visualizer.plot_network(
            neg_graph, axes[1], f'MetS(-)\nDensity: {neg_density:.3f}', neg_centrality)

        plt.tight_layout()
        plt.savefig(os.path.join(mets_total_path, 'Figure1_Poor_Diet_Networks.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("Created Figure 1: Poor Diet Co-occurrence Networks")

        # Figure 2: Non-Poor Diet Co-occurrence Networks (전체 대상자)
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        fig.suptitle('Figure 2. Non-Poor Diet Co-occurrence Networks',
                     fontsize=26, fontweight='bold')

        pos_graph = mets_networks['MetS_Positive_Total']['cooccurrence']['non_poor']['graph']
        pos_centrality = mets_centrality['MetS_Positive_Total']['cooccurrence']['non_poor']
        pos_density = pos_centrality['network_properties'].get('density', 0)

        neg_graph = mets_networks['MetS_Negative_Total']['cooccurrence']['non_poor']['graph']
        neg_centrality = mets_centrality['MetS_Negative_Total']['cooccurrence']['non_poor']
        neg_density = neg_centrality['network_properties'].get('density', 0)

        self.visualizer.plot_network(
            pos_graph, axes[0], f'MetS(+)\nDensity: {pos_density:.3f}', pos_centrality)

        self.visualizer.plot_network(
            neg_graph, axes[1], f'MetS(-)\nDensity: {neg_density:.3f}', neg_centrality)

        plt.tight_layout()
        plt.savefig(os.path.join(mets_total_path, 'Figure2_Non_Poor_Diet_Networks.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("Created Figure 2: Non-Poor Diet Co-occurrence Networks")

        # Figure 3: 남성 식습관 네트워크 비교 (Poor/Non-Poor Diet)
        qualities = ['poor', 'non_poor']
        quality_names = ['Poor Diet', 'Non-Poor Diet']

        fig, axes = plt.subplots(2, 2, figsize=(20, 20))
        fig.suptitle('Figure 3. Men Diet Co-occurrence Networks',
                     fontsize=26, fontweight='bold')

        for i, (quality, quality_name) in enumerate(zip(qualities, quality_names)):
            men_pos_graph = mets_networks['MetS_Positive_Men']['cooccurrence'][quality]['graph']
            men_pos_centrality = mets_centrality['MetS_Positive_Men']['cooccurrence'][quality]
            men_pos_density = men_pos_centrality['network_properties'].get('density', 0)

            men_neg_graph = mets_networks['MetS_Negative_Men']['cooccurrence'][quality]['graph']
            men_neg_centrality = mets_centrality['MetS_Negative_Men']['cooccurrence'][quality]
            men_neg_density = men_neg_centrality['network_properties'].get('density', 0)

            self.visualizer.plot_network(
                men_pos_graph, axes[i, 0], f'MetS(+) {quality_name}\nDensity: {men_pos_density:.3f}',
                men_pos_centrality)

            self.visualizer.plot_network(
                men_neg_graph, axes[i, 1], f'MetS(-) {quality_name}\nDensity: {men_neg_density:.3f}',
                men_neg_centrality)

        plt.tight_layout()
        plt.savefig(os.path.join(mets_gender_path, 'Figure3_Men_Diet_Networks.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("Created Figure 3: Men Diet Networks")

        # Figure 4: 여성 식습관 네트워크 비교 (Poor/Non-Poor Diet)
        fig, axes = plt.subplots(2, 2, figsize=(20, 20))
        fig.suptitle('Figure 4. Women Diet Co-occurrence Networks',
                     fontsize=26, fontweight='bold')

        for i, (quality, quality_name) in enumerate(zip(qualities, quality_names)):
            women_pos_graph = mets_networks['MetS_Positive_Women']['cooccurrence'][quality]['graph']
            women_pos_centrality = mets_centrality['MetS_Positive_Women']['cooccurrence'][quality]
            women_pos_density = women_pos_centrality['network_properties'].get('density', 0)

            women_neg_graph = mets_networks['MetS_Negative_Women']['cooccurrence'][quality]['graph']
            women_neg_centrality = mets_centrality['MetS_Negative_Women']['cooccurrence'][quality]
            women_neg_density = women_neg_centrality['network_properties'].get('density', 0)

            self.visualizer.plot_network(
                women_pos_graph, axes[i, 0], f'MetS(+) {quality_name}\nDensity: {women_pos_density:.3f}',
                women_pos_centrality)

            self.visualizer.plot_network(
                women_neg_graph, axes[i, 1], f'MetS(-) {quality_name}\nDensity: {women_neg_density:.3f}',
                women_neg_centrality)

        plt.tight_layout()
        plt.savefig(os.path.join(mets_gender_path, 'Figure4_Women_Diet_Networks.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("Created Figure 4: Women Diet Networks")

        # 4. 성별+연령대별 MetS 비교 시각화 생성
        mets_age_path = os.path.join(mets_path, '성별+연령대')
        os.makedirs(mets_age_path, exist_ok=True)
        self.create_mets_age_comparison_plots(mets_networks, mets_centrality, mets_age_path)

    def create_mets_age_comparison_plots(self, mets_networks, mets_centrality, save_path):
        """성별+연령대별 MetS 비교 시각화 - Figure 5"""
        age_groups = ['under40', '40-49', '50-64', '65plus']
        age_labels = ['<40', '40-49', '50-64', '65≤']

        # Figure 5a: 남성 연령대별 Poor Diet 네트워크 (MetS+ vs MetS-)
        fig, axes = plt.subplots(2, 4, figsize=(32, 18))
        fig.suptitle('Figure 5a. Men Poor Diet Networks: Age Progression (MetS Comparison)\n' +
                    '(DM/AMI/Stroke/CKD excluded)',
                    fontsize=30, fontweight='bold')

        # MetS(+) 그룹: 첫 번째 행
        for i, (age_group, age_label) in enumerate(zip(age_groups, age_labels)):
            network_key = f'MetS_Positive_Men_{age_group}'

            if network_key in mets_networks:
                graph = mets_networks[network_key]['cooccurrence']['poor']['graph']
                centrality_data = mets_centrality[network_key]['cooccurrence']['poor']
                density = centrality_data['network_properties'].get('density', 0)

                self.visualizer.plot_network(
                    graph, axes[0, i], f'{age_label}\nDensity: {density:.3f}', centrality_data)
            else:
                axes[0, i].text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=20)
                axes[0, i].set_title(f'{age_label}', fontsize=23)

        # MetS(-) 그룹: 두 번째 행
        for i, (age_group, age_label) in enumerate(zip(age_groups, age_labels)):
            network_key = f'MetS_Negative_Men_{age_group}'

            if network_key in mets_networks:
                graph = mets_networks[network_key]['cooccurrence']['poor']['graph']
                centrality_data = mets_centrality[network_key]['cooccurrence']['poor']
                density = centrality_data['network_properties'].get('density', 0)

                self.visualizer.plot_network(
                    graph, axes[1, i], f'{age_label}\nDensity: {density:.3f}', centrality_data)
            else:
                axes[1, i].text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=20)
                axes[1, i].set_title(f'{age_label}', fontsize=23)

        axes[0, 0].set_ylabel('MetS(+)', fontsize=18, fontweight='bold')
        axes[1, 0].set_ylabel('MetS(-)', fontsize=18, fontweight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(save_path, 'Figure5a_Men_Age_Poor_Diet.png'),
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("Created Figure 5a: Men Age Progression (Poor Diet)")

        # Figure 5b: 여성 연령대별 Poor Diet 네트워크 (MetS+ vs MetS-)
        fig, axes = plt.subplots(2, 4, figsize=(32, 18))
        fig.suptitle('Figure 5b. Women Poor Diet Networks: Age Progression (MetS Comparison)\n' +
                    '(DM/AMI/Stroke/CKD excluded)',
                    fontsize=30, fontweight='bold')

        # MetS(+) 그룹: 첫 번째 행
        for i, (age_group, age_label) in enumerate(zip(age_groups, age_labels)):
            network_key = f'MetS_Positive_Women_{age_group}'

            if network_key in mets_networks:
                graph = mets_networks[network_key]['cooccurrence']['poor']['graph']
                centrality_data = mets_centrality[network_key]['cooccurrence']['poor']
                density = centrality_data['network_properties'].get('density', 0)

                self.visualizer.plot_network(
                    graph, axes[0, i], f'{age_label}\nDensity: {density:.3f}', centrality_data)
            else:
                axes[0, i].text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=20)
                axes[0, i].set_title(f'{age_label}', fontsize=23)

        # MetS(-) 그룹: 두 번째 행
        for i, (age_group, age_label) in enumerate(zip(age_groups, age_labels)):
            network_key = f'MetS_Negative_Women_{age_group}'

            if network_key in mets_networks:
                graph = mets_networks[network_key]['cooccurrence']['poor']['graph']
                centrality_data = mets_centrality[network_key]['cooccurrence']['poor']
                density = centrality_data['network_properties'].get('density', 0)

                self.visualizer.plot_network(
                    graph, axes[1, i], f'{age_label}\nDensity: {density:.3f}', centrality_data)
            else:
                axes[1, i].text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=20)
                axes[1, i].set_title(f'{age_label}', fontsize=23)

        axes[0, 0].set_ylabel('MetS(+)', fontsize=18, fontweight='bold')
        axes[1, 0].set_ylabel('MetS(-)', fontsize=18, fontweight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(save_path, 'Figure5b_Women_Age_Poor_Diet.png'),
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("Created Figure 5b: Women Age Progression (Poor Diet)")