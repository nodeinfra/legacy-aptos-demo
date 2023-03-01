import streamlit as st
import requests

api_address = "http://aptos-mainnet.nodeinfra.com:3123/"
nfts_endpoint = 'nfts'
example_address = "0x863e6d2f9aaa418b253d037a61027ecb9041f31d8d419f1819d83b26f43e16bb"
	# good examples
	# 0x863e6d2f9aaa418b253d037a61027ecb9041f31d8d419f1819d83b26f43e16bb
	# 0xa06235f755cb24eb896eb617d3fa7c8f372f04cc674d39c18da545b380b94277
	# 0x87c5241e5d6eb8ba7cd45684e978c8b61d78041662d1c209491104593a60455e
COLUMN_SIZE = 3
MAX_NFTS = 30

def main():
	print('------------new page-------------')
	token_id_list = list()
	st.set_page_config(
		page_title="NodeInfra",
		page_icon="./imgs/dd.png"
	)
	st.title("Aptos Market")

	input_address = st.text_input("Your address here", example_address)
	left, right = st.columns(2)
	button = left.button('Browse it!')
	slow_images = right.checkbox('Load slow images')

	num = 0
	if button:
		response = requests.get(api_address+nfts_endpoint, params={'owner_address':input_address})
		json_data = response.json()
		nfts = json_data["nfts"]

		
		for index, nft in enumerate(nfts):
			if index % COLUMN_SIZE == 0:
				col_list = st.columns(COLUMN_SIZE)
			metadata_uri = nft['metadata_uri']
			if slow_images and (metadata_uri.startswith('https://nftstorage') and not (metadata_uri.endswith('.jpeg') or metadata_uri.endswith('gif') or metadata_uri.endswith('jpg')))or (not metadata_uri.startswith('ipfs') and metadata_uri.endswith('json')):
				response = requests.get(nft['metadata_uri']).json()
				nft['metadata_uri'] = response['image']
			col_list[index%COLUMN_SIZE].text(nft['name'])
			col_list[index%COLUMN_SIZE].image(nft['metadata_uri'])
   
			if index == MAX_NFTS:
				
				break
	st.subheader('sample addresses')
	st.code("0xa06235f755cb24eb896eb617d3fa7c8f372f04cc674d39c18da545b380b94277")
	st.code("0x87c5241e5d6eb8ba7cd45684e978c8b61d78041662d1c209491104593a60455e")
if __name__ == "__main__":
	main()  