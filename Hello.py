# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import streamlit as st
import openai
import os
import streamlit as st

# Configure Streamlit settings to hide the "Manage app" UI elements
st.set_option('server.showManageApp', False)

# Your Streamlit app code here...

# Set OpenAI API key using the SDK's dedicated method
# Retrieve the API key from the environment variable
api_key = st.secrets["OPENAI_API_KEY"]

# Use the API key with OpenAI
openai.api_key = api_key

# Query Suggestions
query_suggestions = [
    "Tell me about African immigration history in the US",
    "What are the current immigration policies for African immigrants?",
    "Statistics on African immigrants in the US",
    "Challenges faced by African immigrants in the United States",
    "How can I support African immigrant communities"
]

# Set up the Streamlit app
def main():
    st.title('African Collaborative Network (ACN)')
    st.sidebar.image("ACN_LOGO.webp", caption='ACN', use_column_width=True)

    # Initialize 'typed_query_history' session state if not present
    if 'typed_query_history' not in st.session_state:
        st.session_state.typed_query_history = []

    # Display query suggestions
    for i, suggestion in enumerate(query_suggestions):
        if st.button(suggestion, key=f"suggestion_button_{i}"):
            # If a suggestion is clicked, populate the user query with the selected suggestion
            user_query = suggestion
            # Proceed to get the response for the selected suggestion
            response_obj = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_query}
                ]
            )
            response = response_obj['choices'][0]['message']['content']

            # Apply green color to the response text
            st.write(f'<span style="color: green;">Response for \'{user_query}\':</span>', unsafe_allow_html=True)
            st.write(response)

    # Handle user queries
    user_query = st.text_input('Ask anything about African Immigrants in the US:', '')

    if user_query:
        response_obj = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )
        response = response_obj['choices'][0]['message']['content']

        # Apply green color to the response text
        st.write(f'<span style="color: green;">Response for \'{user_query}\':</span>', unsafe_allow_html=True)
        st.write(response)

        # Append the query and response to the query history
        st.session_state.typed_query_history.append({"query": user_query, "response": response})

    # Display query history in the sidebar
    st.sidebar.title('Query History')
    clear_typed_query_history = st.sidebar.button("Clear Query History")

    if clear_typed_query_history:
        st.session_state.typed_query_history = []  # Clear the query history

    for i, entry in enumerate(st.session_state.typed_query_history):
        query = entry["query"]
        response = entry["response"]
        if st.sidebar.button(f"{i + 1}. {query}", key=f"typed_query_history_button_{i}"):
            st.write(f'<span style="color: green;">Response for \'{query}\':</span>', unsafe_allow_html=True)
            st.write(response)

if __name__ == "__main__":
    main()



