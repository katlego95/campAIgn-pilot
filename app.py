import streamlit as st
from utils.file_utils import read_csv
from prompts.prompts import get_underperforming_products_prompt, get_campaign_planning_prompt
from llm.gemini import generate_text
from fallback.simulation import run_facebook_ad_campaign, run_email_marketing_campaign

def main():
    st.title("campAIgn pilot")

    # 1. Product Upload
    st.header("1. Upload Product Data")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        df = read_csv(uploaded_file)

        if df is not None:
            # 2. Display Data
            st.header("2. Product Data")
            st.write(df)

            # 3. Underperformance Detection
            st.header("3. Underperformance Detection")
            
            # Simple logic for now: products with high hits but low sales
            underperforming_df = df[(df['hits'] > df['hits'].mean()) & (df['sales'] < df['sales'].mean())]
            
            st.write("Underperforming Products:")
            st.write(underperforming_df)

            if not underperforming_df.empty:
                # Use Gemini to explain the selection
                with st.spinner("Analyzing underperforming products..."):
                    prompt = get_underperforming_products_prompt(underperforming_df)
                    explanation = generate_text(prompt)
                    st.info(explanation)

                # 4. Campaign Planning
                st.header("4. Campaign Planning")
                
                # Let Gemini decide on a campaign
                with st.spinner("Planning campaigns..."):
                    prompt = get_campaign_planning_prompt(underperforming_df)
                    campaign_plan = generate_text(prompt)
                    st.info(campaign_plan)

                # 5. API Calls for Execution
                st.header("5. Campaign Execution")
                campaign_type = st.selectbox("Select a campaign to run:", ["Facebook Ad", "Email Marketing"])
                product_to_promote = st.selectbox("Select a product to promote:", underperforming_df['name'].tolist())

                if st.button("Run Campaign"):
                    if campaign_type == "Facebook Ad":
                        # Placeholder for real API call
                        # result = real_api.run_facebook_ad(product_to_promote)
                        result = run_facebook_ad_campaign(product_to_promote)
                    elif campaign_type == "Email Marketing":
                        # Placeholder for real API call
                        # result = real_api.run_email_campaign(product_to_promote)
                        result = run_email_marketing_campaign(product_to_promote)
                    
                    st.write("Campaign Result:")
                    st.write(result)

                    # 6. Campaign Impact
                    st.header("6. Campaign Impact")
                    st.write("Analyzing campaign impact...")
                    # In a real app, you would measure the impact based on API results
                    # For now, we'll just display the simulated results
                    if result['status'] == 'success':
                        st.success(result['message'])
                        if "ad_spend" in result:
                            st.write(f"Ad Spend: ${result['ad_spend']}")
                            st.write(f"Clicks: {result['clicks']}")
                        if "emails_sent" in result:
                            st.write(f"Emails Sent: {result['emails_sent']}")
                            st.write(f"Opens: {result['opens']}")
                    else:
                        st.error("Campaign failed.")

                    # 7. Decision Logic
                    st.header("7. Decision Logic")
                    with st.spinner("Deciding next steps..."):
                        prompt = f"The {campaign_type} campaign for {product_to_promote} has finished. The result is: {result}. Should we continue, adapt, or stop the campaign? Explain your reasoning."
                        decision = generate_text(prompt)
                        st.info(decision)

if __name__ == "__main__":
    main()
