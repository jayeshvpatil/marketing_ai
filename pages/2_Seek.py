from utils import llm_gcp_q_a_chat, data_loader

# moved chat in a seperate app because streamlit doesn't allow chat inside tabs or expanders
def  main():
    data = data_loader.load()
    llm_gcp_q_a_chat.start_chat(data)
        
if __name__ == '__main__':
    main()
