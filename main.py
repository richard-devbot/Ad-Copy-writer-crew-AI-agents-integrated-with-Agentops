from agents import MarketingAnalysisAgents
from tasks import MarketingAnalysisTasks
from crewai import Crew
import streamlit as st
import agentops
from dotenv import load_dotenv
load_dotenv()
import os

agentops.init()
# agentops.init(os.environ.get("AGENTOPS_API_KEY"))
# agentops.init(api_key='40815592-7122-43ed-88ca-69480fddbe37', tags=['prompt generator'])


tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()


# Create a Streamlit UI
def main():
    st.title("Marketing Analysis and Campaign Development")
    st.sidebar.title("Agents")
    st.sidebar.write("The following agents are working together to develop a marketing campaign:")

    st.sidebar.write("### Lead Market Analyst")
    st.sidebar.write("Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.")
    st.sidebar.write("### Chief Marketing Strategist")
    st.sidebar.write("Synthesize amazing insights from product analysis to formulate incredible marketing strategies.")
    st.sidebar.write("### Creative Content Creator")
    st.sidebar.write("Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact Instagram ad copies.")
    st.sidebar.write("### Senior Photographer")
    st.sidebar.write("Take the most amazing photographs for instagram ads that capture emotions and convey a compelling message.")
    st.sidebar.write("### Chief Creative Director")
    st.sidebar.write("Oversee the work done by your team to make sure it's the best possible and aligned with the product's goals, review, approve, ask clarifying question or delegate follow up work if necessary to make decisions")

    product_website = st.text_input("Enter the product website:")
    product_details = st.text_area("Enter the product details:")

    if st.button("Submit"):
        if product_website and product_details:
            # Create Agents
            product_competitor_agent = agents.product_competitor_agent()
            strategy_planner_agent = agents.strategy_planner_agent()
            creative_agent = agents.creative_content_creator_agent()

            # Create Tasks
            website_analysis = tasks.product_analysis(
                product_competitor_agent, product_website, product_details)
            market_analysis = tasks.competitor_analysis(
                product_competitor_agent, product_website, product_details)
            campaign_development = tasks.campaign_development(
                strategy_planner_agent, product_website, product_details)
            write_copy = tasks.instagram_ad_copy(creative_agent)

            # Create Crew responsible for Copy
            copy_crew = Crew(
                agents=[
                    product_competitor_agent,
                    strategy_planner_agent,
                    creative_agent
                ],
                tasks=[
                    website_analysis,
                    market_analysis,
                    campaign_development,
                    write_copy
                ],
                verbose=True,
                # Remove this when running locally. This helps prevent rate limiting with groq.
                max_rpm=1
            )

            ad_copy = copy_crew.kickoff()

            # Create Crew responsible for Image
            senior_photographer = agents.senior_photographer_agent()
            chief_creative_diretor = agents.chief_creative_diretor_agent()

            # Create Tasks for Image
            take_photo = tasks.take_photograph_task(
                senior_photographer, ad_copy, product_website, product_details)
            approve_photo = tasks.review_photo(
                chief_creative_diretor, product_website, product_details)

            image_crew = Crew(
                agents=[
                    senior_photographer,
                    chief_creative_diretor
                ],
                tasks=[
                    take_photo,
                    approve_photo
                ],
                verbose=True,
                # Remove this when running locally. This helps prevent rate limiting with groq.
                max_rpm=1
            )

            image = image_crew.kickoff()

            # Print results
            st.write("\n\n########################")
            st.write("## Here is the result")
            st.write("########################\n")
            st.write("Your post copy:")
            st.write(ad_copy)
            st.write("'\n\nYour midjourney description:")
            st.write(image)

if __name__ == "__main__":
    main()