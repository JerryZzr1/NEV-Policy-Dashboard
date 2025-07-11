import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, date
import base64
from io import BytesIO
from PIL import Image
import uuid

# Page configuration
st.set_page_config(
    page_title="NEV Policy Research Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data storage file paths
DATA_FILE = "nev_research_data.json"
IMAGES_DIR = "uploaded_images"

# Create images directory if it doesn't exist
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Initialize session state
if 'reports' not in st.session_state:
    st.session_state.reports = {}
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# Data loading and saving functions
def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                st.session_state.reports = data
        except:
            st.session_state.reports = {}

def save_data():
    """Save data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.reports, f, ensure_ascii=False, indent=2)

def save_uploaded_image(uploaded_file):
    """Save uploaded image and return file path"""
    if uploaded_file is not None:
        # Generate unique filename
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(IMAGES_DIR, unique_filename)
        
        # Save image
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None

def convert_image_to_base64(image_path):
    """Convert image to base64 string for JSON storage"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return None

def display_image_from_base64(base64_string, caption="", width=None):
    """Display image from base64 string"""
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        st.image(image, caption=caption, width=width)
    except:
        st.error("Failed to display image")

# Default report template
def create_default_report():
    """Create default NEV research report template"""
    return {
        "title": "New Energy Vehicle Policy Research Report - Hong Kong",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "content": "This comprehensive study investigates the feasibility and implementation strategies for transitioning Hong Kong's transportation sector to New Energy Vehicles (NEVs), including electric vehicles (EVs) and hydrogen fuel cell vehicles (HFCVs). The research encompasses advantages and challenges of NEV adoption, AI-driven energy consumption analysis, infrastructure requirements, and policy recommendations to accelerate NEV adoption in Hong Kong.",
            "key_findings": [
                "EVs show 65% lower carbon emissions compared to ICE vehicles in Hong Kong's electricity grid mix",
                "HFCVs demonstrate superior performance for heavy-duty applications with 40% reduction in refueling time",
                "Infrastructure investment of HK$28.5 billion required for full NEV transition by 2035",
                "Policy incentives could accelerate NEV adoption rate from 12% to 45% by 2030"
            ]
        },
        "metrics": [
            {"label": "Current NEV Adoption Rate", "value": "12.3%", "trend": "+2.8%"},
            {"label": "CO2 Reduction Potential", "value": "58%", "trend": "+15%"},
            {"label": "Infrastructure Readiness", "value": "34%", "trend": "+8%"},
            {"label": "Policy Implementation Score", "value": "67/100", "trend": "+12"}
        ],
        "nev_comparison": [
            {"vehicle_type": "Small/Medium EVs", "energy_efficiency": 85, "carbon_reduction": 65, "cost_effectiveness": 78},
            {"vehicle_type": "Heavy-duty EVs", "energy_efficiency": 72, "carbon_reduction": 58, "cost_effectiveness": 65},
            {"vehicle_type": "Small/Medium HFCVs", "energy_efficiency": 68, "carbon_reduction": 72, "cost_effectiveness": 58},
            {"vehicle_type": "Heavy-duty HFCVs", "energy_efficiency": 75, "carbon_reduction": 68, "cost_effectiveness": 62},
            {"vehicle_type": "ICE Vehicles", "energy_efficiency": 35, "carbon_reduction": 0, "cost_effectiveness": 85}
        ],
        "infrastructure_data": [
            {"infrastructure_type": "EV Charging Stations", "current": 3200, "required": 28000, "investment_hkd": 8.5},
            {"infrastructure_type": "Fast Charging Hubs", "current": 180, "required": 2500, "investment_hkd": 12.2},
            {"infrastructure_type": "Hydrogen Stations", "current": 2, "required": 150, "investment_hkd": 5.8},
            {"infrastructure_type": "Grid Upgrades", "current": 25, "required": 100, "investment_hkd": 2.0}
        ],
        "energy_consumption": [
            {"month": "Jan", "ev_consumption": 42.5, "hfcv_consumption": 38.2, "ice_consumption": 85.6},
            {"month": "Feb", "ev_consumption": 41.8, "hfcv_consumption": 37.9, "ice_consumption": 84.2},
            {"month": "Mar", "ev_consumption": 43.2, "hfcv_consumption": 39.1, "ice_consumption": 86.1},
            {"month": "Apr", "ev_consumption": 44.1, "hfcv_consumption": 39.8, "ice_consumption": 87.3},
            {"month": "May", "ev_consumption": 45.3, "hfcv_consumption": 40.5, "ice_consumption": 88.9},
            {"month": "Jun", "ev_consumption": 46.8, "hfcv_consumption": 41.2, "ice_consumption": 90.1}
        ],
        "policy_recommendations": [
            {
                "title": "Accelerated EV Adoption Incentives",
                "description": "Implement comprehensive tax rebates up to HK$200,000 for EV purchases, coupled with reduced registration fees and priority parking privileges",
                "priority": "High",
                "timeline": "12 months",
                "budget": "HK$2.8 billion",
                "expected_impact": "Increase EV adoption by 25% within 2 years"
            },
            {
                "title": "Hydrogen Infrastructure Development",
                "description": "Establish 150 hydrogen refueling stations across Hong Kong with government-private partnerships, focusing on commercial vehicle routes",
                "priority": "High",
                "timeline": "36 months",
                "budget": "HK$5.8 billion",
                "expected_impact": "Enable 40% of heavy-duty vehicles to transition to hydrogen"
            },
            {
                "title": "Smart Grid Integration",
                "description": "Upgrade electricity grid to support bi-directional charging and renewable energy integration for NEV ecosystem",
                "priority": "Medium",
                "timeline": "48 months",
                "budget": "HK$2.0 billion",
                "expected_impact": "Reduce grid stress and enable V2G technology"
            }
        ],
        "implementation_status": [
            {
                "policy": "EV First Registration Tax Exemption",
                "status": "Active",
                "budget": "HK$1.2 billion",
                "impact": "High",
                "completion": 85,
                "target_date": "2024-12-31"
            },
            {
                "policy": "Public Charging Network Expansion",
                "status": "In Progress",
                "budget": "HK$800 million",
                "impact": "High",
                "completion": 45,
                "target_date": "2025-06-30"
            },
            {
                "policy": "Hydrogen Pilot Program",
                "status": "Planning",
                "budget": "HK$300 million",
                "impact": "Medium",
                "completion": 15,
                "target_date": "2025-12-31"
            }
        ],
        "images": []  # New field for storing images
    }

# Main interface function
def main():
    # Load data
    load_data()
    
    # Sidebar
    with st.sidebar:
        st.title("🚗 NEV Policy Research Dashboard")
        
        # Report management
        st.subheader("Research Reports")
        
        # Create new report
        if st.button("➕ Create New Report", use_container_width=True):
            report_id = f"report_{len(st.session_state.reports) + 1}"
            st.session_state.reports[report_id] = create_default_report()
            st.session_state.current_report = report_id
            save_data()
            st.rerun()
        
        # Select report
        if st.session_state.reports:
            report_options = {k: v["title"] for k, v in st.session_state.reports.items()}
            selected_report = st.selectbox(
                "Select Report",
                options=list(report_options.keys()),
                format_func=lambda x: report_options[x],
                index=list(report_options.keys()).index(st.session_state.current_report) 
                      if st.session_state.current_report in report_options else 0
            )
            st.session_state.current_report = selected_report
            
            # Delete report
            if st.button("🗑️ Delete Current Report", use_container_width=True):
                if len(st.session_state.reports) > 1:
                    del st.session_state.reports[st.session_state.current_report]
                    st.session_state.current_report = list(st.session_state.reports.keys())[0]
                    save_data()
                    st.rerun()
                else:
                    st.error("At least one report must be retained")
        
        # Export options
        st.subheader("Export Options")
        if st.button("📥 Export JSON Data", use_container_width=True):
            json_data = json.dumps(st.session_state.reports, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download JSON File",
                data=json_data,
                file_name=f"nev_research_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        # Image Management
        st.subheader("📸 Image Management")
        if st.session_state.current_report:
            current_report = st.session_state.reports[st.session_state.current_report]
            if 'images' not in current_report:
                current_report['images'] = []
            
            # Upload new image
            uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'gif', 'bmp'])
            if uploaded_file is not None:
                if st.button("💾 Save Image", use_container_width=True):
                    # Convert to base64 and save
                    image_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                    image_info = {
                        "id": str(uuid.uuid4()),
                        "filename": uploaded_file.name,
                        "data": image_data,
                        "caption": "",
                        "uploaded_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    current_report['images'].append(image_info)
                    save_data()
                    st.success("Image saved successfully!")
                    st.rerun()
            
            # Display uploaded images
            if current_report['images']:
                st.write(f"**Uploaded Images ({len(current_report['images'])})**")
                for i, img in enumerate(current_report['images']):
                    with st.expander(f"📷 {img['filename']}", expanded=False):
                        display_image_from_base64(img['data'], width=200)
                        st.caption(f"Uploaded: {img['uploaded_date']}")
                        if st.button(f"Delete", key=f"del_img_{img['id']}"):
                            current_report['images'].pop(i)
                            save_data()
                            st.rerun()

    # Main content area
    if not st.session_state.reports:
        st.title("🚗 NEV Policy Research Dashboard")
        st.info("Please create a report to begin")
        return
    
    current_report = st.session_state.reports[st.session_state.current_report]
    
    # Title and basic information editing
    st.title("🚗 New Energy Vehicle Policy Research Dashboard")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_title = st.text_input("Report Title", value=current_report["title"])
        if new_title != current_report["title"]:
            current_report["title"] = new_title
            current_report["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data()
    
    with col2:
        st.metric("Created Date", current_report["created_date"])
        st.caption(f"Last Modified: {current_report['last_modified']}")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Overview", "🔬 NEV Analysis", "🏗️ Infrastructure", "💡 Policy Recommendations", "🔄 Implementation", "📸 Images & Media"])
    
    # Overview tab
    with tab1:
        st.header("Executive Summary")
        
        # Summary editing
        new_summary = st.text_area("Research Summary", value=current_report["summary"]["content"], height=150)
        if new_summary != current_report["summary"]["content"]:
            current_report["summary"]["content"] = new_summary
            current_report["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data()
        
        # Key findings editing
        st.subheader("Key Research Findings")
        findings = current_report["summary"]["key_findings"]
        
        for i, finding in enumerate(findings):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_finding = st.text_input(f"Finding {i+1}", value=finding, key=f"finding_{i}")
                if new_finding != finding:
                    current_report["summary"]["key_findings"][i] = new_finding
                    save_data()
            with col2:
                if st.button("Delete", key=f"del_finding_{i}"):
                    current_report["summary"]["key_findings"].pop(i)
                    save_data()
                    st.rerun()
        
        if st.button("➕ Add Key Finding"):
            current_report["summary"]["key_findings"].append("New finding")
            save_data()
            st.rerun()
        
        # Key metrics
        st.subheader("Key Performance Indicators")
        metrics_cols = st.columns(4)
        
        for i, metric in enumerate(current_report["metrics"]):
            with metrics_cols[i % 4]:
                st.metric(
                    label=metric["label"],
                    value=metric["value"],
                    delta=metric["trend"]
                )
        
        # Metrics editing
        if st.checkbox("Edit Metrics"):
            for i, metric in enumerate(current_report["metrics"]):
                st.write(f"Metric {i+1}")
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    new_label = st.text_input("Label", value=metric["label"], key=f"metric_label_{i}")
                with col2:
                    new_value = st.text_input("Value", value=metric["value"], key=f"metric_value_{i}")
                with col3:
                    new_trend = st.text_input("Trend", value=metric["trend"], key=f"metric_trend_{i}")
                with col4:
                    if st.button("Delete", key=f"del_metric_{i}"):
                        current_report["metrics"].pop(i)
                        save_data()
                        st.rerun()
                
                if (new_label != metric["label"] or new_value != metric["value"] or new_trend != metric["trend"]):
                    current_report["metrics"][i] = {
                        "label": new_label,
                        "value": new_value,
                        "trend": new_trend
                    }
                    save_data()
            
            if st.button("➕ Add Metric"):
                current_report["metrics"].append({
                    "label": "New Metric",
                    "value": "0%",
                    "trend": "+0%"
                })
                save_data()
                st.rerun()
    
    # NEV Analysis tab
    with tab2:
        st.header("NEV Performance Analysis")
        
        # NEV comparison analysis
        st.subheader("Vehicle Type Comparison")
        
        # NEV data editing
        if st.checkbox("Edit NEV Comparison Data"):
            nev_df = pd.DataFrame(current_report["nev_comparison"])
            edited_nev = st.data_editor(nev_df, use_container_width=True)
            
            if not edited_nev.equals(nev_df):
                current_report["nev_comparison"] = edited_nev.to_dict('records')
                save_data()
        
        # NEV comparison radar chart
        nev_df = pd.DataFrame(current_report["nev_comparison"])
        
        fig_radar = go.Figure()
        
        categories = ['Energy Efficiency', 'Carbon Reduction', 'Cost Effectiveness']
        
        for _, row in nev_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row['energy_efficiency'], row['carbon_reduction'], row['cost_effectiveness']],
                theta=categories,
                fill='toself',
                name=row['vehicle_type']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="NEV Performance Comparison"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Energy consumption analysis
        st.subheader("AI-Driven Energy Consumption Analysis")
        
        # Energy consumption data editing
        if st.checkbox("Edit Energy Consumption Data"):
            energy_df = pd.DataFrame(current_report["energy_consumption"])
            edited_energy = st.data_editor(energy_df, use_container_width=True)
            
            if not edited_energy.equals(energy_df):
                current_report["energy_consumption"] = edited_energy.to_dict('records')
                save_data()
        
        # Energy consumption chart
        energy_df = pd.DataFrame(current_report["energy_consumption"])
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(x=energy_df['month'], y=energy_df['ev_consumption'], 
                                       mode='lines+markers', name='Electric Vehicles',
                                       line=dict(color='green', width=3)))
        fig_energy.add_trace(go.Scatter(x=energy_df['month'], y=energy_df['hfcv_consumption'], 
                                       mode='lines+markers', name='Hydrogen Fuel Cell Vehicles',
                                       line=dict(color='blue', width=3)))
        fig_energy.add_trace(go.Scatter(x=energy_df['month'], y=energy_df['ice_consumption'], 
                                       mode='lines+markers', name='ICE Vehicles',
                                       line=dict(color='red', width=3)))
        
        fig_energy.update_layout(
            title="Energy Consumption Comparison (kWh equivalent per 100km)",
            xaxis_title="Month",
            yaxis_title="Energy Consumption",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_energy, use_container_width=True)
    
    # Infrastructure tab
    with tab3:
        st.header("Infrastructure Requirements Analysis")
        
        # Infrastructure data editing
        if st.checkbox("Edit Infrastructure Data"):
            infra_df = pd.DataFrame(current_report["infrastructure_data"])
            edited_infra = st.data_editor(infra_df, use_container_width=True)
            
            if not edited_infra.equals(infra_df):
                current_report["infrastructure_data"] = edited_infra.to_dict('records')
                save_data()
        
        # Infrastructure gap analysis
        infra_df = pd.DataFrame(current_report["infrastructure_data"])
        
        fig_infra = go.Figure()
        fig_infra.add_trace(go.Bar(name='Current', x=infra_df['infrastructure_type'], 
                                  y=infra_df['current'], marker_color='lightblue'))
        fig_infra.add_trace(go.Bar(name='Required', x=infra_df['infrastructure_type'], 
                                  y=infra_df['required'], marker_color='darkblue'))
        
        fig_infra.update_layout(
            title="Infrastructure Gap Analysis",
            xaxis_title="Infrastructure Type",
            yaxis_title="Number of Units",
            barmode='group'
        )
        
        st.plotly_chart(fig_infra, use_container_width=True)
        
        # Investment requirements
        st.subheader("Investment Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_investment = sum(infra_df['investment_hkd'])
            st.metric("Total Investment Required", f"HK${total_investment:.1f} billion")
        
        with col2:
            # Investment breakdown pie chart
            fig_pie = px.pie(infra_df, values='investment_hkd', names='infrastructure_type',
                           title="Investment Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Policy Recommendations tab
    with tab4:
        st.header("Policy Recommendations")
        
        for i, rec in enumerate(current_report["policy_recommendations"]):
            with st.expander(f"Recommendation {i+1}: {rec['title']}", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    new_title = st.text_input("Title", value=rec["title"], key=f"rec_title_{i}")
                    new_desc = st.text_area("Description", value=rec["description"], key=f"rec_desc_{i}")
                    new_impact = st.text_input("Expected Impact", value=rec["expected_impact"], key=f"rec_impact_{i}")
                
                with col2:
                    new_priority = st.selectbox("Priority", ["High", "Medium", "Low"], 
                                              index=["High", "Medium", "Low"].index(rec["priority"]), 
                                              key=f"rec_priority_{i}")
                    new_timeline = st.text_input("Timeline", value=rec["timeline"], key=f"rec_timeline_{i}")
                    new_budget = st.text_input("Budget", value=rec["budget"], key=f"rec_budget_{i}")
                
                # Update data
                if (new_title != rec["title"] or new_desc != rec["description"] or 
                    new_priority != rec["priority"] or new_timeline != rec["timeline"] or 
                    new_budget != rec["budget"] or new_impact != rec["expected_impact"]):
                    current_report["policy_recommendations"][i] = {
                        "title": new_title,
                        "description": new_desc,
                        "priority": new_priority,
                        "timeline": new_timeline,
                        "budget": new_budget,
                        "expected_impact": new_impact
                    }
                    save_data()
                
                if st.button("Delete Recommendation", key=f"del_rec_{i}"):
                    current_report["policy_recommendations"].pop(i)
                    save_data()
                    st.rerun()
        
        if st.button("➕ Add New Recommendation"):
            current_report["policy_recommendations"].append({
                "title": "New Recommendation",
                "description": "Recommendation description",
                "priority": "Medium",
                "timeline": "6 months",
                "budget": "HK$100 million",
                "expected_impact": "Expected impact description"
            })
            save_data()
            st.rerun()
    
    # Implementation Status tab
    with tab5:
        st.header("Policy Implementation Status")
        
        # Implementation data editing
        impl_df = pd.DataFrame(current_report["implementation_status"])
        
        if st.checkbox("Edit Implementation Data"):
            edited_impl = st.data_editor(
                impl_df,
                use_container_width=True,
                column_config={
                    "completion": st.column_config.ProgressColumn(
                        "Completion %",
                        help="Completion percentage",
                        min_value=0,
                        max_value=100,
                    ),
                    "target_date": st.column_config.DateColumn(
                        "Target Date",
                        help="Expected completion date"
                    )
                }
            )
            
            if not edited_impl.equals(impl_df):
                current_report["implementation_status"] = edited_impl.to_dict('records')
                save_data()
        
        # Implementation status display
        st.dataframe(
            impl_df,
            use_container_width=True,
            column_config={
                "completion": st.column_config.ProgressColumn(
                    "Completion %",
                    help="Completion percentage",
                    min_value=0,
                    max_value=100,
                ),
                "target_date": st.column_config.DateColumn(
                    "Target Date",
                    help="Expected completion date"
                )
            }
        )
        
        # Implementation timeline chart
        st.subheader("Implementation Timeline")
        
        fig_timeline = px.bar(impl_df, x='policy', y='completion', 
                            color='impact', title="Policy Implementation Progress",
                            color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
        fig_timeline.update_layout(xaxis_title="Policy", yaxis_title="Completion %")
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Add new implementation item
        if st.button("➕ Add Implementation Item"):
            current_report["implementation_status"].append({
                "policy": "New Policy",
                "status": "Planning",
                "budget": "HK$100 million",
                "impact": "Medium",
                "completion": 0,
                "target_date": "2025-12-31"
            })
            save_data()
            st.rerun()
    
    # Images & Media tab
    with tab6:
        st.header("📸 Images & Media Gallery")
        
        # Initialize images list if not exists
        if 'images' not in current_report:
            current_report['images'] = []
        
        # Image upload section
        st.subheader("Upload New Images")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_files = st.file_uploader(
                "Choose images", 
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp'], 
                accept_multiple_files=True
            )
        
        with col2:
            if uploaded_files:
                if st.button("📤 Upload All Images", use_container_width=True):
                    for uploaded_file in uploaded_files:
                        image_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        image_info = {
                            "id": str(uuid.uuid4()),
                            "filename": uploaded_file.name,
                            "data": image_data,
                            "caption": f"Image: {uploaded_file.name}",
                            "uploaded_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "category": "General"
                        }
                        current_report['images'].append(image_info)
                    save_data()
                    st.success(f"Successfully uploaded {len(uploaded_files)} images!")
                    st.rerun()
        
        # Display and manage existing images
        if current_report['images']:
            st.subheader(f"Image Gallery ({len(current_report['images'])} images)")
            
            # Image grid display
            cols_per_row = 3
            for i in range(0, len(current_report['images']), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(current_report['images']):
                        img = current_report['images'][i + j]
                        with cols[j]:
                            # Display image
                            display_image_from_base64(img['data'], width=250)
                            
                            # Image details and editing
                            with st.expander(f"✏️ Edit {img['filename']}", expanded=False):
                                # Edit caption
                                new_caption = st.text_input(
                                    "Caption", 
                                    value=img['caption'], 
                                    key=f"caption_{img['id']}"
                                )
                                
                                # Edit category
                                categories = ["General", "Vehicle Images", "Infrastructure", "Charts & Graphs", "Research Data"]
                                current_category = img.get('category', 'General')
                                new_category = st.selectbox(
                                    "Category", 
                                    categories, 
                                    index=categories.index(current_category) if current_category in categories else 0,
                                    key=f"category_{img['id']}"
                                )
                                
                                # Update image info
                                if new_caption != img['caption'] or new_category != img.get('category', 'General'):
                                    img['caption'] = new_caption
                                    img['category'] = new_category
                                    current_report['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    save_data()
                                
                                # Image actions
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    # Download image
                                    image_data = base64.b64decode(img['data'])
                                    st.download_button(
                                        "💾 Download",
                                        data=image_data,
                                        file_name=img['filename'],
                                        mime="image/png",
                                        key=f"download_{img['id']}"
                                    )
                                
                                with col_b:
                                    # Delete image
                                    if st.button("🗑️ Delete", key=f"delete_{img['id']}"):
                                        current_report['images'] = [x for x in current_report['images'] if x['id'] != img['id']]
                                        save_data()
                                        st.rerun()
                                
                                # Show image metadata
                                st.caption(f"Uploaded: {img['uploaded_date']}")
                                st.caption(f"Category: {img.get('category', 'General')}")
            
            # Batch operations
            st.subheader("Batch Operations")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📁 Export All Images", use_container_width=True):
                    # Create a zip file with all images
                    import zipfile
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                        for img in current_report['images']:
                            image_data = base64.b64decode(img['data'])
                            zip_file.writestr(img['filename'], image_data)
                    
                    st.download_button(
                        label="Download Images ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"nev_images_{datetime.now().strftime('%Y%m%d')}.zip",
                        mime="application/zip"
                    )
            
            with col2:
                # Category filter
                all_categories = list(set([img.get('category', 'General') for img in current_report['images']]))
                selected_category = st.selectbox("Filter by Category", ["All"] + all_categories)
            
            with col3:
                if st.button("🗑️ Clear All Images", use_container_width=True):
                    if st.session_state.get('confirm_clear_images', False):
                        current_report['images'] = []
                        save_data()
                        st.success("All images cleared!")
                        st.session_state.confirm_clear_images = False
                        st.rerun()
                    else:
                        st.session_state.confirm_clear_images = True
                        st.warning("Click again to confirm deletion of all images")
        
        else:
            st.info("No images uploaded yet. Use the upload section above to add images to your report.")
            
            # Sample images suggestion
            st.subheader("💡 Suggested Image Categories")
            suggestions = [
                "🚗 Vehicle comparison photos",
                "🏗️ Infrastructure development images",
                "📊 Charts and data visualizations",
                "🔋 Battery and charging technology",
                "🛣️ Transportation network maps",
                "📈 Research methodology diagrams"
            ]
            
            for suggestion in suggestions:
                st.write(f"• {suggestion}")

if __name__ == "__main__":
    main()