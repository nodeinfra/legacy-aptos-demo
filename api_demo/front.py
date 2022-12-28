import streamlit as st
import requests

api_address = "http://223.130.135.191:3000/rpc/"
get_nft_balances = 'get_nft_balances'
get_nft_metadata = 'get_nft_metadata'
example_address = "0xa06235f755cb24eb896eb617d3fa7c8f372f04cc674d39c18da545b380b94277"
	# good examples
	# 0x863e6d2f9aaa418b253d037a61027ecb9041f31d8d419f1819d83b26f43e16bb
	# 0xa06235f755cb24eb896eb617d3fa7c8f372f04cc674d39c18da545b380b94277
	# 0x87c5241e5d6eb8ba7cd45684e978c8b61d78041662d1c209491104593a60455e
COLUMN_SIZE = 3

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
		response = requests.get(api_address+get_nft_balances, params={'owner_hash':input_address})
		json_data = response.json()
		for token in json_data:
			num +=1
			token_id_list.append(token['token_data_id_hash'])
			if num > 20:
				break
		for i, token_id in enumerate(token_id_list):
			response = requests.get(api_address+get_nft_metadata, params={'nft_hash':token_id})
			json_data = response.json()[0]
			print(json_data)
			if slow_images:
				metadata_uri = json_data['metadata_uri']
				if (metadata_uri.startswith('https://nftstorage') and not (metadata_uri.endswith('.jpeg') or metadata_uri.endswith('gif') or metadata_uri.endswith('jpg')))or (not metadata_uri.startswith('ipfs') and metadata_uri.endswith('json')):
					response = requests.get(json_data['metadata_uri']).json()
					print(response)
					json_data['metadata_uri'] = response['image']
			if i % COLUMN_SIZE == 0:
				col_list = st.columns(COLUMN_SIZE)
			col_list[i%COLUMN_SIZE].text(json_data['name'])
			col_list[i%COLUMN_SIZE].image(json_data['metadata_uri'])

	st.subheader('sample addresses')
	st.code('0x863e6d2f9aaa418b253d037a61027ecb9041f31d8d419f1819d83b26f43e16bb')
	st.code('0x87c5241e5d6eb8ba7cd45684e978c8b61d78041662d1c209491104593a60455e')
if __name__ == "__main__":
	main()  