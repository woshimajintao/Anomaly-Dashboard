import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Streamlit 页面配置
st.set_page_config(page_title='Interactive Dashboard with Anomaly Highlighting', layout='wide')

# 侧边栏选项
st.sidebar.header('User Control Panel')

# 使用文件上传功能选择数据源文件
uploaded_file = st.sidebar.file_uploader("Upload Data Source (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['minute'])
else:
    df = None

# 添加"detection method"下拉框
detection_method = st.sidebar.selectbox('Detection Method', ['isolation_forest_anamoly', 'lof_anamoly', 'svm_anamoly', 'knn_anamoly','final_anomaly_flag'])

# 主页面
st.title('Interactive Dashboard with Anomaly Highlighting')

# 确保数据已加载
if df is not None:
    # 更新选择车辆 ID 的选项
    selected_id = st.sidebar.selectbox('Vehicle ID', df['mapped_veh_id'].unique())

    # 定义允许选择的列名
    allowed_columns = ['RS_E_InAirTemp_PC1', 'RS_E_InAirTemp_PC2', 'RS_E_OilPress_PC1', 'RS_E_OilPress_PC2', 'RS_E_RPM_PC1', 'RS_E_RPM_PC2', 'RS_E_WatTemp_PC1', 'RS_E_WatTemp_PC2', 'RS_T_OilTemp_PC1', 'RS_T_OilTemp_PC2', 'Temperature', 'RelativeHumidity', 'DewPoint', 'Precipitation', 'Snowfall', 'Rain', 'lat', 'lon', 'Elevation']
    # 筛选出允许的列名
    available_columns = [col for col in allowed_columns if col in df.columns]
    column_name = st.sidebar.selectbox('Features', available_columns)

    # 根据用户选择的 ID 过滤 DataFrame
    filtered_df = df[df['mapped_veh_id'] == selected_id]

    # 设置时间范围选择器
    min_date = filtered_df['minute'].min().to_pydatetime()
    max_date = filtered_df['minute'].max().to_pydatetime()
    start_date, end_date = st.sidebar.slider(
        "Range of Time", 
        min_value=min_date, 
        max_value=max_date, 
        value=(min_date, max_date),
        format="MM/DD/YY HH:mm"
    )
    # 根据选择的时间范围过滤数据
    filtered_df = filtered_df[(filtered_df['minute'] >= start_date) & (filtered_df['minute'] <= end_date)]
    show_anomalies_only = st.sidebar.checkbox('Show Anomalies Only (Red)')
    # 按时间排序
    filtered_df = filtered_df.sort_values('minute')

    # 创建图表
    fig = go.Figure()

    if show_anomalies_only:
        # 如果用户选择只显示异常值
        anomaly_df = filtered_df[filtered_df[detection_method] == -1]
        fig.add_trace(go.Scatter(
            x=anomaly_df['minute'], 
            y=anomaly_df[column_name],
            mode='markers', 
            name='Anomaly',
            marker=dict(color='red', size=10),
            showlegend=True,
            hovertemplate='Time: %{x}<br>%{text}',  # 修改悬停文本格式
            text=[f'{column_name}: {val}<br>Temperature: {temp}<br>RelativeHumidity: {rh}<br>DewPoint: {dp}<br>Precipitation: {precip}<br>Snowfall: {snowfall}<br>Rain: {rain}' 
                  for val, temp, rh, dp, precip, snowfall, rain in zip(anomaly_df[column_name], anomaly_df['Temperature'], anomaly_df['RelativeHumidity'], anomaly_df['DewPoint'], anomaly_df['Precipitation'], anomaly_df['Snowfall'], anomaly_df['Rain'])]  # 设置悬停文本内容
        ))
    else:
        # 否则，显示所有值，并用颜色标记异常值
        colors = ['red' if anomaly == -1 else 'blue' for anomaly in filtered_df[detection_method]]
        fig.add_trace(go.Scatter(
            x=filtered_df['minute'], 
            y=filtered_df[column_name],
            mode='lines+markers',
            name='Data',
            marker_color=colors,
            hovertemplate='Time: %{x}<br>%{text}',  # 修改悬停文本格式
            text=[f'{column_name}: {val}<br>Temperature: {temp}<br>RelativeHumidity: {rh}<br>DewPoint: {dp}<br>Precipitation: {precip}<br>Snowfall: {snowfall}<br>Rain: {rain}<br>' 
                  for val, temp, rh, dp, precip, snowfall, rain in zip(filtered_df[column_name], filtered_df['Temperature'], filtered_df['RelativeHumidity'], filtered_df['DewPoint'], filtered_df['Precipitation'], filtered_df['Snowfall'], filtered_df['Rain'])]  # 设置悬停文本内容
        ))

    # 设置图表布局
    fig.update_layout(
        title=f'{column_name} Variation Curve and Anomalies',
        autosize=False,
        width=900,
        height=550,
        xaxis_title='Time',
        yaxis_title=f'{column_name}',
        xaxis=dict(
            type='date',
            tickformat='%m/%d/%Y %H:%M'
        )
    )

    # 在 Streamlit 上显示图表
    st.plotly_chart(fig)
