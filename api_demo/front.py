import streamlit as st
import requests
import json

def main():
	st.title("Aptos Market")
	token_id_list = list()
	
	
	
	input_address = st.text_input("Your address here", "0x863e6d2f9aaa418b253d037a61027ecb9041f31d8d419f1819d83b26f43e16bb")
	# good examples
	# 0x863e6d2f9aaa418b253d037a61027ecb9041f31d8d419f1819d83b26f43e16bb
	# 0xa06235f755cb24eb896eb617d3fa7c8f372f04cc674d39c18da545b380b94277
 
	button = st.button('Brows it!')
	URL = 'http://223.130.135.191:3000/rpc/get_token_balances?target_address='
	get_token_metadata_URL = 'http://223.130.135.191:3000/rpc/get_token_metadata?token_contract='
	URL = URL + input_address
	num = 0
	if button:
		response = requests.get(URL)
		json_data = response.json()
		for token in json_data:
			num +=1
			print(token)
			token_id_list.append(token['token_data_id_hash'])
			if num > 50:
				break
		for token_id in token_id_list:
			
			get_token_metadata_URL = 'http://223.130.135.191:3000/rpc/get_token_metadata?token_contract='
			get_token_metadata_URL += token_id

   
			response = requests.get(get_token_metadata_URL)
			json_data = response.json()
			print(json_data)

			st.text(json_data[0]['collection_name'])
			st.text(json_data[0]['name'])
			
			st.image(json_data[0]['metadata_uri'])
			# st.image('https://cloudflare-ipfs.com/ipfs/QmQ7m9tAFapj13h55u9iRQ4FtaiTAKtSFSgY3As47DMvfu\n')
			print(json_data[0]['metadata_uri'])



	
	





if __name__ == "__main__":
	main()  