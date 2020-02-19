import { HEADER_ACTION_SET, HEADER_ACTION_SET_SEARCH_VALUE } from './consts';

const searchDefault = {
  placeholder: 'Поиск...',
  onSearch: null,
  value: '',
};
const addBtnDefault = {
  text: 'Добавить',
  onClick: null,
};
const header = (state = {
  addBtn: addBtnDefault,
  search: searchDefault,
  title: null,
}, action) => {
  switch (action.type) {
    case HEADER_ACTION_SET:
      const { search, title, addBtn } = action.payload;
      return {
        ...state,
        search: { ...searchDefault, ...(search || {}) },
        addBtn: { ...addBtnDefault, ...(addBtn || {}) },
        title: title || null,
      };
    case HEADER_ACTION_SET_SEARCH_VALUE:
      return {
        ...state,
        search: {
          ...state.search,
          value: action.payload,
        },
      };
    default:
      return state;
  }
};

export default header;
