import streamlit as st
import requests
import logging as log

st.title('Search Documents')
search_query = st.text_input('Enter search:')
print(search_query)
if search_query is not None and search_query != '':
    input_data = {"search": search_query }
    headers = {"Content-Type": "application/json"}
    log.info(f'Seach query: {input_data}')
    response = requests.post('http://backend:8000/search/', json=input_data, headers=headers)
    search_results = response.json()
    N_cards_per_row = 3
    results = search_results["results"]
    st.caption(f"Showing {len(results)} results:")
    for n_row, row in enumerate(results):
        i = n_row%N_cards_per_row
        search_index = n_row + 1
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"Result #{search_index}")
            st.caption(f"{row.strip()}")
            st.markdown(f"**{row.strip()}**")
    st.write(f"Search Results: {search_results}")