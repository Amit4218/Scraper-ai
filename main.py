import streamlit as st
from scrape import website, parse_content, clean_content, split_content
from ai import parse_with_openai

st.title("Scraper")
url = st.text_input('Enter your URL')

if st.button('Scrape'):
    if url:
        st.write("Scraping website...")

        website_content = website(url)
        body_content = parse_content(website_content)
        cleaned_content = clean_content(body_content)

        st.session_state.website_content = cleaned_content

        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

if "website_content" in st.session_state:
    parse_description = st.text_area("Describe things to scrape")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing document...")

            dom_chunks = split_content(st.session_state.website_content)
            parsed_result = parse_with_openai(dom_chunks, parse_description)
            st.write(parsed_result)