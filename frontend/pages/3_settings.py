import streamlit as st 
from main import agenda_box
from pathlib import Path
import time,json,pytz
from dbModes.sModes import sModes

def main() -> None:
        
    st.header('Settings ⚙',divider='red',anchor=False)
    
    with st.expander('Type of storage 💾',expanded=False):
        
        storage_modes : list[str] = [
            'Database',
            'Local',
        ]
        
        slctd_optn = st.radio(f"Selected mode of storage : :green[{storage_modes[st.session_state.mode_of_storage]}]",
                 storage_modes,
                 index=st.session_state.mode_of_storage,
                 horizontal=True)
        
        if slctd_optn == 'Database':
            ...
                    
        if slctd_optn == 'Local':
            path : str = st.text_input('Paste file path here',
                                       placeholder='Example path : C:\home\lasu\journal')
            
            
                
        if st.button(f'Set **{slctd_optn}** as storage mode',
                     type='primary',
                             use_container_width=True):
            if slctd_optn == 'Database':
                st.session_state.mode_of_storage = storage_modes.index(slctd_optn)
                st.rerun()
            
            if slctd_optn == 'Local':
                st.session_state.mode_of_storage = storage_modes.index(slctd_optn)
                try:
                    if path:
                        p = Path(path)
                        with st.spinner('loading.....'):
                            time.sleep(1)
                            
                            if p.is_dir():
                                test : list[dict] = [st.session_state.journal]
                                st.session_state.journal_path = path + '\journal.json'
                                with open(st.session_state.journal_path, 'w') as fp:
                                    json.dump(test, fp)
                            else:
                                st.warning('Path not found')
                        
                except Exception as e:
                    print(f'\nError: {e}')
                
        
    with st.expander('Set per-agendas 📝',expanded=True):
        agenda_box('Set agenda')
    
    with st.expander('Import 📥'):
        st.file_uploader('upload your Back-up Journal file here:',
                         type=['csv','json'])
        if st.button('Start importing',
                     type='primary'):
            ...

    with st.expander('Export 📤'):
        ...
    
    
if __name__ == '__main__':
    main()