import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import json
from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as file:
        return json.load(file)

# Rest of your Streamlit app code

st.set_page_config(page_title='Anomaly Dashboard', layout='wide')
# Custom CSS to inject
st.markdown("""
<style>
    html {
        font-size: 14px;
        font-family: 'Arial', sans-serif;;  # Replace with your desired font
    }
    h1 {
        font-size: 2.5em;  # Adjust title font size
    }
    body {
        color: #fff;  # Text color
        background-color: #00FF00;  # Replace with your desired background color
    }

    /* Add other custom styles if needed */
</style>
""", unsafe_allow_html=True)
#st.set_page_config(page_title='Anomaly Dashboard', layout='wide')
# First Lottie Animation
lottie_filepath = "Animation.json"  # Replace with your file path for the first animation
lottie_animation = load_lottiefile(lottie_filepath)

# Second Lottie Animation
another_lottie_filepath = "place2.json"  # Replace with your file path for the second animation
another_lottie_animation = load_lottiefile(another_lottie_filepath)
# 创建行来容纳文本和第二个动画
row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.columns((0.01, .8, 0.01, .2, 0.01))
row2_space1, row2_space2 = st.columns([.2, .8])  # 新增的列


# Displaying First Animation
with row1_1:
    #st.title('Welcome to Anomaly Dashboard!')
    st.write("<span style='font-size: 32px;'><strong>Welcome to Anomaly Dashboard!</span>", unsafe_allow_html=True)

    st.markdown("<div style='font-size: 22px;'>A new tool to help explain the found Anomalies across the Belgium National Railway.</div>", 
             unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)  # Add an underline
    st.markdown("<div style='font-size: 24px;'><strong>Use Cases:</strong></div>", 
             unsafe_allow_html=True)
    st.markdown(
                """
                - _Anomalies got you thinking about weather?_
                - _Looking for a new location of high anomalies?_
                - _Conducting detection methods for anomalies?_
                - _Just here to **have something fun**?_
                """
                )
   

    #st.write("This is the additional line of text.", key="additional_text", font_size=6)
    st.markdown("<hr/>", unsafe_allow_html=True)  # Add an underline
    # 在下划线下方添加视频控件
    st.markdown("<div style='font-size: 24px;'><strong>Tutorial Video:</strong></div>", 
             unsafe_allow_html=True)
    st.video("https://youtu.be/TVA_IU-_WKs")


with row1_2:
    st_lottie(lottie_animation, height=150, key="animation")

# Displaying Second Animation with Modified Layout and Size
with row1_2:  # 改变这里的行为
    # Add space column to separate the second animation from text
    

    # Place the second animation here
    st_lottie(another_lottie_animation, height=240, key="second_animation")  # Adjust height as needed
    st.write("")  # Empty space
# Rest of your Streamlit app code

# [Include the code for sidebar, data uploading, processing, and plotting as per your original app functionality]


# 加载动画文件
#lottie_filepath = "another_animation.json"  # 替换为您的动画文件路径
#lottie_animation = load_lottiefile(lottie_filepath)





# 侧边栏选项
st.sidebar.image('Animation1.gif',width=230)
st.sidebar.header('User Control Panel')
#st.sidebar.image('Animation1.gif')
# 使用文件上传功能选择数据源文件
uploaded_file = st.sidebar.file_uploader("Upload Data Source (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['minute'])
else:
    df = None

# 创建一个空容器用于后续页面显示
#page_container = st.empty()
if st.sidebar.button("Open Map DashBoard"):
    # 在此处设置打开另一个应用的逻辑
    # 可以使用st.experimental_set_query_params()等方法进行页面导航
    st.markdown(
                """
                [Please Open Map](https://map-dashboard-hwraomedhs4qhszvxtcjzt.streamlit.app/)

                """
                )
# 添加"detection method"下拉框
detection_method = st.sidebar.selectbox('Detection Method', ['isolation_forest_anamoly', 'lof_anamoly', 'svm_anamoly', 'knn_anamoly','final_anomaly_flag'])
# 在左侧控件栏中添加一个按钮



# 主页面
#st.title('Interactive Dashboard with Anomaly Highlighting')

# 确保数据已加载
if df is not None:
    # 更新选择车辆 ID 的选项
    selected_id = st.sidebar.selectbox('Vehicle ID', df['mapped_veh_id'].unique())

    # 定义允许选择的列名
    allowed_columns = ['RS_E_InAirTemp_PC1', 'RS_E_InAirTemp_PC2', 'RS_E_OilPress_PC1', 'RS_E_OilPress_PC2', 'RS_E_RPM_PC1', 'RS_E_RPM_PC2', 'RS_E_WatTemp_PC1', 'RS_E_WatTemp_PC2', 'RS_T_OilTemp_PC1', 'RS_T_OilTemp_PC2', 'Temperature', 'RelativeHumidity', 'DewPoint', 'Precipitation', 'Snowfall', 'Rain', 'lat', 'lon', 'Elevation']
    # 筛选出允许的列名
    available_columns = [col for col in allowed_columns if col in df.columns]
    column_name = st.sidebar.selectbox('dimensions', available_columns)

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
    # 在侧边栏中添加复选框
    show_details = st.sidebar.checkbox('Show Details of Anomalies')

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
                  for val, temp, rh, dp, precip, snowfall, rain in zip(filtered_df[column_name], filtered_df['Temperature'], filtered_df['RelativeHumidity'], filtered_df['DewPoint'], filtered_df['Precipitation'], filtered_df['Snowfall'], filtered_df['Rain'])],  # 设置悬停文本内容
            line=dict(color='black',width=0.7)  # 设置线条颜色为黑色
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

    
    st.write("<span style='font-size: 18px;'><strong>Specific Scenario:</span>", unsafe_allow_html=True)
    #st.markdown(f"<strong>specific scenario ID:</strong> , unsafe_allow_html=True)
    st.markdown(f"<strong>Selected Vehicle ID:</strong> {selected_id}", unsafe_allow_html=True)
    st.markdown(f"<strong>Detection Method:</strong> {detection_method}", unsafe_allow_html=True)
    st.markdown(f"<strong>Selected Dimension:</strong> {column_name}", unsafe_allow_html=True)
    st.markdown(f"<strong>Selected Time Range:</strong> {start_date.strftime('%m/%d/%Y %I:%M %p')} to {end_date.strftime('%m/%d/%Y %I:%M %p')}", unsafe_allow_html=True)


    # 在 Streamlit 上显示图表
    st.plotly_chart(fig)

    # 计算当前时间范围内的异常值数量（仅在选择显示异常值时计算）
    

    # 计算当前时间范围内的正常值和异常值数量
    if df is not None:
        if show_anomalies_only:
            anomaly_df = filtered_df[filtered_df[detection_method] == -1]
            normal_df = filtered_df[filtered_df[detection_method] != -1]
        else:
            anomaly_df = filtered_df[filtered_df[detection_method] == -1]
            normal_df = filtered_df[filtered_df[detection_method] != -1]

        total_anomalies = len(anomaly_df)
        total_normals = len(normal_df)
        total_records = len(filtered_df)

        st.write("<span style='font-size: 18px;'><strong>In this scenario:</span>", unsafe_allow_html=True)
        st.write(f"Number of anomalies: {total_anomalies}")
        st.write(f"Number of normals: {total_normals}")
        st.write(f"Proportion of anomalies: {total_anomalies / total_records:.2%}")


        # 在主页面中显示异常值详细信息表格
        if show_details and df is not None:
            if show_anomalies_only:
                anomaly_df = filtered_df[filtered_df[detection_method] == -1]
            else:
                anomaly_df = filtered_df[filtered_df[detection_method] == -1]

            if not anomaly_df.empty:
                st.write("<span style='font-size: 16px;'><strong>Details of Anomalies:</span>", unsafe_allow_html=True)
                st.dataframe(anomaly_df[['mapped_veh_id','minute','lat', 'lon','RS_E_InAirTemp_PC1', 'RS_E_InAirTemp_PC2', 'RS_E_OilPress_PC1', 'RS_E_OilPress_PC2', 'RS_E_RPM_PC1', 'RS_E_RPM_PC2', 'RS_E_WatTemp_PC1', 'RS_E_WatTemp_PC2', 'RS_T_OilTemp_PC1', 'RS_T_OilTemp_PC2', 'Temperature', 'RelativeHumidity', 'DewPoint', 'Precipitation', 'Snowfall', 'Rain']])
