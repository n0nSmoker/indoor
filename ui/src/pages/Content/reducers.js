import {
  CONTENT_ACTION_SET_FILTERS,
  CONTENT_ACTION_RECEIVE_CONTENT,
} from './consts.js'


const content = (state = {
  content: [],
  total: 0,
  isLoading: false,
  filters: {
    limit: 10,
    page: 1,
  },
}, action) => {
  switch (action.type) {
    case CONTENT_ACTION_SET_FILTERS:
      return {
        ...state,
        filters: action.filters,
      };
    case CONTENT_ACTION_RECEIVE_CONTENT:
      return {
        ...state,
        content: action.content.results,
        total: action.content.total,
      };
    default:
      return state;
  }
};

export default content;
